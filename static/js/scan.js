/* PixelProof AI — scan.js */

document.addEventListener("DOMContentLoaded", () => {
  const dropZone    = document.getElementById("drop-zone");
  const fileInput   = document.getElementById("file-input");
  const scanBtn     = document.getElementById("scan-btn");
  const btnText     = document.getElementById("btn-text");
  const btnLoading  = document.getElementById("btn-loading");
  const previewWrap = document.getElementById("preview-wrap");
  const previewImg  = document.getElementById("preview-img");
  const previewName = document.getElementById("preview-name");
  const form        = document.getElementById("scan-form");
  const pipeline    = document.querySelectorAll(".pipeline-step");

  // Drag & Drop Listeners
  if (dropZone) {
    dropZone.addEventListener("dragover", e => {
      e.preventDefault();
      dropZone.classList.add("drag");
    });
    
    dropZone.addEventListener("dragleave", () => {
      dropZone.classList.remove("drag");
    });
    
    dropZone.addEventListener("drop", e => {
      e.preventDefault();
      dropZone.classList.remove("drag");
      const file = e.dataTransfer.files[0];
      if (file) {
        fileInput.files = e.dataTransfer.files;
        showPreview(file);
      }
    });
  }

  // File Input Change
  if (fileInput) {
    fileInput.addEventListener("change", () => {
      if (fileInput.files[0]) {
        showPreview(fileInput.files[0]);
      }
    });
  }

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = e => {
      previewImg.src = e.target.result;
      
      const img = new Image();
      img.onload = () => {
        previewName.textContent = `${file.name} · ${(file.size / 1024).toFixed(1)} KB · ${img.naturalWidth}×${img.naturalHeight}px`;
      };
      img.src = e.target.result;

      previewWrap.classList.remove("hidden");
      if (dropZone) dropZone.classList.add("hidden");
      scanBtn.disabled = false;
      
      // Auto-scroll to initiate scan button smoothly
      scanBtn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    };
    reader.readAsDataURL(file);
  }

  // Form Submit Pipeline Animation
  if (form) {
    form.addEventListener("submit", () => {
      btnText.classList.add("hidden");
      btnLoading.classList.remove("hidden");
      scanBtn.disabled = true;

      let i = 0;
      const interval = setInterval(() => {
        if (i < pipeline.length) {
          pipeline[i].classList.add("active");
          if (i > 0) pipeline[i - 1].classList.replace("active", "done");
          i++;
        } else {
          clearInterval(interval);
        }
      }, 300);
    });
  }
});
