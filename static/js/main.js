/* PixelProof AI — main.js */

// Auth tab switching
document.addEventListener("DOMContentLoaded", () => {
  const tabs = document.querySelectorAll(".auth-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      const target = tab.dataset.tab;
      document.querySelectorAll(".auth-form").forEach(f => f.classList.add("hidden"));
      const form = document.getElementById(`form-${target}`);
      if (form) form.classList.remove("hidden");
    });
  });

  // Auto-hide flash messages after 4s
  document.querySelectorAll(".flash").forEach(el => {
    setTimeout(() => { el.style.opacity = "0"; el.style.transition = "opacity 0.5s"; }, 4000);
  });
});
