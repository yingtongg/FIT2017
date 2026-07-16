function qs(q){ return document.querySelector(q); }

function render(s, {showBanner = false} = {}) {
  const badge = qs("#badge");
  const reason = qs("#reason");
  const enrol = qs("#enrol");
  const banner = qs("#banner");

  badge.textContent = s.ready ? "Ready" : "Blocked";
  badge.className = `badge ${s.ready ? "ready" : "blocked"}`;

  if (s.ready || !s.reason) {
    reason.style.display = "none";
    reason.textContent = "";
  } else {
    reason.style.display = "block";
    reason.textContent = s.reason;
  }

  enrol.disabled = !s.enrolEnabled;

  // success banner only when we explicitly want to show it (after Fix)
  banner.style.display = showBanner ? "block" : "none";
}

async function refresh() {
  const seed = new URL(location.href).searchParams.get("seed") || "domestic_ok";
  const r = await fetch(`/state?seed=${encodeURIComponent(seed)}`);
  const s = await r.json();
  render(s);
}

async function applyFix() {
  const seed = new URL(location.href).searchParams.get("seed") || "domestic_ok";
  const r = await fetch(`/fix?seed=${encodeURIComponent(seed)}`, { method: "POST" });
  const s = await r.json();
  // Render using /fix response; do NOT call refresh() here (that would reset the seed)
  render(s, { showBanner: !!s.ok });
}

qs("#fix").addEventListener("click", applyFix);
window.addEventListener("load", refresh);
