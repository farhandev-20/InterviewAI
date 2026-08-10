/* ==========================================================================
   Live AI Voice Interview Runner Engine
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  // If interview.js is active on this page, let interview.js drive the state machine
  if (document.getElementById('interview-id')) {
    initExitModal();
    return;
  }

  const timerElement = document.getElementById('timer-display');
  const timerContainer = document.getElementById('timer-container');
  const answerTextarea = document.getElementById('answer');
  const charCounter = document.getElementById('char-count');
  const interviewForm = document.getElementById('interview-form');
  const actionInput = document.getElementById('action-input');
  const timeTakenInput = document.getElementById('time-taken-input');
  const questionTextElement = document.getElementById('question-text');


  // Config: 2 minutes per question (120 seconds)
  const QUESTION_TIMEOUT = 120;
  let timeRemaining = QUESTION_TIMEOUT;
  let timeElapsed = 0;
  let timerInterval = null;
  let isPaused = false;
  let isMuted = false;

  // 1. Initialize Countdown Timer
  if (timerElement) {
    updateTimerDisplay();

    timerInterval = setInterval(() => {
      if (isPaused) return; // Skip tick if paused

      timeRemaining--;
      timeElapsed++;

      if (timeTakenInput) {
        timeTakenInput.value = timeElapsed;
      }

      updateTimerDisplay();

      // Warning state when time is below 20 seconds
      if (timeRemaining <= 20) {
        if (timerContainer) {
          timerContainer.style.background = 'rgba(244, 63, 94, 0.15)';
          timerContainer.style.borderColor = 'rgba(244, 63, 94, 0.4)';
          timerContainer.style.color = 'var(--accent-rose)';
        }
      }

      if (timeRemaining <= 0) {
        clearInterval(timerInterval);
        handleTimerExpiration();
      }
    }, 1000);
  }

  function updateTimerDisplay() {
    if (!timerElement) return;
    const mins = Math.floor(timeRemaining / 60);
    const secs = timeRemaining % 60;
    timerElement.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }

  function handleTimerExpiration() {
    console.warn("Time expired for current question. Auto-advancing...");
    if (actionInput && interviewForm) {
      actionInput.value = 'next';
      interviewForm.submit();
    }
  }

  // 2. Character Counter
  if (answerTextarea && charCounter) {
    const updateCharCount = () => {
      const len = answerTextarea.value.length;
      charCounter.textContent = `${len} characters`;
    };

    answerTextarea.addEventListener('input', updateCharCount);
    updateCharCount();
  }

  // 3. Web Speech API - Voice Synthesis (Auto-read, Replay, Mute)
  function speakQuestion(text) {
    if (isMuted || !('speechSynthesis' in window) || !text) return;
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.pitch = 1.0;
    window.speechSynthesis.speak(utterance);
  }

  // Auto-read question on load
  if (questionTextElement) {
    setTimeout(() => {
      speakQuestion(questionTextElement.textContent.trim());
    }, 600);
  }

  // Replay Button
  const replayBtn = document.getElementById('replay-question-btn');
  if (replayBtn && questionTextElement) {
    replayBtn.addEventListener('click', () => {
      speakQuestion(questionTextElement.textContent.trim());
    });
  }

  // Mute / Unmute Button
  const muteBtn = document.getElementById('mute-voice-btn');
  if (muteBtn) {
    muteBtn.addEventListener('click', () => {
      isMuted = !isMuted;
      if (isMuted) {
        window.speechSynthesis?.cancel();
        muteBtn.innerHTML = '<i class="fas fa-volume-mute" style="color: var(--accent-rose);"></i> Voice Muted';
        muteBtn.classList.add('btn-outline');
      } else {
        muteBtn.innerHTML = '<i class="fas fa-volume-up" style="color: var(--accent-emerald);"></i> Voice Active';
        speakQuestion(questionTextElement?.textContent.trim());
      }
    });
  }

  // Pause / Resume Interview Controls
  const pauseBtn = document.getElementById('pause-interview-btn');
  if (pauseBtn) {
    pauseBtn.addEventListener('click', () => {
      isPaused = !isPaused;
      if (isPaused) {
        window.speechSynthesis?.pause();
        pauseBtn.innerHTML = '<i class="fas fa-play" style="color: var(--accent-emerald);"></i> Resume Interview';
        if (timerContainer) timerContainer.style.opacity = '0.5';
      } else {
        window.speechSynthesis?.resume();
        pauseBtn.innerHTML = '<i class="fas fa-pause" style="color: var(--accent-amber);"></i> Pause Interview';
        if (timerContainer) timerContainer.style.opacity = '1';
      }
    });
  }

  // 4. Web Speech API - Microphone Dictation (Speech-to-Text)
  const micBtn = document.getElementById('mic-btn');
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (micBtn && answerTextarea && SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    let isListening = false;

    micBtn.addEventListener('click', () => {
      if (!isListening) {
        try {
          recognition.start();
          isListening = true;
          micBtn.style.background = 'rgba(244, 63, 94, 0.2)';
          micBtn.style.color = 'var(--accent-rose)';
          micBtn.style.borderColor = 'var(--accent-rose)';
          micBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
        } catch (e) {
          console.error("Speech recognition error:", e);
        }
      } else {
        recognition.stop();
        isListening = false;
        micBtn.style.background = 'var(--bg-surface)';
        micBtn.style.color = 'var(--text-primary)';
        micBtn.style.borderColor = 'var(--border-color)';
        micBtn.innerHTML = '<i class="fas fa-microphone" style="color: var(--primary);"></i> Voice Dictation';
      }
    });

    recognition.onresult = (event) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      if (answerTextarea) {
        answerTextarea.value += (answerTextarea.value ? ' ' : '') + transcript;
        answerTextarea.dispatchEvent(new Event('input'));
      }
    };

    recognition.onerror = (e) => {
      console.warn("Speech recognition notice:", e);
      isListening = false;
      micBtn.innerHTML = '<i class="fas fa-microphone" style="color: var(--primary);"></i> Voice Dictation';
    };
  } else if (micBtn) {
    micBtn.addEventListener('click', () => {
      alert("Browser Speech Recognition is not supported on this browser version. You can type your response directly into the answer box.");
    });
  }

  // 5. Action Navigation Buttons
  const navBtns = document.querySelectorAll('[data-action]');
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const action = btn.getAttribute('data-action');
      if (actionInput && interviewForm) {
        actionInput.value = action;
        interviewForm.submit();
      }
    });
  });

  // 6. Exit Confirmation Modal
  initExitModal();
});

function initExitModal() {
  const exitBtn = document.getElementById('exit-interview-btn');
  const exitModal = document.getElementById('exit-modal');
  const cancelExitBtn = document.getElementById('cancel-exit-btn');
  const confirmExitBtn = document.getElementById('confirm-exit-btn');

  if (exitBtn && exitModal) {
    exitBtn.addEventListener('click', (e) => {
      e.preventDefault();
      exitModal.classList.add('active');
    });

    if (cancelExitBtn) {
      cancelExitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        exitModal.classList.remove('active');
      });
    }

    if (confirmExitBtn) {
      confirmExitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        window.location.href = confirmExitBtn.getAttribute('data-href') || '/dashboard';
      });
    }
  }
}

