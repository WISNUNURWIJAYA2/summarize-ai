//  Config 
const API_BASE = 'http://127.0.0.1:8000';
const MAX_FILE_BYTES = 20 * 1024 * 1024;
const ALLOWED_EXT = ['.pdf', '.docx', '.txt'];

//  DOM refs 
const dropZone       = document.getElementById('drop-zone');
const fileInput      = document.getElementById('file-input');
const fileBadge      = document.getElementById('file-badge');
const fileNameEl     = document.getElementById('file-name-display');
const fileSizeEl     = document.getElementById('file-size-display');
const btnRemoveFile  = document.getElementById('btn-remove-file');
const errorBox       = document.getElementById('error-box');
const errorMsg       = document.getElementById('error-msg');
const btnSummarize   = document.getElementById('btn-summarize');
const loadingPanel   = document.getElementById('loading-panel');
const loadingSteps   = document.querySelectorAll('.loading-step');
const resultPanel    = document.getElementById('result-panel');
const summaryText    = document.getElementById('summary-text');
const resultMeta     = document.getElementById('result-meta');
const ratioChip      = document.getElementById('ratio-chip');
const btnCopy        = document.getElementById('btn-copy');
const btnDownloadPdf = document.getElementById('btn-download-pdf');
const btnNew         = document.getElementById('btn-new');
const progressWrap   = document.getElementById('progress-wrap');
const progressFill   = document.getElementById('progress-fill');
const toastEl        = document.getElementById('toast-msg');

//  State 
let currentFile    = null;
let lastPdfUrl     = null;
let lastSummaryTxt = '';
let stepTimer      = null;

//  Helpers 
function formatBytes(b) {
  if (b < 1024) return b + ' B';
  if (b < 1024 ** 2) return (b / 1024).toFixed(1) + ' KB';
  return (b / 1024 ** 2).toFixed(1) + ' MB';
}

function showError(msg) {
  errorMsg.textContent = msg;
  errorBox.classList.add('show');
}

function clearError() {
  errorBox.classList.remove('show');
}

function showToast(msg, duration = 2200) {
  toastEl.textContent = msg;
  toastEl.classList.add('show');
  setTimeout(() => toastEl.classList.remove('show'), duration);
}

function getSelectedRatio() {
  const checked = document.querySelector('input[name="ratio"]:checked');
  return checked ? parseInt(checked.value) : 30;
}

//  File handling 
function validateFile(file) {
  const ext = '.' + file.name.split('.').pop().toLowerCase();
  if (!ALLOWED_EXT.includes(ext)) return 'Format tidak didukung. Gunakan: PDF, DOCX, atau TXT.';
  if (file.size === 0) return 'Dokumen kosong. Pilih file yang valid.';
  if (file.size > MAX_FILE_BYTES) return `File terlalu besar. Maksimal ${formatBytes(MAX_FILE_BYTES)}.`;
  return null;
}

function setFile(file) {
  const err = validateFile(file);
  if (err) { showError(err); return; }
  clearError();
  currentFile = file;
  fileNameEl.textContent = file.name;
  fileSizeEl.textContent = formatBytes(file.size);
  fileBadge.classList.add('show');
  dropZone.classList.add('has-file');
  dropZone.querySelector('.dz-title').textContent = 'File siap diunggah';
  dropZone.querySelector('.dz-sub').textContent = 'Klik atau seret untuk mengganti';
  btnSummarize.disabled = false;
  hideResult();
}

function clearFile() {
  currentFile = null;
  fileInput.value = '';
  fileBadge.classList.remove('show');
  dropZone.classList.remove('has-file');
  dropZone.querySelector('.dz-title').textContent = 'Seret file ke sini atau klik untuk memilih';
  dropZone.querySelector('.dz-sub').textContent = 'PDF, DOCX, TXT · Maks. 20 MB';
  btnSummarize.disabled = true;
  clearError();
  hideResult();
}

//  Drop zone events 
dropZone.addEventListener('click', () => fileInput.click());
dropZone.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') fileInput.click(); });
fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });
btnRemoveFile.addEventListener('click', e => { e.stopPropagation(); clearFile(); });

dropZone.addEventListener('dragover',  e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  const f = e.dataTransfer.files[0];
  if (f) setFile(f);
});

//  Ratio selector 
document.querySelectorAll('.ratio-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.ratio-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    btn.querySelector('input[type=radio]').checked = true;
  });
});

//  Loading animation 
const STEP_DELAYS = [0, 1200, 2800, 5000];

function startLoadingAnim() {
  loadingSteps.forEach(s => s.classList.remove('active', 'done'));

  function activateStep(i) {
    if (i > 0) loadingSteps[i - 1].classList.replace('active', 'done');
    if (i < loadingSteps.length) loadingSteps[i].classList.add('active');
  }

  activateStep(0);
  stepTimer = [1, 2, 3].map(i => setTimeout(() => activateStep(i), STEP_DELAYS[i]));

  progressWrap.classList.add('show');
  progressFill.style.width = '0%';
  const startTime = performance.now();

  function tick() {
    const pct = Math.min(92, ((performance.now() - startTime) / 8000) * 92);
    progressFill.style.width = pct + '%';
    if (pct < 92) requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);
}

