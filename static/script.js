// static/script.js
const output = document.getElementById('output');
const animTitle = document.getElementById('anim-title');
const stopBtn = document.getElementById('stop-btn');
let eventSource = null;

// Start animation
document.querySelectorAll('.anim-link').forEach(link => {
  link.addEventListener('click', (e) => {
    e.preventDefault();
    const key = e.target.dataset.key;
    startAnimation(key);
  });
});

document.getElementById('random-btn').addEventListener('click', () => {
  const links = document.querySelectorAll('.anim-link');
  const randomLink = links[Math.floor(Math.random() * links.length)];
  const key = randomLink.dataset.key;
  startAnimation(key);
});

function startAnimation(key) {
  fetch(`/start/${key}`)
    .then(res => res.json())
    .then(data => {
      if (data.error) {
        alert(data.error);
        return;
      }
      animTitle.textContent = data.animation;
      stopBtn.disabled = false;
      output.textContent = '';
      startStream();
    });
}

function startStream() {
  if (eventSource) eventSource.close();
  eventSource = new EventSource('/stream');

  eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.start) {
      output.textContent = '';
    } else if (data.line !== undefined) {
      output.textContent += data.line + '\n';
      output.scrollTop = output.scrollHeight;
    } else if (data.done) {
      animTitle.textContent = 'Idle';
      stopBtn.disabled = true;
      eventSource.close();
    } else if (data.error) {
      output.textContent += `\n[ERROR] ${data.error}\n`;
    }
  };

  eventSource.onerror = function() {
    eventSource.close();
  };
}

stopBtn.addEventListener('click', () => {
  fetch('/stop').then(() => {
    animTitle.textContent = 'Idle';
    stopBtn.disabled = true;
  });
});

// ESC to stop
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (!stopBtn.disabled) stopBtn.click();
  }
});