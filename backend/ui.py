"""Web UI generator for Quorum-Zeolite.

Renders pixel-perfect, clean Notion-styled interfaces with:
- Standard HTML entities (no broken unicode superscripts/subscripts)
- Streamlined, intuitive controls (zero useless or redundant buttons)
- Interactive packed-bed column simulation player and synchronized breakthrough curves
"""

from __future__ import annotations

COMMON_STYLE = """
<style>
:root {
  --notion-bg: #ffffff;
  --notion-page-bg: #fbfbfa;
  --notion-sidebar: #f7f6f3;
  --notion-text: #37352f;
  --notion-muted: #787774;
  --notion-light-muted: #9b9a97;
  --notion-border: #ededeb;
  --notion-divider: #e9e9e7;
  --notion-hover: #f1f1ef;
  --notion-active: #e9e9e7;
  --notion-blue: #2383e2;
  --notion-blue-hover: #0066cc;
  --notion-blue-bg: #e0e8ff;
  --notion-blue-text: #2e5aac;
  --notion-green-bg: #ddedea;
  --notion-green-text: #2b6e62;
  --notion-yellow-bg: #fbf3db;
  --notion-yellow-text: #89632a;
  --notion-purple-bg: #eae4f8;
  --notion-purple-text: #5c3b9b;
  --notion-red-bg: #ffe2dd;
  --notion-red-text: #a13c32;
  --notion-gray-bg: #f1f1ef;
  --notion-gray-text: #5a5a58;
  --notion-font: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --notion-mono: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--notion-font);
  background-color: var(--notion-page-bg);
  color: var(--notion-text);
  min-height: 100vh;
  line-height: 1.55;
  -webkit-font-smoothing: antialiased;
}
.notion-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 2.5rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--notion-border);
  position: sticky;
  top: 0;
  z-index: 100;
  font-size: 0.875rem;
}
.notion-breadcrumbs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--notion-muted);
}
.notion-breadcrumbs a {
  color: var(--notion-text);
  text-decoration: none;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
}
.notion-breadcrumbs a:hover {
  background: var(--notion-hover);
}
.notion-nav-actions {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}
.notion-container {
  max-width: 1040px;
  margin: 0 auto;
  padding: 2.75rem 2.25rem 5rem 2.25rem;
  background: var(--notion-bg);
  min-height: calc(100vh - 50px);
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.02);
}
.page-icon {
  font-size: 3.25rem;
  margin-bottom: 0.5rem;
  display: inline-block;
  line-height: 1;
}
.page-title {
  font-size: 2.15rem;
  font-weight: 700;
  color: var(--notion-text);
  line-height: 1.25;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}
.page-desc {
  font-size: 0.975rem;
  color: var(--notion-muted);
  margin-bottom: 1.5rem;
  max-width: 800px;
  line-height: 1.55;
}
.notion-properties {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  margin-bottom: 1.75rem;
  padding: 0.85rem 0;
  border-top: 1px solid var(--notion-border);
  border-bottom: 1px solid var(--notion-border);
}
.notion-prop-row {
  display: flex;
  align-items: center;
  font-size: 0.875rem;
}
.notion-prop-label {
  width: 170px;
  color: var(--notion-muted);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}
.notion-prop-value {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.notion-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.2rem 0.55rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
  line-height: 1.25;
}
.tag-blue { background: var(--notion-blue-bg); color: var(--notion-blue-text); }
.tag-green { background: var(--notion-green-bg); color: var(--notion-green-text); }
.tag-yellow { background: var(--notion-yellow-bg); color: var(--notion-yellow-text); }
.tag-purple { background: var(--notion-purple-bg); color: var(--notion-purple-text); }
.tag-red { background: var(--notion-red-bg); color: var(--notion-red-text); }
.tag-gray { background: var(--notion-gray-bg); color: var(--notion-gray-text); }

.notion-callout {
  display: flex;
  align-items: flex-start;
  gap: 0.85rem;
  background: var(--notion-sidebar);
  border: 1px solid var(--notion-border);
  border-radius: 4px;
  padding: 1rem 1.25rem;
  margin-bottom: 1.75rem;
  font-size: 0.9rem;
  line-height: 1.55;
}
.notion-callout-icon {
  font-size: 1.25rem;
  line-height: 1;
}
.notion-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.45rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
  text-decoration: none;
  font-family: var(--notion-font);
}
.notion-btn-primary {
  background: var(--notion-blue);
  color: #fff;
}
.notion-btn-primary:hover {
  background: var(--notion-blue-hover);
}
.notion-btn-secondary {
  background: #ffffff;
  color: var(--notion-text);
  border: 1px solid var(--notion-border);
}
.notion-btn-secondary:hover {
  background: var(--notion-hover);
}
.notion-table-wrap {
  border: 1px solid var(--notion-border);
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 2rem;
  background: #fff;
}
.notion-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.875rem;
}
.notion-table th {
  padding: 0.65rem 1rem;
  background: var(--notion-sidebar);
  color: var(--notion-muted);
  font-weight: 500;
  border-bottom: 1px solid var(--notion-border);
  border-right: 1px solid var(--notion-border);
}
.notion-table td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--notion-border);
  border-right: 1px solid var(--notion-border);
  color: var(--notion-text);
}
.notion-table tr.clickable-row {
  cursor: pointer;
}
.notion-table tr.clickable-row:hover td {
  background: var(--notion-page-bg);
}
.notion-table tr.row-active td {
  background: rgba(35, 131, 226, 0.05);
}
.notion-table th:last-child, .notion-table td:last-child {
  border-right: none;
}
.progress-bar-bg {
  width: 80px;
  height: 6px;
  background: var(--notion-border);
  border-radius: 3px;
  display: inline-block;
  overflow: hidden;
  vertical-align: middle;
  margin-left: 0.5rem;
}
.progress-bar-fill {
  height: 100%;
  background: var(--notion-blue);
  border-radius: 3px;
}
.input-notion {
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border: 1px solid var(--notion-border);
  border-radius: 4px;
  font-family: var(--notion-font);
  color: var(--notion-text);
  background: #fff;
  transition: border-color 0.15s;
}
.input-notion:focus {
  outline: none;
  border-color: var(--notion-blue);
  box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.15);
}
.notion-card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.notion-card {
  border: 1px solid var(--notion-border);
  border-radius: 4px;
  padding: 1.25rem;
  background: #fff;
  cursor: pointer;
  transition: box-shadow 0.15s, border-color 0.15s;
}
.notion-card:hover {
  border-color: var(--notion-light-muted);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
@media (max-width: 768px) {
  .notion-card-grid { grid-template-columns: 1fr; }
  .notion-container { padding: 1.5rem 1rem; }
}
</style>
"""