function finishLoadingAnim() {
  if (stepTimer) stepTimer.forEach(clearTimeout);
  loadingSteps.forEach(s => s.classList.add('done'));
  progressFill.style.width = '100%';
  setTimeout(() => progressWrap.classList.remove('show'), 600);
}

//  Show/hide result 
function showResult(data) {
  const ratioPct = getSelectedRatio();

  lastSummaryTxt = data.summary || '(Tidak ada ringkasan yang dihasilkan)';
  summaryText.textContent = lastSummaryTxt;

  ratioChip.innerHTML = `<b>${ratioPct}%</b>`;

  const chips = [];
  if (data.original_words) chips.push(`<span class="meta-chip"><i class="bi bi-file-text" style="font-size:.9rem"></i> ${data.original_words} kata asli</span>`);
  if (data.summary_words)  chips.push(`<span class="meta-chip"><i class="bi bi-scissors" style="font-size:.9rem"></i> ${data.summary_words} kata ringkasan</span>`);
  if (data.processing_time) chips.push(`<span class="meta-chip"><i class="bi bi-clock" style="font-size:.9rem"></i> ${data.processing_time}s</span>`);
  resultMeta.innerHTML = chips.join('');

  if (data.downloads?.pdf) {
    lastPdfUrl = `${API_BASE}/documents/download/pdf/${data.downloads.pdf}`;
    btnDownloadPdf.style.display = '';
  } else {
    lastPdfUrl = null;
    btnDownloadPdf.style.display = 'none';
  }

  resultPanel.style.display = 'block';
  requestAnimationFrame(() => {
    requestAnimationFrame(() => resultPanel.classList.add('show', 'visible'));
  });
  resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResult() {
  resultPanel.classList.remove('show', 'visible');
  lastPdfUrl = null;
  lastSummaryTxt = '';
}

//  API error mapper
function mapApiError(err) {
  const code = err?.detail?.code || err?.code || '';
  const msg  = err?.detail?.message || err?.message || '';
  const map  = {
    FILE_NOT_SUPPORTED: 'Format file tidak didukung.',
    WRONG_RATIO:        'Rasio ringkasan tidak valid.',
    EMPTY_DOCUMENT:     'Dokumen kosong. Pastikan file memiliki konten teks.',
    MODEL_ERROR:        'Model MT5 mengalami kesalahan. Coba beberapa saat lagi.',
    OOM:                'RAM tidak mencukupi. Coba file yang lebih kecil.',
  };
  return map[code] || msg || 'Terjadi kesalahan. Silakan coba lagi.';
}

//  Submit 
btnSummarize.addEventListener('click', async (e) => {
  e.preventDefault();
  e.stopPropagation();
  if (!currentFile) return;

  clearError();
  hideResult();
  btnSummarize.disabled = true;
  loadingPanel.classList.add('show');
  startLoadingAnim();

  const fd = new FormData();
  fd.append('file', currentFile);
  fd.append('ratio', getSelectedRatio());

  try {
    const res  = await fetch(`${API_BASE}/documents/summarize`, { method: 'POST', body: fd });
    const data = await res.json();

    if (!res.ok) {
      finishLoadingAnim();
      setTimeout(() => {
        loadingPanel.classList.remove('show');
        showError(mapApiError(data));
        btnSummarize.disabled = false;
      }, 500);
      return;
    }

    finishLoadingAnim();
    setTimeout(() => {
      loadingPanel.classList.remove('show');
      progressFill.style.width = '0%';
      showResult(data);
      showToast('Ringkasan berhasil dibuat!');
      btnSummarize.disabled = false;
    }, 500);

  } catch (err) {
    finishLoadingAnim();
    setTimeout(() => {
      loadingPanel.classList.remove('show');
      showError(
        err instanceof TypeError && err.message.includes('fetch')
          ? 'Tidak dapat terhubung ke server. Pastikan backend berjalan.'
          : 'Terjadi kesalahan tidak terduga.'
      );
      btnSummarize.disabled = false;
    }, 500);
  }
});

//  Copy
btnCopy.addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(lastSummaryTxt);
    btnCopy.classList.add('copied');
    btnCopy.innerHTML = '<i class="bi bi-clipboard-check"></i> Tersalin!';
    showToast('Teks berhasil disalin');
    setTimeout(() => {
      btnCopy.classList.remove('copied');
      btnCopy.innerHTML = '<i class="bi bi-clipboard"></i> Salin';
    }, 2500);
  } catch {
    showToast('Gagal menyalin. Salin manual dari kotak teks.');
  }
});

//  Download PDF 
btnDownloadPdf.addEventListener('click', () => {
  if (!lastPdfUrl) return;
  window.open(lastPdfUrl, '_blank');
});

//  New document 
btnNew.addEventListener('click', () => {
  clearFile();
  hideResult();
  window.scrollTo({ top: 0, behavior: 'smooth' });
});

//  Reduced motion 
if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  document.querySelectorAll('.spinner-ring, .step-dot').forEach(el => {
    el.style.animation = 'none';
  });
}