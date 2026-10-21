// Shared helpers for all tools.
window.fmt = (n, d = 0) =>
  Number.isFinite(n) ? n.toLocaleString("zh-TW", { minimumFractionDigits: d, maximumFractionDigits: d }) : "—";
window.num = (id) => parseFloat(document.getElementById(id).value);
window.bindAll = (fn) => {
  document.querySelectorAll("main input, main select").forEach((el) => el.addEventListener("input", fn));
  fn();
};
