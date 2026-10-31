import { eliminarCliente } from '../services/clientesApi.js';
import { notificar } from './notificaciones.js';

export function configurarModalEliminar(alEliminar) {
    const obtenerElemento = id => document.getElementById(id);
    const fondoModal = obtenerElemento('deleteOverlay');
    let clienteActual = null;

    function abrir(cliente) {
        clienteActual = cliente;
        obtenerElemento('deleteCopy').textContent = `¿Deseas eliminar a ${cliente.name}? Esta acción no se puede deshacer.`;
        fondoModal.hidden = false;
        document.body.style.overflow = 'hidden';
    }
    function cerrar() {
        fondoModal.hidden = true;
        clienteActual = null;
        document.body.style.overflow = '';
    }
    async function confirmar() {
        if (!clienteActual) return;
        const boton = obtenerElemento('confirmDelete');
        boton.disabled = true;
        try {
            await eliminarCliente(clienteActual.id);
            cerrar();
            notificar('Cliente eliminado correctamente');
            await alEliminar();
        } catch (error) {
            console.error(error);
            notificar(error.message, true);
        } finally { boton.disabled = false; }
    }
    obtenerElemento('confirmDelete').addEventListener('click', confirmar);
    return { abrir, cerrar };
}
