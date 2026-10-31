/**
 * Blockchain Leak Tracing - Interactive UI Controller
 */

document.addEventListener("DOMContentLoaded", function () {
  // 1. Live Ledger Audit Verification Button Handler
  const verifyBtn = document.getElementById("btn-verify-ledger");
  const auditResultModal = document.getElementById("ledger-audit-result");

  if (verifyBtn) {
    verifyBtn.addEventListener("click", function () {
      verifyBtn.disabled = true;
      const originalText = verifyBtn.innerHTML;
      verifyBtn.innerHTML = `
        <svg class="animate-spin" style="width:14px;height:14px;animation:spin 1s linear infinite;" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="12" cy="12" r="10" stroke-width="4" stroke="currentColor" stroke-dasharray="32" stroke-linecap="round"></circle>
        </svg> Cryptographic Audit in Progress...
      `;

      fetch("/api/ledger/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
        .then(response => response.json())
        .then(data => {
          verifyBtn.disabled = false;
          verifyBtn.innerHTML = originalText;

          if (auditResultModal) {
            auditResultModal.style.display = "block";
            const statusEl = document.getElementById("audit-status-badge");
            const detailsEl = document.getElementById("audit-details-content");

            if (data.is_valid) {
              statusEl.className = "status-badge badge-valid";
              statusEl.innerHTML = `<span class="pulse-dot"></span> CRYPTOGRAPHICALLY VALID`;
              detailsEl.innerHTML = `
                <p><strong>Total Blocks Checked:</strong> ${data.total_blocks}</p>
                <p><strong>Total Access Events Audited:</strong> ${data.total_events}</p>
                <p style="color:#15803d;margin-top:8px;">✓ All SHA-256 block hash links verified.</p>
                <p style="color:#15803d;">✓ All Merkle roots recomputed and matched exactly.</p>
                <p style="color:#15803d;">✓ All custodian Ed25519 digital signatures mathematically validated.</p>
              `;
            } else {
              statusEl.className = "status-badge badge-danger";
              statusEl.innerHTML = `<span class="pulse-dot"></span> TAMPERING DETECTED`;
              let errHtml = `<p style="color:#b91c1c;font-weight:600;">Cryptographic Audit Failed (${data.errors.length} anomalies detected):</p><ul style="margin-left:20px;margin-top:6px;">`;
              data.errors.forEach(err => {
                errHtml += `<li><strong>Block #${err.block_index}:</strong> ${err.error_type} - ${err.details}</li>`;
              });
              errHtml += "</ul>";
              detailsEl.innerHTML = errHtml;
            }
          } else {
            alert(`Audit Complete: Ledger is ${data.is_valid ? 'VALID (100% Intact)' : 'COMPROMISED'}`);
            window.location.reload();
          }
        })
        .catch(err => {
          verifyBtn.disabled = false;
          verifyBtn.innerHTML = originalText;
          alert("Audit failed due to network error: " + err);
        });
    });
  }

  // 2. Demo Dataset Seed Handler
  const seedDemoBtn = document.getElementById("btn-seed-demo");
  if (seedDemoBtn) {
    seedDemoBtn.addEventListener("click", function () {
      if (!confirm("Load standardized university examination demonstration dataset?\n(This will register 1 exam, 4 custodians, 8 fingerprinted copies, and 24 signed blockchain custody events.)")) {
        return;
      }
      seedDemoBtn.disabled = true;
      seedDemoBtn.innerText = "Loading Demonstration Data...";

      fetch("/api/demo/seed", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
        .then(res => res.json())
        .then(data => {
          alert("Demonstration dataset initialized successfully!");
          window.location.reload();
        })
        .catch(err => {
          seedDemoBtn.disabled = false;
          seedDemoBtn.innerText = "Load Demonstration Dataset";
          alert("Failed to seed demo data: " + err);
        });
    });
  }

  // 3. Demo Dataset Reset Handler
  const resetDemoBtn = document.getElementById("btn-reset-demo");
  if (resetDemoBtn) {
    resetDemoBtn.addEventListener("click", function () {
      if (!confirm("Are you sure you want to reset the demonstration dataset?\nAll demo examinations, copies, and events will be wiped.")) {
        return;
      }
      resetDemoBtn.disabled = true;
      resetDemoBtn.innerText = "Resetting...";

      fetch("/api/demo/reset", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
      })
        .then(res => res.json())
        .then(data => {
          alert("Demonstration data wiped clean.");
          window.location.reload();
        })
        .catch(err => {
          resetDemoBtn.disabled = false;
          resetDemoBtn.innerText = "Reset Demo Data";
          alert("Failed to reset: " + err);
        });
    });
  }

  // 4. Investigation Quick Sample Selectors
  const sampleSelect = document.getElementById("select-sample-preset");
  const sampleTextarea = document.getElementById("sample_text");

  if (sampleSelect && sampleTextarea) {
    sampleSelect.addEventListener("change", function () {
      const selectedVal = this.value;
      if (!selectedVal) return;
      
      // Auto-submit form or set preloaded_sample field
      const preloadedField = document.getElementById("preloaded_sample");
      if (preloadedField) {
        preloadedField.value = selectedVal;
      }
    });
  }
});
