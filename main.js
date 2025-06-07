// main.js
// Handles form logic, file reading, API calls, and page navigation

document.addEventListener('DOMContentLoaded', function () {
    // Main page logic
    const audioForm = document.getElementById('audioForm');
    const audioFileInput = document.getElementById('audioFile');
    const languageSelect = document.getElementById('language');
    const submitBtn = document.getElementById('submitBtn');

    if (audioForm) {
        // Enable submit button only if both fields are filled
        function checkForm() {
            submitBtn.disabled = !(audioFileInput.files.length > 0 && languageSelect.value);
        }
        audioFileInput.addEventListener('change', checkForm);
        languageSelect.addEventListener('change', checkForm);

        audioForm.addEventListener('submit', function (e) {
            e.preventDefault();
            // Redirect to loading page and start upload
            window.location.href = 'Pages/loading.html';
            // Save form data to localStorage for loading page to use
            const file = audioFileInput.files[0];
            const reader = new FileReader();
            reader.onload = function (event) {
                localStorage.setItem('audio_base64', event.target.result);
                localStorage.setItem('language', languageSelect.value);
                // After file is read, loading page JS will pick up
            };
            reader.readAsDataURL(file);
        });
    }

    // Loading page logic
    if (window.location.pathname.endsWith('loading.html')) {
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        let progress = 0;
        function updateProgress(val) {
            progressBar.style.width = val + '%';
            progressText.textContent = 'Processing: ' + val + '%';
        }
        updateProgress(10);
        // Prepare data
        const audio_base64 = localStorage.getItem('audio_base64');
        const language = localStorage.getItem('language');
        if (!audio_base64 || !language) {
            progressText.textContent = 'Missing data. Please start again.';
            return;
        }
        // Simulate progress
        let interval = setInterval(() => {
            if (progress < 70) {
                progress += 10;
                updateProgress(progress);
            }
        }, 300);
        // Send to backend
        fetch('/api/process-audio', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ language, audio_base64 })
        })
        .then(res => res.json())
        .then(data => {
            clearInterval(interval);
            updateProgress(100);
            localStorage.setItem('result_audio_base64', data.result_audio_base64);
            setTimeout(() => {
                window.location.href = 'result.html';
            }, 600);
        })
        .catch(() => {
            clearInterval(interval);
            progressText.textContent = 'Error processing audio.';
        });
    }

    // Result page logic
    if (window.location.pathname.endsWith('result.html')) {
        const audioElem = document.getElementById('resultAudio');
        const backBtn = document.getElementById('backBtn');
        const resultAudioBase64 = localStorage.getItem('result_audio_base64');
        if (resultAudioBase64 && audioElem) {
            audioElem.src = resultAudioBase64;
            // Download button
            let downloadBtn = document.createElement('a');
            downloadBtn.textContent = 'Download Audio';
            downloadBtn.href = resultAudioBase64;
            downloadBtn.download = 'result_audio.' + (resultAudioBase64.includes('mp3') ? 'mp3' : 'wav');
            downloadBtn.className = 'download-btn';
            audioElem.parentNode.insertBefore(downloadBtn, backBtn);
        }
        if (backBtn) {
            backBtn.onclick = function () {
                localStorage.clear();
                window.location.href = '../index.html';
            };
        }
    }
});
