/**
 * InterviewAI - Autonomous AI HR Interviewer & Video Conference Controller
 * Full State Machine: IDLE -> AI_SPEAKING -> LISTENING -> THINKING -> NEXT_QUESTION -> FINISHED
 * Handles Webcam Stream, TTS Voice, Continuous STT, Silence Detection, and Dynamic Adaptive Flow.
 */

document.addEventListener('DOMContentLoaded', () => {
    initModeSelector();
    initWebcam();
    initInterviewEngine();
});

// 1. Mode Selector Cards in Setup Form
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

// 2. Candidate Webcam & Audio Media Stream Handler
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
                statusBadge.innerHTML = '<span class="recording-dot"></span> Candidate Cam & Mic';
                statusBadge.classList.add('badge-success');
            }
            if (requestCamBtn) requestCamBtn.style.display = 'none';
        } catch (err) {
            console.warn('[Webcam Notice]', err);
            if (statusBadge) {
                statusBadge.innerHTML = '<i class="fas fa-exclamation-triangle" style="color: var(--accent-amber);"></i> Camera Access Denied';
            }
        }
    }

    if (requestCamBtn) {
        requestCamBtn.addEventListener('click', startCamera);
    }
    
    // Auto-start camera if element is present
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

// 3. Autonomous AI HR Interviewer State Machine Engine
function initInterviewEngine() {
    const interviewIdInput = document.getElementById('interview-id');
    if (!interviewIdInput) return; // Not on interview live screen

    const interviewId = interviewIdInput.value;
    const questionIdInput = document.getElementById('current-question-id');
    const questionTextEl = document.getElementById('question-text-content');
    const answerInput = document.getElementById('answer-input');
    const transcriptBox = document.getElementById('live-transcript');
    const charCounter = document.getElementById('char-count');
    const stageContainer = document.getElementById('ai-stage-container');
    const statusBadge = document.getElementById('ai-status-badge');
    const statusDot = document.getElementById('ai-status-dot');
    const statusText = document.getElementById('ai-status-text');
    const sttStatusLabel = document.getElementById('stt-status-label');
    const silenceWrap = document.getElementById('silence-indicator-wrap');
    const silenceFill = document.getElementById('silence-progress-fill');
    const silenceText = document.getElementById('silence-text');

    const btnSubmitTurn = document.getElementById('btn-submit-turn');
    const btnSkipQuestion = document.getElementById('btn-skip-question');
    const btnTtsRead = document.getElementById('btn-tts-read');
    const replayBtn = document.getElementById('replay-question-btn');
    const btnSttToggle = document.getElementById('btn-stt-toggle');
    const timerDisplay = document.getElementById('timer-display');
    const timerContainer = document.getElementById('timer-container');
    const timeTakenInput = document.getElementById('time_taken_input');

    // States: IDLE, AI_SPEAKING, LISTENING, ANALYZING, GENERATING_QUESTION, COMPLETED
    let currentState = 'IDLE';
    let isSpeechRecognitionActive = false;
    let recognitionInstance = null;
    let lastSpeechTimestamp = 0;
    let hasSpokenInCurrentTurn = false;
    let silenceCheckInterval = null;
    let turnSecondsElapsed = 0;
    let turnTimerInterval = null;
    const SILENCE_TIMEOUT_MS = 2600; // 2.6s silence after answer triggers auto-advance

    // State UI Manager
    function setInterviewState(newState, customMessage = '') {
        currentState = newState;
        console.log(`[Interview State Machine] State: ${newState}`);

        // Update container classes
        if (stageContainer) {
            stageContainer.classList.remove(
                'state-idle', 'state-speaking', 'state-listening',
                'state-thinking', 'state-analyzing', 'state-generating',
                'state-generating-question', 'state-finished', 'state-completed'
            );
        }

        switch (newState) {
            case 'AI_SPEAKING':
                if (stageContainer) stageContainer.classList.add('state-speaking');
                if (statusText) statusText.textContent = customMessage || 'AI HR Speaking...';
                if (statusDot) statusDot.style.backgroundColor = 'var(--accent-purple)';
                if (sttStatusLabel) sttStatusLabel.textContent = 'Mic Paused during AI Speech';
                if (silenceWrap) silenceWrap.style.display = 'none';
                break;

            case 'LISTENING':
                if (stageContainer) stageContainer.classList.add('state-listening');
                if (statusText) statusText.textContent = customMessage || 'Listening to your answer...';
                if (statusDot) statusDot.style.backgroundColor = 'var(--accent-emerald)';
                if (sttStatusLabel) sttStatusLabel.textContent = 'Listening (Speak freely)';
                break;

            case 'ANALYZING':
                if (stageContainer) stageContainer.classList.add('state-analyzing');
                if (statusText) statusText.textContent = customMessage || 'Analyzing your answer...';
                if (statusDot) statusDot.style.backgroundColor = 'var(--accent-cyan, #38bdf8)';
                if (sttStatusLabel) sttStatusLabel.textContent = 'Analyzing response...';
                if (silenceWrap) silenceWrap.style.display = 'none';
                break;

            case 'GENERATING_QUESTION':
                if (stageContainer) stageContainer.classList.add('state-generating-question');
                if (statusText) statusText.textContent = customMessage || 'Generating next question...';
                if (statusDot) statusDot.style.backgroundColor = 'var(--primary)';
                if (sttStatusLabel) sttStatusLabel.textContent = 'Preparing next question...';
                if (silenceWrap) silenceWrap.style.display = 'none';
                break;

            case 'COMPLETED':
                if (stageContainer) stageContainer.classList.add('state-completed');
                if (statusText) statusText.textContent = customMessage || 'Interview Completed 🎉';
                if (statusDot) statusDot.style.backgroundColor = 'var(--accent-amber)';
                if (sttStatusLabel) sttStatusLabel.textContent = 'Evaluation complete!';
                if (silenceWrap) silenceWrap.style.display = 'none';
                break;

            default: // IDLE
                if (stageContainer) stageContainer.classList.add('state-idle');
                if (statusText) statusText.textContent = customMessage || 'AI HR Ready';
                if (statusDot) statusDot.style.backgroundColor = 'var(--primary)';
                break;
        }
    }


    // Question Timer (2 Minutes per Question)
    const QUESTION_TIMEOUT = 120;
    let timeRemaining = QUESTION_TIMEOUT;

    function startTurnTimer() {
        clearInterval(turnTimerInterval);
        timeRemaining = QUESTION_TIMEOUT;
        turnSecondsElapsed = 0;
        updateTimerDisplay();

        turnTimerInterval = setInterval(() => {
            if (currentState === 'FINISHED') {
                clearInterval(turnTimerInterval);
                return;
            }

            turnSecondsElapsed++;
            timeRemaining--;

            if (timeTakenInput) {
                timeTakenInput.value = turnSecondsElapsed;
            }

            updateTimerDisplay();

            if (timeRemaining <= 20 && timerContainer) {
                timerContainer.style.background = 'rgba(244, 63, 94, 0.15)';
                timerContainer.style.borderColor = 'rgba(244, 63, 94, 0.4)';
                timerContainer.style.color = 'var(--accent-rose)';
            } else if (timerContainer) {
                timerContainer.style.background = 'var(--bg-surface)';
                timerContainer.style.borderColor = 'var(--border-color)';
                timerContainer.style.color = 'inherit';
            }

            if (timeRemaining <= 0) {
                clearInterval(turnTimerInterval);
                console.warn("[Timer Expiration] Automatically submitting turn...");
                processTurn(false);
            }
        }, 1000);
    }

    function updateTimerDisplay() {
        if (!timerDisplay) return;
        const mins = Math.max(0, Math.floor(timeRemaining / 60));
        const secs = Math.max(0, timeRemaining % 60);
        timerDisplay.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }

    // Character Counter
    if (answerInput && charCounter) {
        answerInput.addEventListener('input', () => {
            charCounter.textContent = `${answerInput.value.length} characters`;
        });
    }

    // Speech-to-Text Setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        recognitionInstance = new SpeechRecognition();
        recognitionInstance.continuous = true;
        recognitionInstance.interimResults = true;
        recognitionInstance.lang = 'en-US';

        recognitionInstance.onstart = () => {
            isSpeechRecognitionActive = true;
            if (btnSttToggle) {
                btnSttToggle.classList.add('btn-primary');
                btnSttToggle.classList.remove('btn-outline');
                btnSttToggle.innerHTML = '<i class="fas fa-microphone"></i> Listening...';
            }
        };

        recognitionInstance.onend = () => {
            isSpeechRecognitionActive = false;
            // Auto-restart recognition if still in LISTENING state
            if (currentState === 'LISTENING') {
                try {
                    recognitionInstance.start();
                } catch (e) {
                    console.warn("[STT Restart Notice]", e);
                }
            } else if (btnSttToggle) {
                btnSttToggle.classList.remove('btn-primary');
                btnSttToggle.classList.add('btn-outline');
                btnSttToggle.innerHTML = '<i class="fas fa-microphone"></i> Voice Ready';
            }
        };

        recognitionInstance.onresult = (event) => {
            if (currentState !== 'LISTENING') return;

            let interimTranscript = '';
            let finalTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript + ' ';
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }

            if (finalTranscript || interimTranscript) {
                lastSpeechTimestamp = Date.now();
                hasSpokenInCurrentTurn = true;

                if (finalTranscript && answerInput) {
                    answerInput.value = (answerInput.value + ' ' + finalTranscript).trim();
                    if (charCounter) charCounter.textContent = `${answerInput.value.length} characters`;
                }

                if (transcriptBox) {
                    const currentTotal = (answerInput ? answerInput.value : '') + (interimTranscript ? ' ' + interimTranscript : '');
                    transcriptBox.textContent = currentTotal || 'Transcribing...';
                    transcriptBox.scrollTop = transcriptBox.scrollHeight;
                }

                // Show silence detector bar
                if (silenceWrap) silenceWrap.style.display = 'flex';
            }
        };

        recognitionInstance.onerror = (e) => {
            console.warn("[SpeechRecognition Notice]", e);
        };
    } else {
        if (btnSttToggle) {
            btnSttToggle.disabled = true;
            btnSttToggle.title = "Speech recognition is not supported in this browser. Please type your response.";
        }
        if (transcriptBox) {
            transcriptBox.textContent = "Spoken transcription not supported in this browser. You can type directly in the response box.";
        }
    }

    function startListening() {
        if (!recognitionInstance) {
            setInterviewState('LISTENING');
            return;
        }

        hasSpokenInCurrentTurn = false;
        lastSpeechTimestamp = 0;
        if (silenceFill) silenceFill.style.width = '0%';
        if (silenceWrap) silenceWrap.style.display = 'none';

        setInterviewState('LISTENING');

        try {
            if (!isSpeechRecognitionActive) {
                recognitionInstance.start();
            }
        } catch (err) {
            console.warn("[STT Start Notice]", err);
        }

        // Start silence detection interval
        clearInterval(silenceCheckInterval);
        silenceCheckInterval = setInterval(() => {
            if (currentState !== 'LISTENING') return;

            const textLength = answerInput ? answerInput.value.trim().length : 0;
            if (hasSpokenInCurrentTurn && textLength >= 8) {
                const elapsedSinceSpeech = Date.now() - lastSpeechTimestamp;
                const percent = Math.min(100, Math.round((elapsedSinceSpeech / SILENCE_TIMEOUT_MS) * 100));

                if (silenceFill) silenceFill.style.width = `${percent}%`;
                const secsRemaining = Math.max(0, ((SILENCE_TIMEOUT_MS - elapsedSinceSpeech) / 1000).toFixed(1));
                if (silenceText) silenceText.innerHTML = `<i class="fas fa-check-circle text-emerald"></i> Answer complete in ${secsRemaining}s...`;

                if (elapsedSinceSpeech >= SILENCE_TIMEOUT_MS) {
                    console.log("[Silence Detected] Automatically processing answer turn...");
                    clearInterval(silenceCheckInterval);
                    processTurn(false);
                }
            }
        }, 100);
    }

    function stopListening() {
        clearInterval(silenceCheckInterval);
        if (recognitionInstance && isSpeechRecognitionActive) {
            try {
                recognitionInstance.stop();
            } catch (err) {
                console.warn("[STT Stop Notice]", err);
            }
        }
        if (silenceWrap) silenceWrap.style.display = 'none';
    }

    // Text-to-Speech (TTS) Voice Synthesis
    function speakAIText(text, onComplete) {
        if (!text || !('speechSynthesis' in window)) {
            if (onComplete) onComplete();
            return;
        }

        stopListening();
        window.speechSynthesis.cancel();

        setInterviewState('AI_SPEAKING');

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        // Select a natural English voice if available
        const voices = window.speechSynthesis.getVoices();
        const preferredVoice = voices.find(v => (v.lang.startsWith('en') && (v.name.includes('Google') || v.name.includes('Natural') || v.name.includes('Samantha') || v.name.includes('Zira') || v.name.includes('Jenny'))));
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }

        let completed = false;
        function finishSpeech() {
            if (!completed) {
                completed = true;
                if (onComplete) onComplete();
            }
        }

        utterance.onend = finishSpeech;
        utterance.onerror = (e) => {
            console.warn("[TTS Error/Cancel]", e);
            finishSpeech();
        };

        // Safety fallback timeout in case speech end does not fire
        const estDuration = Math.max(2000, (text.split(' ').length / 2.5) * 1000 + 1500);
        setTimeout(() => {
            if (!completed && currentState === 'AI_SPEAKING') {
                finishSpeech();
            }
        }, estDuration);

        window.speechSynthesis.speak(utterance);
    }

    // Automated Turn Execution (AJAX to /interview/<id>/turn)
    let isTurnProcessing = false;

    async function processTurn(isSkip = false) {
        if (isTurnProcessing || currentState === 'COMPLETED') return;
        isTurnProcessing = true;

        stopListening();
        window.speechSynthesis?.cancel();

        setInterviewState('ANALYZING', 'Analyzing your answer...');
        if (btnSubmitTurn) btnSubmitTurn.disabled = true;
        if (btnSkipQuestion) btnSkipQuestion.disabled = true;

        const currentQId = questionIdInput ? questionIdInput.value : '';
        const answerText = isSkip ? '' : (answerInput ? answerInput.value.trim() : '');
        const timeTaken = turnSecondsElapsed;

        try {
            setInterviewState('GENERATING_QUESTION', 'Generating next adaptive question...');

            const response = await fetch(`/interview/${interviewId}/turn`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: currentQId,
                    answer: answerText,
                    time_taken: timeTaken
                })
            });

            const data = await response.json();

            if (data.status === 'success') {
                if (data.completed) {
                    setInterviewState('COMPLETED', 'Interview Completed! Generating Report...');
                    setTimeout(() => {
                        window.location.href = data.redirect_url || `/interview/${interviewId}/report`;
                    }, 1200);
                    return;
                }

                // Update to Next Question
                const nextQ = data.next_question;
                if (questionIdInput) questionIdInput.value = nextQ.id;
                if (questionTextEl) questionTextEl.textContent = nextQ.question_text;

                const qNumLabel = document.getElementById('q-num-label');
                if (qNumLabel) qNumLabel.textContent = data.current_q_num;

                const topicBadge = document.getElementById('topic-badge');
                if (topicBadge) topicBadge.innerHTML = `<i class="fas fa-tag"></i> ${nextQ.topic}`;

                const diffBadge = document.getElementById('difficulty-badge');
                if (diffBadge) diffBadge.textContent = nextQ.difficulty;

                const stageBadge = document.getElementById('interview-stage-badge');
                if (stageBadge) stageBadge.textContent = `Stage ${data.current_q_num}: Adaptive`;

                // Reset answer textarea & transcript
                if (answerInput) answerInput.value = '';
                if (transcriptBox) transcriptBox.textContent = 'Transcribing your speech in real-time...';
                if (charCounter) charCounter.textContent = '0 characters';

                startTurnTimer();

                // Build speech text: Transition phrase + Next question
                const transitionPhrase = data.transition_phrase ? data.transition_phrase + " " : "";
                const speechText = `${transitionPhrase} ${nextQ.question_text}`;

                speakAIText(speechText, () => {
                    startListening();
                });

            } else {
                console.error("[Turn Error]", data.message);
                alert("Notice: " + (data.message || "An error occurred. Retrying..."));
                startListening();
            }
        } catch (err) {
            console.error("[Turn Network Error]", err);
            startListening();
        } finally {
            isTurnProcessing = false;
            if (btnSubmitTurn) btnSubmitTurn.disabled = false;
            if (btnSkipQuestion) btnSkipQuestion.disabled = false;
        }
    }


    // Manual Event Listeners
    if (btnSubmitTurn) {
        btnSubmitTurn.addEventListener('click', (e) => {
            e.preventDefault();
            processTurn(false);
        });
    }

    if (btnSkipQuestion) {
        btnSkipQuestion.addEventListener('click', (e) => {
            e.preventDefault();
            processTurn(true);
        });
    }

    if (btnTtsRead && questionTextEl) {
        btnTtsRead.addEventListener('click', () => {
            speakAIText(questionTextEl.textContent.trim(), () => {
                startListening();
            });
        });
    }

    if (replayBtn && questionTextEl) {
        replayBtn.addEventListener('click', () => {
            speakAIText(questionTextEl.textContent.trim(), () => {
                startListening();
            });
        });
    }

    if (btnSttToggle) {
        btnSttToggle.addEventListener('click', (e) => {
            e.preventDefault();
            if (currentState === 'LISTENING') {
                stopListening();
                setInterviewState('IDLE', 'Microphone Paused');
            } else {
                startListening();
            }
        });
    }

    // Initialize Follow-up Handler
    initFollowupHandler();

    // Start Question 1 Flow Automatically
    startTurnTimer();
    const initialQuestionText = questionTextEl ? questionTextEl.textContent.trim() : '';
    if (initialQuestionText) {
        setTimeout(() => {
            const greeting = "Hello! I am Sophia, your AI HR and Technical Interviewer. Let's begin.";
            const fullIntro = `${greeting} ${initialQuestionText}`;
            speakAIText(fullIntro, () => {
                startListening();
            });
        }, 700);
    }
}

// 4. Dynamic AI Follow-up Handler
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
            followupBtn.innerHTML = '<i class="fas fa-robot"></i> Ask Dynamic Follow-up';
        }
    });
}

