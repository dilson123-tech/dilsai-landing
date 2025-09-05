// ano no rodapé
document.getElementById('year').textContent = new Date().getFullYear();

// rolagem suave CTA
document.getElementById('cta-btn').addEventListener('click', (e) => {
  const target = document.querySelector('#cta');
  if (target) {
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
});

// toggle mensal/anual
const toggle = document.getElementById('billing-toggle');
const prices = document.querySelectorAll('[data-price-m]');
function applyBilling() {
  prices.forEach(span => {
    span.textContent = toggle.checked ? span.dataset.priceY : span.dataset.priceM;
  });
}
toggle.addEventListener('change', applyBilling);
applyBilling();
