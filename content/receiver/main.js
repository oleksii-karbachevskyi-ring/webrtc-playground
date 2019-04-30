'use strict';

const connectButton = document.getElementById('connectButton');
const hangupButton = document.getElementById('hangupButton');

hangupButton.disabled = true;
connectButton.addEventListener('click', connect);
hangupButton.addEventListener('click', hangup);

let startTime;
const localVideo = document.getElementById('localVideo');

localVideo.addEventListener('loadedmetadata', function () {
    console.log(`Video width: ${this.videoWidth}px, height: ${this.videoHeight}px`);
});

localVideo.addEventListener('resize', () => {
    console.log(`Video size changed to ${localVideo.videoWidth}x${localVideo.videoHeight}`);
    // We'll use the first onsize callback as an indication that video has started
    // playing out.
    if (startTime) {
        const elapsedTime = window.performance.now() - startTime;
        console.log('Setup time: ' + elapsedTime.toFixed(3) + 'ms');
        startTime = null;
    }
});

let pc;
let rtpSender;
let offer;
let socket;
const offerOptions = {
    offerToReceiveAudio: 1,
    offerToReceiveVideo: 1
};

function getName(pc) {
    return 'Receive peer';
}

function connect() {
    socket = new WebSocket('ws://' + document.querySelector('#server').value);
    socket.onmessage = function (e) { onMessage(e.data); };
    socket.onopen = function () { socket.send('{"who":"receiver"}'); };
    hangupButton.disabled = false;
    const configuration = {};
    pc = new RTCPeerConnection(configuration);
    pc.addEventListener('icecandidate', e => onIceCandidate(pc, e));
    pc.addEventListener('iceconnectionstatechange', e => onIceStateChange(pc, e));
    pc.addEventListener('track', onTrack);
}

function hangup() {
    console.log('Ending call');
    pc.close();
    pc = null;
    localVideo.srcObject = null;
    connectButton.disabled = false;
    hangupButton.disabled = true;
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
            let remote_offer = { 'type': obj.offer.type, 'sdp': decodeURI(obj.offer.sdp_escaped) }
            await pc.setRemoteDescription(remote_offer);
            onSetRemoteSuccess(pc);
            console.log('pc createAnswer start');
            // Since the 'remote' side has no media stream we need
            // to pass in the right constraints in order for it to
            // accept the incoming offer of audio and video.
            const answer = await pc.createAnswer();
            await SetLocalDescriptionAndSendIt(answer);
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

    // candidate['sdpMid'] = event.candidate.sdpMid;
    // candidate['sdpMLineIndex'] = event.candidate.sdpMLineIndex;
    // if (pc == pc2) {
    //     candidate['candidate'] = event.candidate.candidate;
    //     await (pc1.addIceCandidate(candidate));
    // }
    // else {
    //     candidate['candidate'] = event.candidate.candidate.replace('100.64.0.2', '100.64.0.1');
    //     await (pc2.addIceCandidate(candidate));
    // }
    console.log(`${getName(pc)} ICE candidate:\n${JSON.stringify(event.candidate)}`);
}

function onTrack(e) {
    if (localVideo.srcObject !== e.streams[0]) {
        localVideo.srcObject = e.streams[0];
        console.log('pc received remote stream');
    }
}

function onCreateSessionDescriptionError(error) {
    console.log(`Failed to create session description: ${error.toString()}`);
}

async function SetLocalDescriptionAndSendIt(desc) {
    console.log(`Answer from pc:\n${desc.sdp}`);
    console.log('pc setLocalDescription start');
    try {
        await pc.setLocalDescription(desc);
        onSetLocalSuccess(pc);
    } catch (e) {
        onSetSessionDescriptionError(e);
    }
    socket.send(`{"offer":{"type":"${desc.type}", "sdp_escaped":"${encodeURI(desc.sdp)}"}}`);
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
