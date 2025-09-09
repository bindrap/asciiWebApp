// static/script.js - Debug version
console.log('🎨 Script loaded successfully!');

const output = document.getElementById('output');
const animTitle = document.getElementById('anim-title');
const stopBtn = document.getElementById('stop-btn');
const slideshowBtn = document.getElementById('slideshow-btn');
const randomBtn = document.getElementById('random-btn');
const testBtn = document.getElementById('test-btn');

let eventSource = null;
let isSlideshow = false;

// Check if all elements exist
console.log('Elements found:', {
  output: !!output,
  animTitle: !!animTitle,
  stopBtn: !!stopBtn,
  slideshowBtn: !!slideshowBtn,
  randomBtn: !!randomBtn,
  testBtn: !!testBtn
});

function startAnimation(key) {
  console.log('🚀 Starting animation:', key);
  setLoadingState(true);
  
  fetch(`/start/${key}`)
    .then(res => {
      console.log('Response received:', res.status);
      return res.json();
    })
    .then(data => {
      console.log('Response data:', data);
      if (data.error) {
        alert(data.error);
        setLoadingState(false);
        return;
      }
      animTitle.textContent = data.animation;
      stopBtn.disabled = false;
      slideshowBtn.disabled = true;
      output.textContent = 'Starting animation...\n';
      startStream();
    })
    .catch(err => {
      console.error('❌ Error starting animation:', err);
      setLoadingState(false);
      alert('Error starting animation: ' + err.message);
    });
}

function startSlideshow() {
  console.log('🎬 Starting slideshow');
  setLoadingState(true);
  
  fetch('/slideshow')
    .then(res => {
      console.log('Slideshow response received:', res.status);
      return res.json();
    })
    .then(data => {
      console.log('Slideshow response data:', data);
      if (data.error) {
        alert(data.error);
        setLoadingState(false);
        return;
      }
      animTitle.textContent = '🎬 ' + data.animation;
      stopBtn.disabled = false;
      slideshowBtn.disabled = true;
      output.textContent = 'Starting slideshow...\n';
      startStream();
    })
    .catch(err => {
      console.error('❌ Error starting slideshow:', err);
      setLoadingState(false);
      alert('Error starting slideshow: ' + err.message);
    });
}

function startTest() {
  console.log('🧪 Starting test');
  setLoadingState(true);
  
  fetch('/test')
    .then(res => {
      console.log('Test response received:', res.status);
      return res.json();
    })
    .then(data => {
      console.log('Test response data:', data);
      animTitle.textContent = 'Test Animation';
      stopBtn.disabled = false;
      slideshowBtn.disabled = true;
      output.textContent = 'Starting test...\n';
      startStream();
    })
    .catch(err => {
      console.error('❌ Error starting test:', err);
      setLoadingState(false);
      alert('Error starting test: ' + err.message);
    });
}

