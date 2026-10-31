import { obtenerClientes } from './services/clientesApi.js';
import { renderizarClientes } from './components/tablaClientes.js';
import { cargarIndicadores } from './components/kpiCards.js';
import { configurarFiltros } from './components/filtrosClientes.js';
import { crearPaginacion } from './components/paginacion.js';
import { configurarModalCliente } from './components/modalCliente.js';
import { configurarModalEliminar } from './components/modalEliminar.js';
import { notificar } from './components/notificaciones.js';

const filtros = { buscar: '', estado: 'Todos' };
let numeroConsulta = 0;
let modalCliente;
let modalEliminar;

const paginacion = crearPaginacion(cargarClientes);

async function cargarClientes() {
    const consultaActual = ++numeroConsulta;
    try {
        const datos = await obtenerClientes({ ...filtros, cursor: paginacion.obtenerCursor() });
        if (consultaActual !== numeroConsulta) return;
        const clientes = datos.clientes || [];
        const totalClientes = datos.totalClientes ?? clientes.length;
        renderizarClientes(clientes, totalClientes, {
            editar: cliente => modalCliente.abrir(cliente),
            eliminar: cliente => modalEliminar.abrir(cliente),
        }, datos.totalFiltrados ?? totalClientes);
        paginacion.actualizar(datos);
    } catch (error) {
        if (consultaActual !== numeroConsulta) return;
        console.error('Error cargando clientes:', error);
        notificar(error.message, true);
    }
}

async function actualizarPantalla() {
    paginacion.reiniciar();
    await Promise.allSettled([cargarClientes(), cargarIndicadores()]);
}

function configurarNavegacion() {
    const menu = document.getElementById('mobileMenu');
    const barraLateral = document.getElementById('sidebar');
    const fondoNavegacion = document.getElementById('shade');
    const cerrarBarraLateral = () => {
        barraLateral.classList.remove('open');
        fondoNavegacion.classList.remove('show');
        menu?.setAttribute('aria-expanded', 'false');
    };
    menu?.addEventListener('click', () => {
        const abierto = barraLateral.classList.toggle('open');
        fondoNavegacion.classList.toggle('show', abierto);
        menu.setAttribute('aria-expanded', String(abierto));
    });
    fondoNavegacion?.addEventListener('click', cerrarBarraLateral);
    document.querySelectorAll('[data-page]').forEach(elementoNavegacion => {
        elementoNavegacion.querySelector('button')?.addEventListener('click', () => {
            document.querySelectorAll('[data-page]').forEach(opcionNavegacion => {
                opcionNavegacion.classList.toggle('active', opcionNavegacion === elementoNavegacion);
                opcionNavegacion.querySelector('button')?.removeAttribute('aria-current');
            });
            elementoNavegacion.querySelector('button')?.setAttribute('aria-current', 'page');
            const esPaginaClientes = elementoNavegacion.dataset.page === 'clientes';
            document.getElementById('crumb').textContent = esPaginaClientes ? 'Clientes' : 'Dashboard';
            document.getElementById('pageTitle').textContent = esPaginaClientes ? 'Directorio de clientes' : 'Panel de clientes';
            document.querySelector('.stats').hidden = esPaginaClientes;
            cerrarBarraLateral();
        });
    });
}

modalCliente = configurarModalCliente(actualizarPantalla);
modalEliminar = configurarModalEliminar(actualizarPantalla);
configurarFiltros({ alCambiar: nuevosFiltros => {
    Object.assign(filtros, nuevosFiltros);
    paginacion.reiniciar();
    cargarClientes();
} });

document.querySelectorAll('[data-close]').forEach(boton => {
    boton.addEventListener('click', () => {
        if (boton.dataset.close === 'formOverlay') modalCliente.cerrar();
        if (boton.dataset.close === 'deleteOverlay') modalEliminar.cerrar();
    });
});
configurarNavegacion();
actualizarPantalla();
