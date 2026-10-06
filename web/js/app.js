async function loadCapabilities() {
  const target = document.querySelector('#capacidades');
  if (!target) return;

  try {
    const response = await fetch('../data/capacidades.json');
    const data = await response.json();

    target.innerHTML = data.capacidades.map((item) => `
      <article class="card">
        <div class="number">${String(item.id).padStart(2, '0')}</div>
        <h3>${item.titulo}</h3>
        <p>${item.resumen}</p>
      </article>
    `).join('');
  } catch (error) {
    target.innerHTML = '<p>No se pudieron cargar las capacidades estructuradas.</p>';
    console.error(error);
  }
}

loadCapabilities();