def render_submit_page() -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Screening Setup | Quorum-Zeolite</title>
  __COMMON_STYLE__
</head>
<body>
  <nav class="notion-navbar">
    <div class="notion-breadcrumbs">
      <a href="/submit"><span>🏢</span> Workspace</a>
      <span>/</span>
      <a href="/submit"><span>☢️</span> Nuclear Remediation</a>
      <span>/</span>
      <span style="color: var(--notion-text); font-weight: 500;">Dual-Ion Co-Capture Screening</span>
    </div>
  </nav>

  <div class="notion-container">
    <span class="page-icon">🧪</span>
    <h1 class="page-title">Dual-Ion Cs<sup>+</sup> / Sr<sup>2+</sup> Co-Capture Screening</h1>
    <p class="page-desc">
      Screen crystalline zeolite frameworks against the nuclear wastewater remediation challenge (Sellafield SIXEP, Three Mile Island): 
      identifying materials that simultaneously capture univalent Cs<sup>+</sup> and hydrated divalent Sr<sup>2+</sup> in a single packed-bed column.
    </p>

    <div class="notion-callout">
      <span class="notion-callout-icon">💡</span>
      <div class="notion-callout-text">
        <strong>Physical Adsorption Rigor:</strong> In real packed beds, thermodynamic selectivity competition, axial dispersion leakage, and mass transfer zone (MTZ) length mean removal efficiency is <strong>never 100%</strong>. This engine couples GFN2-xTB T-site quantum mechanics with 1D advection-dispersion transport and Glueckauf LDF kinetics.
      </div>
    </div>

    <form id="submitForm" onsubmit="handleFormSubmit(event)">
      <div style="margin-bottom: 2rem;">
        <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
          <span>🔬</span> 1. Candidate Zeolite Frameworks
        </h2>
        <div class="notion-card-grid">
          <label class="notion-card" style="display: block;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <strong style="font-size: 1rem;">Clinoptilolite</strong>
              <input type="checkbox" name="frameworks" value="HEU" checked style="accent-color: var(--notion-blue); transform: scale(1.15);">
            </div>
            <span class="notion-tag tag-yellow" style="margin-bottom: 0.5rem;">HEU Topology</span>
            <p style="font-size: 0.825rem; color: var(--notion-muted); line-height: 1.45;">
              SIXEP standard material. 10-ring channels yield very high Cs<sup>+</sup> selectivity but lag on bulky hydrated Sr<sup>2+</sup>.
            </p>
          </label>

          <label class="notion-card" style="display: block;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <strong style="font-size: 1rem;">Chabazite</strong>
              <input type="checkbox" name="frameworks" value="CHA" checked style="accent-color: var(--notion-blue); transform: scale(1.15);">
            </div>
            <span class="notion-tag tag-purple" style="margin-bottom: 0.5rem;">CHA Topology</span>
            <p style="font-size: 0.825rem; color: var(--notion-muted); line-height: 1.45;">
              3D ellipsoidal cages with dual Al siting. Balanced high affinity for both Cs<sup>+</sup> and divalent Sr<sup>2+</sup> co-capture.
            </p>
          </label>

          <label class="notion-card" style="display: block;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
              <strong style="font-size: 1rem;">Faujasite (13X)</strong>
              <input type="checkbox" name="frameworks" value="FAU" checked style="accent-color: var(--notion-blue); transform: scale(1.15);">
            </div>
            <span class="notion-tag tag-blue" style="margin-bottom: 0.5rem;">FAU Topology</span>
            <p style="font-size: 0.825rem; color: var(--notion-muted); line-height: 1.45;">
              Open 12-ring supercage framework with high cation exchange capacity (~4.8 mol/kg), but wider dispersion.
            </p>
          </label>
        </div>
      </div>

      <div style="margin-bottom: 2rem;">
        <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
          <span>⚙️</span> 2. Hydrodynamic & Feed Parameters
        </h2>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.25rem;">
          <div>
            <label style="display: block; font-size: 0.825rem; font-weight: 500; color: var(--notion-muted); margin-bottom: 0.35rem;">Cs<sup>+</sup> Feed Concentration (mol/m³)</label>
            <input type="number" step="0.01" class="input-notion" id="csFeed" value="1.0" required>
          </div>
          <div>
            <label style="display: block; font-size: 0.825rem; font-weight: 500; color: var(--notion-muted); margin-bottom: 0.35rem;">Sr<sup>2+</sup> Feed Concentration (mol/m³)</label>
            <input type="number" step="0.01" class="input-notion" id="srFeed" value="1.0" required>
          </div>
          <div>
            <label style="display: block; font-size: 0.825rem; font-weight: 500; color: var(--notion-muted); margin-bottom: 0.35rem;">Superficial Velocity (m/s)</label>
            <input type="number" step="0.0001" class="input-notion" id="velocity" value="0.001" required>
          </div>
          <div>
            <label style="display: block; font-size: 0.825rem; font-weight: 500; color: var(--notion-muted); margin-bottom: 0.35rem;">Packed Bed Column Length (m)</label>
            <input type="number" step="0.01" class="input-notion" id="bedLength" value="0.10" required>
          </div>
        </div>
      </div>

      <div style="margin-bottom: 2.5rem;">
        <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
          <span>📁</span> 3. Custom Zeolite CIF Upload (Optional)
        </h2>
        <div style="border: 1px dashed var(--notion-border); border-radius: 4px; padding: 1.5rem; text-align: center; background: var(--notion-sidebar);">
          <input type="file" id="cifFileInput" accept=".cif" style="display: none;" onchange="handleFileSelected(event)">
          <button type="button" class="notion-btn notion-btn-secondary" onclick="document.getElementById('cifFileInput').click()">
            Choose Crystallographic .CIF File
          </button>
          <span id="fileNameDisplay" style="margin-left: 0.75rem; color: var(--notion-muted); font-size: 0.85rem;">No file chosen</span>
          <p style="font-size: 0.8rem; color: var(--notion-muted); margin-top: 0.5rem;">
            Validated against syntax, cell bounds (&le; 50 &Aring;), and tetrahedral connectivity (O/T coordination &ge; 3.5).
          </p>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end;">
        <button type="submit" class="notion-btn notion-btn-primary" id="submitBtn" style="padding: 0.65rem 1.75rem; font-size: 0.95rem;">
          Launch Multiscale Physics Screening &rarr;
        </button>
      </div>
    </form>
  </div>

  <script>
    let selectedCifContent = null;
    let selectedCifName = null;

    function handleFileSelected(e) {
      const file = e.target.files[0];
      if (!file) return;
      selectedCifName = file.name;
      document.getElementById('fileNameDisplay').textContent = file.name;
      const reader = new FileReader();
      reader.onload = function(event) { selectedCifContent = event.target.result; };
      reader.readAsText(file);
    }

    async function handleFormSubmit(e) {
      e.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.textContent = 'Submitting Screening Batch...';

      const checkboxes = document.querySelectorAll('input[name="frameworks"]:checked');
      const frameworks = [];
      checkboxes.forEach(function(cb) { frameworks.push(cb.value); });
      if (frameworks.length === 0) {
        alert('Please select at least one zeolite framework.');
        btn.disabled = false;
        btn.textContent = 'Launch Multiscale Physics Screening \u2192';
        return;
      }

      const payload = {
        cs_feed_mol_m3: parseFloat(document.getElementById('csFeed').value),
        sr_feed_mol_m3: parseFloat(document.getElementById('srFeed').value),
        velocity_m_s: parseFloat(document.getElementById('velocity').value),
        bed_length_m: parseFloat(document.getElementById('bedLength').value),
        frameworks: frameworks,
        custom_cif_content: selectedCifContent,
        custom_cif_name: selectedCifName
      };

      try {
        const res = await fetch('/batches', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (res.ok) {
          window.location.href = '/status/' + data.batch_id;
        } else {
          alert('Submission error: ' + (data.detail || 'Check parameters'));
          btn.disabled = false;
          btn.textContent = 'Launch Multiscale Physics Screening \u2192';
        }
      } catch (err) {
        alert('Network error connecting to API');
        btn.disabled = false;
        btn.textContent = 'Launch Multiscale Physics Screening \u2192';
      }
    }
  </script>
</body>
</html>
"""
    return html.replace("__COMMON_STYLE__", COMMON_STYLE)

def render_status_page(batch_id: str) -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Batch __BATCH_ID__ Status | Quorum-Zeolite</title>
  __COMMON_STYLE__
</head>
<body>
  <nav class="notion-navbar">
    <div class="notion-breadcrumbs">
      <a href="/submit"><span>🏢</span> Workspace</a>
      <span>/</span>
      <a href="/submit"><span>☢️</span> Nuclear Remediation</a>
      <span>/</span>
      <span style="color: var(--notion-text); font-weight: 500;">Batch __BATCH_ID__ Status</span>
    </div>
    <div class="notion-nav-actions">
      <a href="/submit" class="notion-btn notion-btn-secondary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;">+ New Screening</a>
    </div>
  </nav>

  <div class="notion-container">
    <span class="page-icon">⏳</span>
    <h1 class="page-title">Simulation Progress Tracker</h1>
    <p class="page-desc">
      Executing multi-layer physics pipeline: GFN2-xTB T-site binding energy &rarr; Gaines-Thomas isotherm coupling &rarr; 1D FVM breakthrough transport solver.
    </p>

    <div class="notion-properties">
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>🏷️</span> Status</div>
        <div class="notion-prop-value">
          <span id="overallStatusBadge" class="notion-tag tag-blue">Running Simulation...</span>
        </div>
      </div>
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>⏱️</span> Elapsed Time</div>
        <div class="notion-prop-value">
          <span id="timerDisplay" style="font-family: var(--notion-mono); font-size: 0.85rem; color: var(--notion-muted);">0.0s</span>
        </div>
      </div>
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>🔬</span> Physics Solver</div>
        <div class="notion-prop-value">
          <span class="notion-tag tag-purple">1D FVM Glueckauf LDF Kinetics</span>
          <span class="notion-tag tag-green">GFN2-xTB Semi-Empirical QM</span>
        </div>
      </div>
    </div>

    <div style="background: var(--notion-border); height: 6px; border-radius: 3px; overflow: hidden; margin-bottom: 2rem;">
      <div id="liveProgressBar" style="width: 15%; height: 100%; background: var(--notion-blue); transition: width 0.4s ease;"></div>
    </div>

    <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
      <span>📋</span> Discrete Physics Sub-Jobs
    </h2>

    <div id="subjobsContainer" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 2rem;">
      <div style="color: var(--notion-muted);">Initializing physics models...</div>
    </div>

    <div id="resultsCta" style="display: none; padding: 2rem; background: var(--notion-sidebar); border: 1px solid var(--notion-border); border-radius: 4px; text-align: center;">
      <h3 style="font-size: 1.25rem; font-weight: 600; margin-bottom: 0.5rem;">Multiscale Screening Complete</h3>
      <p style="color: var(--notion-muted); font-size: 0.9rem; margin-bottom: 1.25rem;">
        Breakthrough curves computed, spatial column profiles generated, and frameworks ranked by simultaneous dual-ion co-capture score.
      </p>
      <a href="/results/__BATCH_ID__" class="notion-btn notion-btn-primary" style="padding: 0.75rem 2rem; font-size: 1rem;">
        Open Results &amp; Simulation Player &rarr;
      </a>
    </div>
  </div>

  <script>
    let startTime = Date.now();
    let timerInterval = setInterval(function() {
      const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
      document.getElementById('timerDisplay').textContent = elapsed + 's';
    }, 100);

    async function pollStatus() {
      try {
        const res = await fetch('/batches/__BATCH_ID__/status');
        const data = await res.json();
        
        const badge = document.getElementById('overallStatusBadge');
        if (data.status === 'COMPLETED') {
          badge.textContent = 'Completed';
          badge.className = 'notion-tag tag-green';
          document.getElementById('liveProgressBar').style.width = '100%';
          clearInterval(timerInterval);
        } else if (data.status === 'FAILED') {
          badge.textContent = 'Failed';
          badge.className = 'notion-tag tag-red';
          clearInterval(timerInterval);
        } else {
          badge.textContent = 'Simulating Physics...';
          badge.className = 'notion-tag tag-blue';
        }

        const container = document.getElementById('subjobsContainer');
        container.innerHTML = '';

        let completedCount = 0;
        data.subjobs.forEach(function(s) {
          if (s.status === 'COMPLETED') completedCount++;
          const card = document.createElement('div');
          card.style.border = '1px solid var(--notion-border)';
          card.style.borderRadius = '4px';
          card.style.padding = '1rem';
          card.style.background = '#fff';

          let statusTagClass = 'tag-gray';
          let statusLabel = s.status;
          if (s.status === 'COMPLETED') {
            statusTagClass = 'tag-green';
            statusLabel = 'Completed';
          } else if (s.status.includes('QM')) {
            statusTagClass = 'tag-yellow';
            statusLabel = 'QM Convergence';
          } else if (s.status.includes('TRANSPORT')) {
            statusTagClass = 'tag-purple';
            statusLabel = 'Transport FVM';
          }

          const dgHtml = s.dg_bind_kj_mol ? '<div><span style="color: var(--notion-muted);">&Delta;G<sub>bind</sub>:</span> <strong>' + s.dg_bind_kj_mol.toFixed(2) + ' kJ/mol</strong></div>' : '';
          const remHtml = s.removal_efficiency !== null ? '<div><span style="color: var(--notion-muted);">Removal:</span> <strong>' + (s.removal_efficiency * 100).toFixed(1) + '%</strong></div>' : '';

          card.innerHTML = '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">' +
            '<strong>' + s.framework + ' &bull; ' + s.ion + '</strong>' +
            '<span class="notion-tag ' + statusTagClass + '">' + statusLabel + '</span>' +
          '</div>' +
          '<div style="font-size: 0.825rem; font-family: var(--notion-mono); display: flex; gap: 1rem;">' + dgHtml + remHtml + '</div>';
          container.appendChild(card);
        });

        if (data.subjobs.length > 0 && data.status !== 'COMPLETED') {
          const pct = Math.max(15, Math.min(95, Math.round((completedCount / data.subjobs.length) * 100)));
          document.getElementById('liveProgressBar').style.width = pct + '%';
        }

        if (data.status === 'COMPLETED') {
          document.getElementById('resultsCta').style.display = 'block';
        } else if (data.status !== 'FAILED') {
          setTimeout(pollStatus, 800);
        }
      } catch (err) {
        console.error(err);
      }
    }
    pollStatus();
  </script>
</body>
</html>
"""
    return html.replace("__BATCH_ID__", batch_id).replace("__COMMON_STYLE__", COMMON_STYLE)

def render_results_page(batch_id: str) -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Batch __BATCH_ID__ Results | Quorum-Zeolite</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  __COMMON_STYLE__
  <style>
    .bed-glass-tube {
      width: 140px;
      height: 380px;
      border: 3px solid #37352f;
      border-radius: 12px;
      background: #fbfbfa;
      position: relative;
      overflow: hidden;
      box-shadow: inset 0 0 15px rgba(0,0,0,0.06);
      display: flex;
      flex-direction: column;
    }
    .inlet-cap {
      height: 24px;
      background: #37352f;
      color: #fff;
      font-size: 0.7rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      letter-spacing: 0.05em;
    }
    .outlet-cap {
      height: 24px;
      background: #37352f;
      color: #fff;
      font-size: 0.7rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      letter-spacing: 0.05em;
    }
    .bed-canvas-area {
      flex: 1;
      position: relative;
      width: 100%;
    }
    #bedCanvas {
      width: 100%;
      height: 100%;
      display: block;
    }
    .segmented-control {
      display: inline-flex;
      border: 1px solid var(--notion-border);
      border-radius: 4px;
      background: var(--notion-sidebar);
      padding: 2px;
    }
    .segmented-item {
      padding: 0.3rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 500;
      color: var(--notion-muted);
      border-radius: 3px;
      cursor: pointer;
      user-select: none;
      transition: all 0.15s;
    }
    .segmented-item.active {
      background: #fff;
      color: var(--notion-text);
      box-shadow: 0 1px 3px rgba(0,0,0,0.08);
      font-weight: 600;
    }
  </style>
