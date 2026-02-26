function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-button').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}

document.getElementById('resumeForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const resume = document.getElementById('resume').value;
  const jd = document.getElementById('jd').value;
  await analyzeResumes(resume, jd);
});

function setupFileUpload(dropZoneId, fileInputId) {
  const dropZone = document.getElementById(dropZoneId);
  const fileInput = document.getElementById(fileInputId);

  dropZone.addEventListener('click', () => fileInput.click());

  dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
  });

  dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
  });

  dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      updateFileInfo(fileInputId);
    }
  });

  fileInput.addEventListener('change', () => updateFileInfo(fileInputId));
}

function updateFileInfo(fileInputId) {
  const fileInput = document.getElementById(fileInputId);
  const infoId = fileInputId === 'resumeFile' ? 'resumeFileInfo' : 'jdFileInfo';
  const infoDiv = document.getElementById(infoId);

  if (fileInput.files.length > 0) {
    const file = fileInput.files[0];
    infoDiv.innerHTML = `<div class="file-info">✓ ${file.name} (${(file.size / 1024 / 1024).toFixed(2)}MB)</div>`;
  } else {
    infoDiv.innerHTML = '';
  }
}

setupFileUpload('resumeDropZone', 'resumeFile');
setupFileUpload('jdDropZone', 'jdFile');

async function uploadFile(fileInputId, endpoint) {
  const fileInput = document.getElementById(fileInputId);
  if (!fileInput.files.length) {
    throw new Error('No file selected');
  }

  const formData = new FormData();
  const fieldName = endpoint === '/upload-resume' ? 'resume' : 'jd';
  formData.append(fieldName, fileInput.files[0]);

  const response = await fetch(endpoint, {
    method: 'POST',
    body: formData
  });

  const data = await response.json();
  if (!response.ok) throw new Error(data.error);
  return data.text;
}

async function analyzeFromFiles() {
  const errorDiv = document.getElementById('fileError');
  const successDiv = document.getElementById('fileSuccess');
  errorDiv.innerHTML = '';
  successDiv.innerHTML = '';

  try {
    const resume = await uploadFile('resumeFile', '/upload-resume');
    const jd = await uploadFile('jdFile', '/upload-jd');

    successDiv.innerHTML = '<div class="success">✓ Files uploaded successfully!</div>';
    await analyzeResumes(resume, jd);
  } catch (err) {
    errorDiv.innerHTML = `<div class="error">✗ Error: ${err.message}</div>`;
  }
}

function clearFiles() {
  document.getElementById('resumeFile').value = '';
  document.getElementById('jdFile').value = '';
  document.getElementById('resumeFileInfo').innerHTML = '';
  document.getElementById('jdFileInfo').innerHTML = '';
  document.getElementById('fileError').innerHTML = '';
  document.getElementById('fileSuccess').innerHTML = '';
}

async function analyzeResumes(resume, jd) {
  document.getElementById('initialState').style.display = 'none';
  document.getElementById('resultsContainer').style.display = 'block';

  try {
    const response = await fetch('/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ resume, jd })
    });

    const data = await response.json();

    if (data.results) {
      const r = data.results;
      document.getElementById('keywordScore').textContent = r.keyword_score.toFixed(0);
      document.getElementById('semanticScore').textContent = r.semantic_score.toFixed(0);
      document.getElementById('formatScore').textContent = r.format_score.toFixed(0);
      document.getElementById('bulletScore').textContent = r.bullet_score.toFixed(0);
      document.getElementById('finalScore').textContent = r.final_score.toFixed(0);

      const pct = (r.final_score / 10000) * 100;
      document.getElementById('percentageMatch').textContent = pct.toFixed(1) + '%';

      document.getElementById('keywordBar').style.width = (r.keyword_score / 40) + '%';
      document.getElementById('semanticBar').style.width = (r.semantic_score / 30) + '%';
      document.getElementById('formatBar').style.width = (r.format_score / 20) + '%';
      document.getElementById('bulletBar').style.width = (r.bullet_score / 10) + '%';

      let badges = { excellent: '🟢 EXCELLENT', good: '🟡 GOOD', fair: '🟠 FAIR', poor: '🔴 POOR' };
      let badgeClass = pct >= 80 ? 'excellent' : pct >= 60 ? 'good' : pct >= 40 ? 'fair' : 'poor';
      document.getElementById('assessment').textContent = badges[badgeClass];
      document.getElementById('assessment').className = 'assessment-badge ' + badgeClass;
    }

    if (data.ai_suggestions) {
      let html = JSON.stringify(data.ai_suggestions, null, 2);
      document.getElementById('suggestions').textContent = html;
    }
  } catch (err) {
    alert('Error: ' + err.message);
  }
}

