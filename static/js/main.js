/* PixelProof AI — main.js */

document.addEventListener("DOMContentLoaded", () => {
  // Live UTC Clock in Footer
  function updateClock() {
    const clockEl = document.getElementById("utc-clock");
    if (clockEl) {
      const now = new Date();
      const utcString = now.toISOString().replace("T", " ").substring(0, 19) + " UTC";
      clockEl.textContent = utcString;
    }
  }
  updateClock();
  setInterval(updateClock, 1000);

  // Auto-hide flash notifications after 4.5 seconds
  document.querySelectorAll(".flash").forEach(el => {
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateY(-8px)";
      el.style.transition = "opacity 0.4s ease, transform 0.4s ease";
      setTimeout(() => el.remove(), 400);
    }, 4500);
  });
});