function startStream() {
  console.log('📡 Starting event stream');
  
  if (eventSource) {
    console.log('Closing existing stream');
    eventSource.close();
  }
  
  eventSource = new EventSource('/stream');
  
  eventSource.onopen = function(event) {
    console.log('✅ Stream connected');
  };

  eventSource.onmessage = function(event) {
    console.log('📨 Stream message:', event.data);
    
    try {
      const data = JSON.parse(event.data);
      console.log('📦 Parsed data:', data);
      
      if (data.type === 'start') {
        output.textContent = '';
        setLoadingState(false);
        console.log('🎬 Animation started:', data.name);
      } else if (data.type === 'clear') {
        output.textContent = '';
        console.log('🧹 Screen cleared');
      } else if (data.type === 'line') {
        output.textContent += data.data + '\n';
        output.scrollTop = output.scrollHeight;
        console.log('📝 Line added:', data.data.substring(0, 50) + '...');
      } else if (data.type === 'slideshow_next') {
        output.textContent = '';
        output.textContent += `\n🎬 Now Playing: ${data.name}\n\n`;
        output.scrollTop = output.scrollHeight;
        animTitle.textContent = `🎬 Slideshow - ${data.name}`;
        console.log('🎬 Slideshow next:', data.name);
      } else if (data.type === 'done' || data.type === 'stream_end') {
        animTitle.textContent = 'Idle';
        stopBtn.disabled = true;
        slideshowBtn.disabled = false;
        setLoadingState(false);
        if (eventSource) {
          eventSource.close();
          eventSource = null;
        }
        console.log('✅ Animation done');
      } else if (data.type === 'error') {
        output.textContent += `\n❌ [ERROR] ${data.message}\n`;
        output.scrollTop = output.scrollHeight;
        console.error('❌ Animation error:', data.message);
      } else {
        console.log('❓ Unknown message type:', data);
      }
    } catch (e) {
      console.error('❌ Error parsing stream data:', e, 'Raw data:', event.data);
    }
  };

  eventSource.onerror = function(error) {
    console.error('❌ EventSource error:', error);
    setLoadingState(false);
    animTitle.textContent = 'Connection Error';
    stopBtn.disabled = true;
    slideshowBtn.disabled = false;
    if (eventSource) {
      eventSource.close();
      eventSource = null;
    }
  };
}

function setLoadingState(loading) {
  console.log('Loading state:', loading);
  const buttons = document.querySelectorAll('button');
  const links = document.querySelectorAll('.anim-link');
  
  if (loading) {
    animTitle.innerHTML = '<span class="loading"></span> Loading...';
    buttons.forEach(btn => btn.disabled = true);
    links.forEach(link => link.style.pointerEvents = 'none');
  } else {
    links.forEach(link => link.style.pointerEvents = 'auto');
  }
}

function stopAnimation() {
  console.log('🛑 Stopping animation');
  fetch('/stop')
    .then(res => res.json())
    .then(() => {
      animTitle.textContent = 'Idle';
      stopBtn.disabled = true;
      slideshowBtn.disabled = false;
      isSlideshow = false;
      if (eventSource) {
        eventSource.close();
        eventSource = null;
      }
      console.log('✅ Animation stopped');
    })
    .catch(err => {
      console.error('❌ Error stopping animation:', err);
    });
}

// Set up event listeners
document.addEventListener('DOMContentLoaded', function() {
  console.log('🌟 DOM loaded, setting up event listeners');
  
  // Animation links
  document.querySelectorAll('.anim-link').forEach((link, index) => {
    console.log(`Setting up listener for animation ${index + 1}`);
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const key = e.target.dataset.key;
      console.log('🎯 Animation link clicked:', key);
      isSlideshow = false;
      startAnimation(key);
    });
  });

  // Button listeners
  if (randomBtn) {
    randomBtn.addEventListener('click', () => {
      console.log('🎲 Random button clicked');
      const links = document.querySelectorAll('.anim-link');
      const randomLink = links[Math.floor(Math.random() * links.length)];
      const key = randomLink.dataset.key;
      console.log('🎲 Selected random animation:', key);
      isSlideshow = false;
      startAnimation(key);
    });
  }

  if (slideshowBtn) {
    slideshowBtn.addEventListener('click', () => {
      console.log('🎬 Slideshow button clicked');
      isSlideshow = true;
      startSlideshow();
    });
  }

  if (testBtn) {
    testBtn.addEventListener('click', () => {
      console.log('🧪 Test button clicked');
      startTest();
    });
  }

  if (stopBtn) {
    stopBtn.addEventListener('click', stopAnimation);
  }

  // ESC key listener
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      console.log('⎋ ESC key pressed');
      if (!stopBtn.disabled) {
        stopAnimation();
      }
    }
  });

  console.log('✅ All event listeners set up');
  animTitle.textContent = 'Ready';
});

console.log('📜 Script file loaded completely');