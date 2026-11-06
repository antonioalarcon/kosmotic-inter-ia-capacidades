const escapeHtml = (value) => String(value ?? '')
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

const labelEstado = (estado) => ({
  fijo: 'Semántico fijo',
  contextual: 'Semántico contextual',
  decorativo: 'Decorativo'
}[estado] || estado);

async function loadGraphicSystem() {
  const resumen = document.querySelector('#sg-resumen');
  const regla = document.querySelector('#sg-regla');
  const catalogo = document.querySelector('#sg-catalogo');
  if (!resumen || !regla || !catalogo) return;

  try {
    const response = await fetch('data/sistema-grafico.json');
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();

    const totalIconos = data.iconos.length;
    const totalFamilias = data.familias.length;
    const estados = data.iconos.reduce((acc, item) => {
      acc[item.estado_semantico] = (acc[item.estado_semantico] || 0) + 1;
      return acc;
    }, {});

    resumen.innerHTML = `
      <article class="mini-card"><strong>${escapeHtml(data.version)}</strong><span>Versión</span></article>
      <article class="mini-card"><strong>${totalIconos}</strong><span>Iconos registrados</span></article>
      <article class="mini-card"><strong>${totalFamilias}</strong><span>Familias conceptuales</span></article>
      <article class="mini-card"><strong>${escapeHtml(data.estado)}</strong><span>Estado</span></article>
    `;

    regla.innerHTML = Object.entries(data.regla_coherencia).map(([key, value]) => `
      <article class="rule-card">
        <h3>${escapeHtml(labelEstado(key.replace('semantico_', '')))}</h3>
        <p>${escapeHtml(value)}</p>
      </article>
    `).join('');

    const iconosPorFamilia = data.iconos.reduce((acc, item) => {
      (acc[item.familia] ||= []).push(item);
      return acc;
    }, {});

    catalogo.innerHTML = data.familias.map((familia) => {
      const iconos = iconosPorFamilia[familia.slug] || [];
      return `
        <section class="family-block" id="${escapeHtml(familia.slug)}">
          <div class="family-header">
            <h3>${escapeHtml(familia.titulo)}</h3>
            <span>${iconos.length} iconos</span>
          </div>
          <div class="icon-grid">
            ${iconos.map((item) => `
              <article class="icon-card">
                <div class="icon-symbol">${escapeHtml(item.icono)}</div>
                <div class="icon-meta">
                  <div class="icon-number">${String(item.id).padStart(2, '0')}</div>
                  <h4>${escapeHtml(item.nombre)}</h4>
                  <p>${escapeHtml(item.significado_funcional)}</p>
                  <span class="state-pill state-${escapeHtml(item.estado_semantico)}">${escapeHtml(labelEstado(item.estado_semantico))}</span>
                </div>
              </article>
            `).join('')}
          </div>
        </section>
      `;
    }).join('');
  } catch (error) {
    catalogo.innerHTML = '<p>No se pudo cargar el sistema gráfico estructurado.</p>';
    console.error(error);
  }
}

loadGraphicSystem();
