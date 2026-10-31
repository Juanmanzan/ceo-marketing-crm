export function configurarFiltros({ alCambiar }) {
    const campoBusqueda = document.getElementById('tableSearch');
    const botones = document.querySelectorAll('[data-status]');
    const tarjetas = document.querySelectorAll('[data-stat-filter]');
    let filtro = 'Todos';
    let temporizador;

    function actualizarSeleccion() {
        botones.forEach(boton => boton.setAttribute('aria-pressed', String(boton.dataset.status === filtro)));
        tarjetas.forEach(tarjeta => tarjeta.classList.toggle('stat-selected', tarjeta.dataset.statFilter === filtro));
    }
    function seleccionar(valor) {
        filtro = valor;
        actualizarSeleccion();
        alCambiar({ buscar: campoBusqueda.value.trim(), estado: filtro });
    }

    botones.forEach(boton => boton.addEventListener('click', () => seleccionar(boton.dataset.status)));
    tarjetas.forEach(tarjeta => {
        tarjeta.addEventListener('click', () => seleccionar(tarjeta.dataset.statFilter));
        tarjeta.addEventListener('keydown', evento => {
            if (evento.key === 'Enter' || evento.key === ' ') {
                evento.preventDefault();
                seleccionar(tarjeta.dataset.statFilter);
            }
        });
    });
    campoBusqueda.addEventListener('input', () => {
        clearTimeout(temporizador);
        temporizador = setTimeout(() => alCambiar({ buscar: campoBusqueda.value.trim(), estado: filtro }), 300);
    });
    actualizarSeleccion();
}
