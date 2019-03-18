'use strict';

const startButton = document.getElementById('startButton');
const createOfferButton = document.getElementById('createOfferButton');
const setOfferButton = document.getElementById('setOfferButton');
const hangupButton = document.getElementById('hangupButton');

createOfferButton.disabled = true;
setOfferButton.disabled = true;
hangupButton.disabled = true;
startButton.addEventListener('click', start);
createOfferButton.addEventListener('click', createOffer);
setOfferButton.addEventListener('click', setOffer);
hangupButton.addEventListener('click', hangup);

let startTime;
const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

localVideo.addEventListener('loadedmetadata', function() {
  console.log(`Local video videoWidth: ${this.videoWidth}px,  videoHeight: ${this.videoHeight}px`);
});

remoteVideo.addEventListener('loadedmetadata', function() {
  console.log(`Remote video videoWidth: ${this.videoWidth}px,  videoHeight: ${this.videoHeight}px`);
});

remoteVideo.addEventListener('resize', () => {
  console.log(`Remote video size changed to ${remoteVideo.videoWidth}x${remoteVideo.videoHeight}`);
  // We'll use the first onsize callback as an indication that video has started
  // playing out.
  if (startTime) {
    const elapsedTime = window.performance.now() - startTime;
    console.log('Setup time: ' + elapsedTime.toFixed(3) + 'ms');
    startTime = null;
  }
});

let localStream;
let pc1;
let pc2;
let rtpSender;
let offer;
const offerOptions = {
  offerToReceiveAudio: 1,
  offerToReceiveVideo: 1
};

function getName(pc) {
  return (pc === pc1) ? 'pc1' : 'pc2';
}

function getOtherPc(pc) {
  return (pc === pc1) ? pc2 : pc1;
}

async function start() {
  console.log('Requesting local stream');
  startButton.disabled = true;
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: false, video: {
      width: { exact: 1920 },
      height: { exact: 1080 },
      frameRate: { exact: 30 }
    }});
    console.log('Received local stream');
    localVideo.srcObject = stream;
    localStream = stream;
    createOfferButton.disabled = false;
  } catch (e) {
    alert(`getUserMedia() error: ${e.name}`);
  }
}

function getSelectedSdpSemantics() {
  const sdpSemanticsSelect = document.querySelector('#sdpSemantics');
  const option = sdpSemanticsSelect.options[sdpSemanticsSelect.selectedIndex];
  return option.value === '' ? {} : {sdpSemantics: option.value};
}

async function createOffer() {
  createOfferButton.disabled = true;
  setOfferButton.disabled = false;
  console.log('Creating an offer');
  startTime = window.performance.now();
  const videoTracks = localStream.getVideoTracks();
  if (videoTracks.length > 0) {
    console.log(`Using video device: ${videoTracks[0].label}`);
  }
  const configuration = getSelectedSdpSemantics();
  console.log('RTCPeerConnection configuration:', configuration);
  pc1 = new RTCPeerConnection(configuration);
  pc1.addEventListener('icecandidate', e => onIceCandidate(pc1, e));
  pc1.addEventListener('iceconnectionstatechange', e => onIceStateChange(pc1, e));
  console.log('Created local peer connection object pc1');
  pc2 = new RTCPeerConnection(configuration);
  pc2.addEventListener('icecandidate', e => onIceCandidate(pc2, e));
  pc2.addEventListener('iceconnectionstatechange', e => onIceStateChange(pc2, e));
  pc2.addEventListener('track', gotRemoteStream);
  console.log('Created remote peer connection object pc2');

  rtpSender = pc1.addTrack(videoTracks[0], localStream);
  const old_params = rtpSender.getParameters();
  let new_params = old_params;
  new_params['degradationPreference'] = 'maintain-resolution'
  try {
    rtpSender.setParameters(new_params);
  } catch (e) {
    console.log(`Failed to set parameters:\n${new_params.toString()}\nError:${e.toString()}`);
  }
  console.log('Added local stream to pc1');

  try {
    console.log('pc1 createOffer start');
    offer = await pc1.createOffer(offerOptions);
  } catch (e) {
    onCreateSessionDescriptionError(e);
  }
}

function onCreateSessionDescriptionError(error) {
  console.log(`Failed to create session description: ${error.toString()}`);
}

function FindCodecs() {
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
}

async function setOffer() {
  hangupButton.disabled = false;
  console.log(`Offer from pc1\n${offer.sdp}`);

  console.log('pc1 setLocalDescription start');
  FindCodecs();
  try {
    await pc1.setLocalDescription(offer);
    onSetLocalSuccess(pc1);
  } catch (e) {
    onSetSessionDescriptionError(e);
  }

  console.log('pc2 setRemoteDescription start');
  try {
    await pc2.setRemoteDescription(offer);
    onSetRemoteSuccess(pc2);
  } catch (e) {
    onSetSessionDescriptionError(e);
  }

  console.log('pc2 createAnswer start');
  // Since the 'remote' side has no media stream we need
  // to pass in the right constraints in order for it to
  // accept the incoming offer of audio and video.
  try {
    const answer = await pc2.createAnswer();
    await onCreateAnswerSuccess(answer);
  } catch (e) {
    onCreateSessionDescriptionError(e);
  }
}

async function onCreateAnswerSuccess(desc) {
  console.log(`Answer from pc2:\n${desc.sdp}`);
  console.log('pc2 setLocalDescription start');
  try {
    await pc2.setLocalDescription(desc);
    onSetLocalSuccess(pc2);
  } catch (e) {
    onSetSessionDescriptionError(e);
  }
  console.log('pc1 setRemoteDescription start');
  try {
    await pc1.setRemoteDescription(desc);
    onSetRemoteSuccess(pc1);
  } catch (e) {
    onSetSessionDescriptionError(e);
  }
}

function onSetLocalSuccess(pc) {
  console.log(`${getName(pc)} setLocalDescription complete`);
}

function onSetRemoteSuccess(pc) {
  console.log(`${getName(pc)} setRemoteDescription complete`);
}

function onSetSessionDescriptionError(error) {
  console.log(`Failed to set session description: ${error.toString()}`);
}

function gotRemoteStream(e) {
  if (remoteVideo.srcObject !== e.streams[0]) {
    remoteVideo.srcObject = e.streams[0];
    console.log('pc2 received remote stream');
  }
}

async function onIceCandidate(pc, event) {
  try {
    await (getOtherPc(pc).addIceCandidate(event.candidate));
    onAddIceCandidateSuccess(pc);
  } catch (e) {
    onAddIceCandidateError(pc, e);
  }
  console.log(`${getName(pc)} ICE candidate:\n${event.candidate ? event.candidate.candidate : '(null)'}`);
}

function onAddIceCandidateSuccess(pc) {
  console.log(`${getName(pc)} addIceCandidate success`);
}

function onAddIceCandidateError(pc, error) {
  console.log(`${getName(pc)} failed to add ICE Candidate: ${error.toString()}`);
}

function onIceStateChange(pc, event) {
  if (pc) {
    console.log(`${getName(pc)} ICE state: ${pc.iceConnectionState}`);
    console.log('ICE state change event: ', event);
  }
}

function hangup() {
  console.log('Ending call');
  rtpSender = null;
  pc1.close();
  pc2.close();
  pc1 = null;
  pc2 = null;
  localVideo.srcObject = null;
  localStream = null;
  startButton.disabled = false;
  createOfferButton.disabled = true;
  setOfferButton.disabled = true;
  hangupButton.disabled = true;
}