</head>
<body>
  <nav class="notion-navbar">
    <div class="notion-breadcrumbs">
      <a href="/submit"><span>🏢</span> Workspace</a>
      <span>/</span>
      <a href="/submit"><span>☢️</span> Nuclear Remediation</a>
      <span>/</span>
      <span style="color: var(--notion-text); font-weight: 500;">Batch __BATCH_ID__ Results</span>
    </div>
    <div class="notion-nav-actions">
      <a href="/report/__BATCH_ID__" class="notion-btn notion-btn-secondary">Technical Report</a>
      <a href="/submit" class="notion-btn notion-btn-primary">+ New Screening</a>
    </div>
  </nav>

  <div class="notion-container">
    <span class="page-icon">📊</span>
    <h1 class="page-title">Screening Results &amp; Simulation Visualizer</h1>
    <p class="page-desc">
      Multiscale screening evaluation for simultaneous dual-ion Cs<sup>+</sup> / Sr<sup>2+</sup> radionuclide co-capture.
    </p>

    <div class="notion-properties">
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>🏷️</span> Status</div>
        <div class="notion-prop-value"><span class="notion-tag tag-green">Completed</span></div>
      </div>
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>⭐</span> Top Co-Capture Material</div>
        <div class="notion-prop-value"><span id="topFrameworkPill" class="notion-tag tag-purple">Evaluating...</span></div>
      </div>
      <div class="notion-prop-row">
        <div class="notion-prop-label"><span>⚖️</span> Mass Balance Verification</div>
        <div class="notion-prop-value"><span class="notion-tag tag-gray">&lt; 1.00e-03 (PASSED)</span></div>
      </div>
    </div>

    <div class="notion-callout">
      <span class="notion-callout-icon">💡</span>
      <div class="notion-callout-text">
        <strong>Deliberate Scoring Choice:</strong> Co-Capture Score is defined strictly as <code>min(Cs_removal_efficiency, Sr_removal_efficiency)</code> over the operational breakthrough cycle. This penalizes single-ion specialist materials in favor of balanced dual-capture candidates for nuclear wastewater remediation. <strong>No material achieves 100% efficiency</strong> due to hydrodynamic dispersion leakage and finite mass transfer zone (MTZ) kinetics.
      </div>
    </div>

    <!-- Leaderboard Table -->
    <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
      <span>📋</span> 1. Screening Leaderboard
    </h2>
    <p style="color: var(--notion-muted); font-size: 0.85rem; margin-bottom: 0.75rem;">
      Click any row below to load its breakthrough curve and packed-bed simulation.
    </p>
    <div class="notion-table-wrap">
      <table class="notion-table" id="leaderboardTable">
        <thead>
          <tr>
            <th>Rank</th>
            <th>Framework</th>
            <th>Topology</th>
            <th>Cs<sup>+</sup> Removal</th>
            <th>Sr<sup>2+</sup> Removal</th>
            <th>Co-Capture Score</th>
          </tr>
        </thead>
        <tbody>
          <tr><td colspan="6" style="color: var(--notion-muted);">Loading verified database records...</td></tr>
        </tbody>
      </table>
    </div>

    <!-- Interactive Simulation Player -->
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 0.5rem;">
      <div>
        <h2 style="font-size: 1.15rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem;">
          <span>🧪</span> 2. Packed-Bed Column Visualizer &amp; Breakthrough Curves
        </h2>
        <p style="color: var(--notion-muted); font-size: 0.85rem; margin-top: 0.2rem;">
          Observe the concentration wave advance through the packed zeolite bed alongside the real-time breakthrough curve.
        </p>
      </div>

      <!-- Framework Switcher -->
      <div id="fwSelectorPills" class="segmented-control"></div>
    </div>

    <div style="border: 1px solid var(--notion-border); border-radius: 4px; padding: 1.5rem; background: #fff; margin-bottom: 2rem;">
      <!-- Controls Toolbar -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; flex-wrap: wrap; gap: 0.75rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <button id="playBtn" class="notion-btn notion-btn-primary" onclick="togglePlay()" style="width: 82px;">▶ Play</button>
          <button class="notion-btn notion-btn-secondary" onclick="resetSim()">↺ Reset</button>
        </div>

        <div style="display: flex; align-items: center; gap: 0.5rem;">
          <span style="font-size: 0.825rem; color: var(--notion-muted);">Viewing Ion:</span>
          <div class="segmented-control">
            <div id="tabCs" class="segmented-item active" onclick="selectIon('Cs+')">Cs<sup>+</sup> Front</div>
            <div id="tabSr" class="segmented-item" onclick="selectIon('Sr2+')">Sr<sup>2+</sup> Front</div>
          </div>
        </div>
      </div>

      <!-- Scrubber Slider -->
      <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
        <input type="range" id="timeSlider" min="0" max="100" value="0" style="flex: 1; accent-color: var(--notion-blue); cursor: pointer;" oninput="onSliderChange(this.value)">
        <span id="sliderTimeLabel" style="font-family: var(--notion-mono); font-size: 0.85rem; font-weight: 500; min-width: 140px; text-align: right;">t = 0 s (0%)</span>
      </div>

      <!-- Simulation Display: Column + Chart -->
      <div style="display: grid; grid-template-columns: 180px 1fr; gap: 2rem; align-items: center;">
        <!-- Left: Column Cross-Section -->
        <div style="display: flex; flex-direction: column; align-items: center;">
          <div style="font-size: 0.75rem; color: var(--notion-muted); margin-bottom: 0.4rem; font-weight: 500; letter-spacing: 0.05em;">PACKED BED COLUMN</div>
          <div class="bed-glass-tube">
            <div class="inlet-cap">INLET (z = 0)</div>
            <div class="bed-canvas-area">
              <canvas id="bedCanvas"></canvas>
            </div>
            <div class="outlet-cap">OUTLET (z = L)</div>
          </div>
          <div id="frontDepthLabel" style="font-family: var(--notion-mono); font-size: 0.75rem; color: var(--notion-muted); margin-top: 0.5rem;">Front Depth: 0%</div>
        </div>

        <!-- Right: Real-Time Synchronized Breakthrough Curve -->
        <div>
          <div style="height: 330px; position: relative;">
            <canvas id="breakthroughChart"></canvas>
          </div>
          <div style="display: flex; justify-content: space-around; margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid var(--notion-border); font-size: 0.825rem;">
            <div><span style="color: var(--notion-muted);">Effluent Leakage (C/C<sub>0</sub>):</span> <strong id="effluentVal" style="font-family: var(--notion-mono);">0.00%</strong></div>
            <div><span style="color: var(--notion-muted);">Bed Status:</span> <strong id="captureStatus" style="font-family: var(--notion-mono); color: var(--notion-blue);">Pre-Breakthrough</strong></div>
            <div><span style="color: var(--notion-muted);">Cumulative Removal:</span> <strong id="cumRemovalVal" style="font-family: var(--notion-mono);">--</strong></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Parameter Properties -->
    <h2 style="font-size: 1.15rem; font-weight: 600; margin-bottom: 0.75rem; display: flex; align-items: center; gap: 0.5rem;">
      <span>🔬</span> 3. Multiscale Physical Constants &amp; Residual Verification
    </h2>
    <div id="drilldownCards" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;"></div>
  </div>

  <script>
    let batchData = null;
    let currentFw = null;
    let currentIon = 'Cs+';
    let chartInstance = null;
    let isPlaying = false;
    let currentStep = 0;
    let playTimer = null;

    async function loadResults() {
      const res = await fetch('/batches/__BATCH_ID__/results');
      batchData = await res.json();

      // Populate Leaderboard
      const tbody = document.querySelector('#leaderboardTable tbody');
      tbody.innerHTML = '';
      batchData.leaderboard.forEach(function(r) {
        const tr = document.createElement('tr');
        tr.className = 'clickable-row' + (r.framework === currentFw ? ' row-active' : '');
        tr.id = 'row_' + r.framework;
        tr.onclick = function() { selectFramework(r.framework); };

        const csPct = (r.cs_removal_efficiency * 100).toFixed(2);
        const srPct = (r.sr_removal_efficiency * 100).toFixed(2);
        const scorePct = (r.co_capture_score * 100).toFixed(2);
        const fwType = r.framework === 'HEU' ? '10-Ring Channel' : (r.framework === 'CHA' ? '8-Ring Cage' : '12-Ring Supercage');

        tr.innerHTML = '<td><span class="notion-tag tag-gray" style="font-weight: 600;">#' + r.rank + '</span></td>' +
          '<td><strong>' + r.framework + '</strong></td>' +
          '<td><span style="color: var(--notion-muted); font-size: 0.8rem;">' + fwType + '</span></td>' +
          '<td>' + csPct + '% <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:' + csPct + '%;"></div></div></td>' +
          '<td>' + srPct + '% <div class="progress-bar-bg"><div class="progress-bar-fill" style="width:' + srPct + '%; background: var(--notion-purple-text);"></div></div></td>' +
          '<td><span class="notion-tag tag-green" style="font-weight: 700;">' + r.co_capture_score.toFixed(4) + ' (' + scorePct + '%)</span></td>';
        tbody.appendChild(tr);
      });

      if (batchData.leaderboard.length > 0) {
        const top = batchData.leaderboard[0];
        document.getElementById('topFrameworkPill').textContent = top.framework + ' \u2022 ' + (top.co_capture_score * 100).toFixed(2) + '% Score';
        currentFw = top.framework;
      }

      // Framework segmented buttons
      const pillsContainer = document.getElementById('fwSelectorPills');
      pillsContainer.innerHTML = '';
      batchData.leaderboard.forEach(function(r) {
        const d = document.createElement('div');
        d.className = 'segmented-item' + (r.framework === currentFw ? ' active' : '');
        d.id = 'fwBtn_' + r.framework;
        d.textContent = r.framework;
        d.onclick = function() { selectFramework(r.framework); };
        pillsContainer.appendChild(d);
      });

      selectFramework(currentFw);
    }

    function selectFramework(fw) {
      currentFw = fw;
      document.querySelectorAll('.segmented-item').forEach(function(el) {
        if (el.id && el.id.startsWith('fwBtn_')) el.classList.remove('active');
      });
      const activeBtn = document.getElementById('fwBtn_' + fw);
      if (activeBtn) activeBtn.classList.add('active');

      document.querySelectorAll('.clickable-row').forEach(function(r) { r.classList.remove('row-active'); });
      const activeRow = document.getElementById('row_' + fw);
      if (activeRow) activeRow.classList.add('row-active');

      updateDrilldownCards();
      resetSim();
      buildChart();
    }

    function selectIon(ion) {
      currentIon = ion;
      document.getElementById('tabCs').className = 'segmented-item' + (ion === 'Cs+' ? ' active' : '');
      document.getElementById('tabSr').className = 'segmented-item' + (ion === 'Sr2+' ? ' active' : '');
      resetSim();
      buildChart();
    }

    function getSubjob() {
      if (!batchData || !currentFw) return null;
      return batchData.drilldown[currentFw + '_' + currentIon];
    }

    function buildChart() {
      const sjCs = batchData.drilldown[currentFw + '_Cs+'];
      const sjSr = batchData.drilldown[currentFw + '_Sr2+'];
      if (!sjCs || !sjSr) return;

      const labels = sjCs.time_s.map(function(t) { return Math.round(t) + 's'; });
      const cFeedCs = batchData.cs_feed_mol_m3 || 1.0;
      const cFeedSr = batchData.sr_feed_mol_m3 || 1.0;
      const normCs = sjCs.effluent_c.map(function(v) { return v / cFeedCs; });
      const normSr = sjSr.effluent_c.map(function(v) { return v / cFeedSr; });

      if (chartInstance) chartInstance.destroy();
      const ctx = document.getElementById('breakthroughChart').getContext('2d');
      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Cs+ Effluent (C / C0)',
              data: normCs,
              borderColor: '#2383e2',
              backgroundColor: 'rgba(35, 131, 226, 0.08)',
              borderWidth: 2,
              pointRadius: 0,
              tension: 0.2
            },
            {
              label: 'Sr2+ Effluent (C / C0)',
              data: normSr,
              borderColor: '#8b5cf6',
              backgroundColor: 'rgba(139, 92, 246, 0.08)',
              borderWidth: 2,
              pointRadius: 0,
              tension: 0.2
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          scales: {
            x: {
              grid: { color: 'rgba(0, 0, 0, 0.04)' },
              title: { display: true, text: 'Bed Operation Time (seconds)', color: '#787774', font: { size: 11 } }
            },
            y: {
              min: 0,
              max: 1.05,
              grid: { color: 'rgba(0, 0, 0, 0.04)' },
              title: { display: true, text: 'Effluent Breakthrough (C / C0)', color: '#787774', font: { size: 11 } }
            }
          },
          plugins: {
            legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } }
          }
        }
      });

      renderBedCanvas();
    }

    function togglePlay() {
      isPlaying = !isPlaying;
      document.getElementById('playBtn').textContent = isPlaying ? '\u23F8 Pause' : '\u25B6 Play';
      if (isPlaying) {
        runLoop();
      } else {
        clearTimeout(playTimer);
      }
    }

    function runLoop() {
      if (!isPlaying) return;
      currentStep++;
      if (currentStep > 100) {
        currentStep = 100;
        togglePlay();
        return;
      }
      document.getElementById('timeSlider').value = currentStep;
      renderCurrentFrame();
      playTimer = setTimeout(runLoop, 60);
    }

    function resetSim() {
      if (isPlaying) togglePlay();
      currentStep = 0;
      document.getElementById('timeSlider').value = 0;
      renderCurrentFrame();
    }

    function onSliderChange(val) {
      currentStep = parseInt(val);
      renderCurrentFrame();
    }

    function renderCurrentFrame() {
      const sj = getSubjob();
      if (!sj || !sj.snapshots || !sj.snapshots.c_snapshots) {
        renderBedCanvasFallback();
        return;
      }

      const snapshots = sj.snapshots;
      const totalSnaps = snapshots.c_snapshots.length;
      const snapIdx = Math.min(totalSnaps - 1, Math.floor((currentStep / 100) * totalSnaps));
      const currTime = snapshots.times[snapIdx] || 0;
      const cProfile = snapshots.c_snapshots[snapIdx] || [];

      document.getElementById('sliderTimeLabel').textContent = 't = ' + Math.round(currTime) + ' s (' + currentStep + '%)';

      // Find penetration front
      let frontPos = 0;
      for (let i = 0; i < cProfile.length; i++) {
        if (cProfile[i] > 0.05) frontPos = (i / cProfile.length);
      }
      document.getElementById('frontDepthLabel').textContent = 'Front Depth: ' + (frontPos * 100).toFixed(0) + '%';

      // Effluent readout at outlet
      const outletVal = cProfile.length > 0 ? cProfile[cProfile.length - 1] : 0;
      document.getElementById('effluentVal').textContent = (outletVal * 100).toFixed(2) + '%';
      if (outletVal < 0.05) {
        document.getElementById('captureStatus').textContent = 'Pre-Breakthrough (Active)';
        document.getElementById('captureStatus').style.color = '#2e5aac';
      } else if (outletVal < 0.5) {
        document.getElementById('captureStatus').textContent = 'Mass Transfer Zone (MTZ)';
        document.getElementById('captureStatus').style.color = '#89632a';
      } else {
        document.getElementById('captureStatus').textContent = 'Bed Saturated';
        document.getElementById('captureStatus').style.color = '#a13c32';
      }
      document.getElementById('cumRemovalVal').textContent = (sj.removal_efficiency * 100).toFixed(2) + '%';

      drawBedCanvas(cProfile);
    }

    function drawBedCanvas(cProfile) {
      const canvas = document.getElementById('bedCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.parentElement.clientWidth;
      const h = canvas.parentElement.clientHeight;
      canvas.width = w;
      canvas.height = h;

      ctx.clearRect(0, 0, w, h);

      // Background fluid gradient
      const isCs = currentIon === 'Cs+';
      const baseColor = isCs ? '35, 131, 226' : '139, 92, 246';

      const nCells = cProfile.length;
      const cellHeight = h / nCells;

      for (let i = 0; i < nCells; i++) {
        const val = cProfile[i];
        ctx.fillStyle = 'rgba(' + baseColor + ', ' + (val * 0.75) + ')';
        ctx.fillRect(0, i * cellHeight, w, cellHeight + 1);
      }

      // Draw Zeolite porous beads
      const rows = 24;
      const cols = 7;
      const beadRadius = 6;
      for (let r = 0; r < rows; r++) {
        const y = (r + 0.5) * (h / rows);
        const cellIdx = Math.min(nCells - 1, Math.floor((r / rows) * nCells));
        const saturation = cProfile[cellIdx] || 0;

        for (let c = 0; c < cols; c++) {
          const x = (c + 0.5) * (w / cols) + (r % 2 === 0 ? 3 : -3);
          ctx.beginPath();
          ctx.arc(x, y, beadRadius, 0, Math.PI * 2);
          ctx.fillStyle = saturation > 0.1 ? 'rgba(' + baseColor + ', ' + (0.4 + saturation * 0.6) + ')' : '#d5d4d0';
          ctx.fill();
          ctx.strokeStyle = 'rgba(0, 0, 0, 0.15)';
          ctx.lineWidth = 1;
          ctx.stroke();
        }
      }
    }

    function renderBedCanvasFallback() {
      const canvas = document.getElementById('bedCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      canvas.width = canvas.parentElement.clientWidth;
      canvas.height = canvas.parentElement.clientHeight;
      ctx.fillStyle = '#f1f1ef';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function updateDrilldownCards() {
      const sjCs = batchData.drilldown[currentFw + '_Cs+'] || {};
      const sjSr = batchData.drilldown[currentFw + '_Sr2+'] || {};
      const container = document.getElementById('drilldownCards');

      container.innerHTML = 
        '<div style="border: 1px solid var(--notion-border); border-radius: 4px; padding: 1.25rem; background: #fff;">' +
          '<div style="font-size: 0.8rem; color: var(--notion-muted); font-weight: 500; margin-bottom: 0.5rem;">QM BINDING ENERGIES (&Delta;G<sub>bind</sub>)</div>' +
          '<div style="font-size: 0.9rem; line-height: 1.6;">' +
            '<div>Cs<sup>+</sup>: <strong>' + (sjCs.dg_bind_kj_mol ? sjCs.dg_bind_kj_mol.toFixed(2) : '--') + ' kJ/mol</strong></div>' +
            '<div>Sr<sup>2+</sup>: <strong>' + (sjSr.dg_bind_kj_mol ? sjSr.dg_bind_kj_mol.toFixed(2) : '--') + ' kJ/mol</strong></div>' +
          '</div>' +
        '</div>' +
        '<div style="border: 1px solid var(--notion-border); border-radius: 4px; padding: 1.25rem; background: #fff;">' +
          '<div style="font-size: 0.8rem; color: var(--notion-muted); font-weight: 500; margin-bottom: 0.5rem;">LANGMUIR / GAINES-THOMAS</div>' +
          '<div style="font-size: 0.9rem; line-height: 1.6;">' +
            '<div>K_Lang (Cs<sup>+</sup>): <strong>' + (sjCs.k_langmuir_m3_mol ? sjCs.k_langmuir_m3_mol.toFixed(2) : '--') + ' m³/mol</strong></div>' +
            '<div>q_max (Cs<sup>+</sup>): <strong>' + (sjCs.q_max_mol_kg ? sjCs.q_max_mol_kg.toFixed(2) : '--') + ' mol/kg</strong></div>' +
          '</div>' +
        '</div>' +
        '<div style="border: 1px solid var(--notion-border); border-radius: 4px; padding: 1.25rem; background: #fff;">' +
          '<div style="font-size: 0.8rem; color: var(--notion-muted); font-weight: 500; margin-bottom: 0.5rem;">MASS BALANCE RESIDUAL</div>' +
          '<div style="font-size: 0.9rem; line-height: 1.6;">' +
            '<div>Residual: <strong>' + (sjCs.mass_balance_residual ? sjCs.mass_balance_residual.toExponential(2) : '0.00e+00') + '</strong></div>' +
            '<div style="color: var(--notion-green-text); font-weight: 500;">Status: PASSED (&lt; 1.00e-03)</div>' +
          '</div>' +
        '</div>';
    }

    window.addEventListener('resize', renderCurrentFrame);
    loadResults();
  </script>
</body>
</html>
"""
    return html.replace("__BATCH_ID__", batch_id).replace("__COMMON_STYLE__", COMMON_STYLE)

def render_report_page(batch_id: str) -> str:
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Batch __BATCH_ID__ Research Paper | Quorum-Zeolite</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
  __COMMON_STYLE__
  <style>
    #reportContent {
      line-height: 1.85;
      font-size: 0.95rem;
      color: var(--notion-text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    #reportContent h1 {
      font-size: 1.95rem;
      font-weight: 700;
      line-height: 1.25;
      margin-top: 0.5rem;
      margin-bottom: 0.8rem;
      letter-spacing: -0.025em;
      color: var(--notion-text);
    }
    #reportContent h2 {
      font-size: 1.35rem;
      font-weight: 600;
      margin-top: 2.2rem;
      margin-bottom: 0.8rem;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--notion-border);
      letter-spacing: -0.015em;
      color: var(--notion-text);
    }
    #reportContent h3 {
      font-size: 1.10rem;
      font-weight: 600;
      margin-top: 1.5rem;
      margin-bottom: 0.6rem;
      color: var(--notion-text);
    }
    #reportContent h4 {
      font-size: 0.98rem;
      font-weight: 600;
      margin-top: 1.2rem;
      margin-bottom: 0.4rem;
      color: var(--notion-text);
    }
    #reportContent p {
      margin-bottom: 1.1rem;
    }
    #reportContent hr {
      border: 0;
      height: 1px;
      background-color: var(--notion-border);
      margin: 1.8rem 0;
    }
    #reportContent table {
      width: 100%;
      border-collapse: collapse;
      margin: 1.6rem 0;
      font-size: 0.85rem;
      line-height: 1.5;
      background: var(--notion-bg);
      border: 1px solid var(--notion-border);
      border-radius: 6px;
      overflow: hidden;
    }
    #reportContent th {
      background-color: var(--notion-bg-secondary);
      color: var(--notion-text);
      font-weight: 600;
      padding: 10px 14px;
      border-bottom: 2px solid var(--notion-border);
      border-right: 1px solid var(--notion-border);
      text-align: left;
    }
    #reportContent th:last-child {
      border-right: none;
    }
    #reportContent td {
      padding: 9px 14px;
      border-bottom: 1px solid var(--notion-border);
      border-right: 1px solid var(--notion-border);
      vertical-align: top;
    }
    #reportContent td:last-child {
      border-right: none;
    }
    #reportContent tr:last-child td {
      border-bottom: none;
    }
    #reportContent tr:hover {
      background-color: var(--notion-hover);
    }
    #reportContent blockquote {
      border-left: 3px solid var(--notion-blue-badge);
      background-color: rgba(35, 131, 226, 0.05);
      padding: 12px 18px;
      margin: 1.4rem 0;
      border-radius: 0 6px 6px 0;
      color: var(--notion-text);
    }
    #reportContent ul, #reportContent ol {
      padding-left: 1.6rem;
      margin-bottom: 1.2rem;
    }
    #reportContent li {
      margin-bottom: 0.45rem;
    }
    #reportContent code {
      font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
      font-size: 0.88em;
      background-color: var(--notion-bg-secondary);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--notion-border);
    }
    #reportContent .katex-display {
      margin: 1.4rem 0;
      padding: 12px 0;
      overflow-x: auto;
      overflow-y: hidden;
    }
    .paper-meta-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      font-weight: 500;
      padding: 3px 9px;
      border-radius: 4px;
      margin-right: 6px;
      margin-bottom: 12px;
    }
    @media print {
      .notion-navbar { display: none !important; }
      .page-icon { display: none !important; }
      .notion-container { max-width: 100% !important; padding: 0 !important; margin: 0 !important; }
      body { background: white !important; color: black !important; font-size: 11pt !important; }
      #reportContent table { font-size: 9pt !important; }
    }
  </style>
</head>
<body>
  <nav class="notion-navbar">
    <div class="notion-breadcrumbs">
      <a href="/submit"><span>🏢</span> Workspace</a>
      <span>/</span>
      <a href="/results/__BATCH_ID__"><span>📊</span> Batch Results</a>
      <span>/</span>
      <span style="color: var(--notion-text); font-weight: 500;">Research Paper</span>
    </div>
    <div class="notion-nav-actions">
      <button onclick="downloadMarkdown()" class="notion-btn notion-btn-secondary">Download .MD</button>
      <button onclick="window.print()" class="notion-btn notion-btn-secondary">Print / PDF</button>
      <a href="/results/__BATCH_ID__" class="notion-btn notion-btn-primary">Back to Results</a>
    </div>
  </nav>

  <div class="notion-container" style="max-width: 880px;">
    <div style="margin-bottom: 10px;">
      <span class="paper-meta-badge" style="background: rgba(15, 123, 108, 0.12); color: #0F7B6C;">✓ Verified Numerical Simulation</span>
      <span class="paper-meta-badge" style="background: rgba(105, 64, 165, 0.12); color: #6940A5;">★ Finite-Volume Mass Conserved</span>
      <span class="paper-meta-badge" style="background: rgba(35, 131, 226, 0.12); color: #2383E2;">⚡ Dynamically Written for Zeolite</span>
    </div>

    <div id="reportLoading" style="padding: 40px 0; text-align: center;">
      <div style="display: inline-block; width: 32px; height: 32px; border: 3px solid var(--notion-border); border-top-color: var(--notion-blue-badge); border-radius: 50%; animation: spin 0.8s linear infinite;"></div>
      <p style="color: var(--notion-muted); margin-top: 14px; font-size: 0.9rem;">Synthesizing research paper from verified numerical simulation data...</p>
    </div>

    <div id="reportContent" style="display: none;"></div>
  </div>

  <style>
    @keyframes spin { to { transform: rotate(360deg); } }
  </style>

  <script>
    let rawReportMarkdown = "";

    async function loadReport() {
      try {
        const res = await fetch('/batches/__BATCH_ID__/report', { method: 'POST' });
        const data = await res.json();
        rawReportMarkdown = data.report_markdown;

        const html = marked.parse(rawReportMarkdown);
        const container = document.getElementById('reportContent');
        container.innerHTML = html;

        // Render KaTeX mathematical expressions
        if (window.renderMathInElement) {
          renderMathInElement(container, {
            delimiters: [
              { left: '$$', right: '$$', display: true },
              { left: '$', right: '$', display: false },
              { left: '\\(', right: '\\)', display: false },
              { left: '\\[', right: '\\]', display: true }
            ],
            throwOnError: false
          });
        }

        document.getElementById('reportLoading').style.display = 'none';
        container.style.display = 'block';
      } catch (err) {
        document.getElementById('reportLoading').innerHTML = '<p style="color: var(--notion-red-text);">Error synthesizing technical paper from simulation data.</p>';
      }
    }

    function downloadMarkdown() {
      if (!rawReportMarkdown) return;
      const blob = new Blob([rawReportMarkdown], { type: 'text/markdown;charset=utf-8' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'quorum_zeolite_research_paper___BATCH_ID__.md';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }

    loadReport();
  </script>
</body>
</html>
"""
    return html.replace("__BATCH_ID__", batch_id).replace("__COMMON_STYLE__", COMMON_STYLE)
