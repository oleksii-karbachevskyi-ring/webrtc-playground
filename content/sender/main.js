'use strict';

const startButton = document.getElementById('startButton');
const connectButton = document.getElementById('connectButton');
const negotiateButton = document.getElementById('negotiateButton');
const hangupButton = document.getElementById('hangupButton');

connectButton.disabled = true;
negotiateButton.disabled = true;
hangupButton.disabled = true;
startButton.addEventListener('click', start);
connectButton.addEventListener('click', connect);
negotiateButton.addEventListener('click', negotiate);
hangupButton.addEventListener('click', hangup);

let startTime;
const localVideo = document.getElementById('localVideo');

localVideo.addEventListener('loadedmetadata', function() {
  console.log(`Local video videoWidth: ${this.videoWidth}px,  videoHeight: ${this.videoHeight}px`);
});

let localStream;
let pc;
let rtpSender;
let offer;
let socket;
const offerOptions = {
    offerToReceiveAudio: 0,
    offerToReceiveVideo: 1
};

function getName(pc) {
    return 'Sender peer';
}

async function start() {
  console.log('Requesting local stream');
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: false, video: {
      width:     { exact: parseInt(document.querySelector('#width').value) },
      height:    { exact: parseInt(document.querySelector('#height').value) },
      frameRate: { exact: parseInt(document.querySelector('#framerate').value) }
    }});
    console.log('Received local stream');
    localVideo.srcObject = stream;
    localStream = stream;
    connectButton.disabled = false;
  } catch (e) {
    alert(`getUserMedia() error: ${e.name}`);
  }
}

function connect() {
    socket = new WebSocket('ws://' + document.querySelector('#server').value);
    socket.onmessage = function (e) { onMessage(e.data); };
    socket.onopen = function () { socket.send('{"who":"sender"}'); };
    negotiateButton.disabled = false;
}

async function negotiate() {
    const videoTracks = localStream.getVideoTracks();
    const configuration = {};
    pc = new RTCPeerConnection(configuration);
    pc.addEventListener('icecandidate', e => onIceCandidate(pc, e));
    pc.addEventListener('iceconnectionstatechange', e => onIceStateChange(pc, e));

    rtpSender = pc.addTrack(videoTracks[0], localStream);
    const old_params = rtpSender.getParameters();
    let new_params = old_params;
    new_params['degradationPreference'] = 'maintain-resolution'
    try {
        rtpSender.setParameters(new_params);
    } catch (e) {
        console.log(`Failed to set parameters:\n${new_params.toString()}\nError:${e.toString()}`);
    }
    console.log('Added local stream');

    try {
        console.log('pc createOffer start');
        offer = await pc.createOffer(offerOptions);
    } catch (e) {
        onCreateSessionDescriptionError(e);
    }

    ChangePreferredCodec();
    try {
        await pc.setLocalDescription(offer);
        sendOffer();
    } catch (e) {
        onSetSessionDescriptionError(e);
    }
}

async function onMessage(data) {
    console.log(data);
    let obj = JSON.parse(data);
    if (obj.hasOwnProperty('ice')) {
        try {
            let candidate = {}
            if (obj.ice) {
                candidate['sdpMid'] = obj.ice.sdpMid;
                candidate['sdpMLineIndex'] = obj.ice.sdpMLineIndex;
                candidate['candidate'] = decodeURI(obj.ice.candidate_escaped);
            }
            await (pc.addIceCandidate(candidate));
            onAddIceCandidateSuccess(pc);
        } catch (e) {
            onAddIceCandidateError(pc, e);
        }
    }
    if (obj.hasOwnProperty('offer')) {
        try {
            let remote_offer = {'type': obj.offer.type, 'sdp': decodeURI(obj.offer.sdp_escaped)}
            await pc.setRemoteDescription(remote_offer);
            onSetRemoteSuccess(pc);
        } catch (e) {
            onSetSessionDescriptionError(e);
        }
    }
}

async function onIceCandidate(pc, event) {
    if (event.candidate == null) {
        console.log(`${getName(pc)} ICE candidate is null`);
        socket.send('{"ice":null}')
        return;
    }
    let c = event.candidate;
    socket.send(`{"ice":{"candidate_escaped":"${encodeURI(c.candidate)}", "sdpMid":"${c.sdpMid}", "sdpMLineIndex":${c.sdpMLineIndex}}}`)
    console.log(`${getName(pc)} ICE candidate sent:\n${JSON.stringify(event.candidate)}`);
}
  
function onCreateSessionDescriptionError(error) {
  console.log(`Failed to create session description: ${error.toString()}`);
}

function ChangePreferredCodec() {
  let sdp = offer.sdp;
  sdp = sdp.split('\n');
  let selected = document.querySelector('#codec');
  selected = selected.options[selected.selectedIndex].value;
  for (var i=0;i<sdp.length;i++) {
    if (sdp[i].startsWith('m=video')) {
      let l = sdp[i];
      const len = selected.length;
      let pos = l.search(selected);
      if (pos != -1) {
        // m=video 9 UDP/TLS/RTP/SAVPF 96 97 98 99 100 101 102 123 127 122 125 107 108 109 124
        let pts_selected = selected.split(' ') // '', '96' , '97'
        let x = l.split(' ')
        let y = [x[0], x[1], x[2], pts_selected[1], pts_selected[2]]
        for (var j=3; j<x.length; j++)
          if (selected.search(x[j]) == -1)
            y.push(x[j])
        let new_line = y.join(' ');
        sdp[i] = new_line;
        i = sdp.length; // exiting
      }
    }
  }
  offer.sdp = sdp.join('\n');
  console.log(`${offer.sdp}`);
}

function sendOffer() {
    socket.send(`{"offer":{"type":"${offer.type}", "sdp_escaped":"${encodeURI(offer.sdp)}"}}`);
    console.log('Offer is sent');
}

function onSetRemoteSuccess(pc) {
  console.log(`${getName(pc)} setRemoteDescription complete`);
}

function onSetSessionDescriptionError(error) {
  console.log(`Failed to set session description: ${error.toString()}`);
}

function onAddIceCandidateSuccess(pc) {
  console.log(`${getName(pc)} addIceCandidate success`);
}

function onAddIceCandidateError(pc, error) {
  console.log(`${getName(pc)} failed to add ICE Candidate: ${error.toString()}`);
}

function onIceStateChange(pc, event) {
  if (pc) {
    console.log(`New ICE state: ${pc.iceConnectionState}`);
  }
}

function hangup() {
  console.log('Ending call');
  rtpSender = null;
  pc.close();
  pc = null;
  localVideo.srcObject = null;
  localStream = null;
  startButton.disabled = false;
  createOfferButton.disabled = true;
  setOfferButton.disabled = true;
  hangupButton.disabled = true;
}
