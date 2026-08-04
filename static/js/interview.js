/**
 * InterviewAI - Modern Client-Side Controller
 * Handles Webcam Stream, Speech-to-Text (STT), Text-to-Speech (TTS), Timer & AI Follow-ups
 */

document.addEventListener('DOMContentLoaded', () => {
    initModeSelector();
    initWebcam();
    initSpeechToText();
    initTextToSpeech();
    initLiveTimer();
    initFollowupHandler();
});

// Mode Selector Cards in Setup Form
function initModeSelector() {
    const modeCards = document.querySelectorAll('.mode-card');
    if (!modeCards.length) return;

    modeCards.forEach(card => {
        card.addEventListener('click', () => {
            modeCards.forEach(c => c.classList.remove('active'));
            card.classList.add('active');
            const radio = card.querySelector('input[type="radio"]');
            if (radio) radio.checked = true;
        });
    });
}

// Webcam Media Stream Handler
let webcamStream = null;
function initWebcam() {
    const videoElement = document.getElementById('webcam-preview');
    if (!videoElement) return;

    const requestCamBtn = document.getElementById('btn-request-cam');
    const toggleCamBtn = document.getElementById('btn-toggle-cam');
    const toggleMicBtn = document.getElementById('btn-toggle-mic');
    const statusBadge = document.getElementById('cam-status-badge');

    async function startCamera() {
        try {
            webcamStream = await navigator.mediaDevices.getUserMedia({
                video: { width: { ideal: 1280 }, height: { ideal: 720 } },
                audio: true
            });
            videoElement.srcObject = webcamStream;
            if (statusBadge) {
                statusBadge.innerHTML = '<span class="recording-dot"></span> Camera & Mic Active';
                statusBadge.classList.add('badge-success');
            }
            if (requestCamBtn) requestCamBtn.style.display = 'none';
        } catch (err) {
            console.warn('[Webcam Notice]', err);
            if (statusBadge) {
                statusBadge.innerHTML = '<i class="fas fa-exclamation-triangle text-amber"></i> Camera Access Denied';
            }
        }
    }

    if (requestCamBtn) {
        requestCamBtn.addEventListener('click', startCamera);
    }
    
    // Auto-start camera if element present
    startCamera();

    if (toggleCamBtn) {
        toggleCamBtn.addEventListener('click', () => {
            if (!webcamStream) return;
            const videoTracks = webcamStream.getVideoTracks();
            if (videoTracks.length > 0) {
                const enabled = !videoTracks[0].enabled;
                videoTracks[0].enabled = enabled;
                toggleCamBtn.classList.toggle('btn-secondary', !enabled);
                toggleCamBtn.innerHTML = enabled ? '<i class="fas fa-video"></i> Cam On' : '<i class="fas fa-video-slash"></i> Cam Off';
            }
        });
    }

    if (toggleMicBtn) {
        toggleMicBtn.addEventListener('click', () => {
            if (!webcamStream) return;
            const audioTracks = webcamStream.getAudioTracks();
            if (audioTracks.length > 0) {
                const enabled = !audioTracks[0].enabled;
                audioTracks[0].enabled = enabled;
                toggleMicBtn.classList.toggle('btn-secondary', !enabled);
                toggleMicBtn.innerHTML = enabled ? '<i class="fas fa-microphone"></i> Mic On' : '<i class="fas fa-microphone-slash"></i> Muted';
            }
        });
    }
}

// Speech-to-Text (STT) Handler
let recognition = null;
let isRecognizing = false;

function initSpeechToText() {
    const micToggleBtn = document.getElementById('btn-stt-toggle');
    const answerInput = document.getElementById('answer-input');
    const transcriptBox = document.getElementById('live-transcript');
    const audioWave = document.getElementById('audio-wave-visualizer');

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        if (micToggleBtn) {
            micToggleBtn.disabled = true;
            micToggleBtn.title = "Speech Recognition not supported in this browser. Please type your answer.";
        }
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isRecognizing = true;
        if (micToggleBtn) {
            micToggleBtn.classList.add('btn-danger');
            micToggleBtn.innerHTML = '<i class="fas fa-stop-circle"></i> Stop Recording';
        }
        if (audioWave) audioWave.classList.add('active');
    };

    recognition.onend = () => {
        isRecognizing = false;
        if (micToggleBtn) {
            micToggleBtn.classList.remove('btn-danger');
            micToggleBtn.innerHTML = '<i class="fas fa-microphone"></i> Start Voice Answer';
        }
        if (audioWave) audioWave.classList.remove('active');
    };

    recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript + ' ';
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }

        if (finalTranscript) {
            if (answerInput) answerInput.value = (answerInput.value + ' ' + finalTranscript).trim();
            if (transcriptBox) transcriptBox.innerText = answerInput.value;
        } else if (interimTranscript && transcriptBox) {
            transcriptBox.innerText = (answerInput ? answerInput.value + ' ' : '') + interimTranscript;
        }
    };

    if (micToggleBtn) {
        micToggleBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (isRecognizing) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });
    }
}

// Text-to-Speech (TTS) Handler
function initTextToSpeech() {
    const speakBtn = document.getElementById('btn-tts-read');
    const questionTextEl = document.getElementById('question-text-content');

    if (!speakBtn || !questionTextEl || !('speechSynthesis' in window)) return;

    speakBtn.addEventListener('click', () => {
        if (window.speechSynthesis.speaking) {
            window.speechSynthesis.cancel();
            speakBtn.innerHTML = '<i class="fas fa-volume-up"></i> Read Aloud';
            return;
        }

        const text = questionTextEl.innerText.trim();
        if (!text) return;

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        utterance.onstart = () => {
            speakBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Reading';
        };

        utterance.onend = () => {
            speakBtn.innerHTML = '<i class="fas fa-volume-up"></i> Read Aloud';
        };

        window.speechSynthesis.speak(utterance);
    });
}

// Live Timer Display
function initLiveTimer() {
    const timerDisplay = document.getElementById('live-question-timer');
    const timeTakenHidden = document.getElementById('time_taken_input');
    if (!timerDisplay) return;

    let seconds = 0;
    setInterval(() => {
        seconds++;
        if (timeTakenHidden) timeTakenHidden.value = seconds;
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        timerDisplay.innerText = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }, 1000);
}

// Dynamic AI Follow-up Handler
function initFollowupHandler() {
    const followupBtn = document.getElementById('btn-ask-followup');
    const followupContainer = document.getElementById('followup-container');
    const followupText = document.getElementById('followup-text');
    const answerInput = document.getElementById('answer-input');
    const questionTextEl = document.getElementById('question-text-content');

    if (!followupBtn || !followupContainer || !followupText) return;

    followupBtn.addEventListener('click', async () => {
        const interviewId = followupBtn.dataset.interviewId;
        if (!interviewId) return;

        followupBtn.disabled = true;
        followupBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating Follow-up...';

        try {
            const res = await fetch(`/interview/${interviewId}/follow-up`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_text: questionTextEl ? questionTextEl.innerText : '',
                    answer: answerInput ? answerInput.value : ''
                })
            });

            const data = await res.json();
            if (data.status === 'success' && data.followup) {
                followupText.innerText = data.followup;
                followupContainer.style.display = 'block';
                followupContainer.scrollIntoView({ behavior: 'smooth' });
            }
        } catch (err) {
            console.error('Follow-up error:', err);
        } finally {
            followupBtn.disabled = false;
            followupBtn.innerHTML = '<i class="fas fa-robot"></i> Ask Dynamic AI Follow-up';
        }
    });
}
