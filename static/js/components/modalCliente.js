import { crearCliente, actualizarCliente } from '../services/clientesApi.js';
import { notificar } from './notificaciones.js';
import { limpiarErroresFormulario, validarCliente, mostrarErroresFormulario } from '../utils/validaciones.js';

export function configurarModalCliente(alGuardar) {
    const obtenerElemento = id => document.getElementById(id);
    const formulario = obtenerElemento('clientForm');
    const fondoModal = obtenerElemento('formOverlay');
    let idClienteEnEdicion = null;

    function cambiarEstado(valor) {
        obtenerElemento('fieldStatus').value = valor;
        obtenerElemento('statusValue').textContent = valor;
        obtenerElemento('statusTrigger').querySelector('.status-dot').className = `status-dot ${valor.toLowerCase()}`;
        document.querySelectorAll('#statusOptions [data-value]').forEach(botonEstado => {
            botonEstado.setAttribute('aria-selected', String(botonEstado.dataset.value === valor));
        });
        obtenerElemento('statusOptions').hidden = true;
        obtenerElemento('statusTrigger').setAttribute('aria-expanded', 'false');
        obtenerElemento('statusSelect').classList.remove('is-open');
    }
    function cerrar() {
        fondoModal.hidden = true;
        document.body.style.overflow = '';
    }
    function abrir(cliente = null) {
        idClienteEnEdicion = cliente?.id ?? null;
        formulario.reset();
        limpiarErroresFormulario();
        obtenerElemento('fieldName').value = cliente?.name ?? '';
        obtenerElemento('fieldCompany').value = cliente?.company ?? '';
        obtenerElemento('fieldEmail').value = cliente?.email ?? '';
        obtenerElemento('fieldPhone').value = cliente?.phone ?? '';
        cambiarEstado(cliente?.status || 'Prospecto');
        obtenerElemento('formTitle').textContent = cliente ? 'Editar cliente' : 'Nuevo cliente';
        obtenerElemento('saveBtn').textContent = cliente ? 'Actualizar cliente' : 'Guardar cliente';
        fondoModal.hidden = false;
        document.body.style.overflow = 'hidden';
        obtenerElemento('fieldName').focus();
    }
    function obtenerDatos() {
        return {
            name: obtenerElemento('fieldName').value.trim(), company: obtenerElemento('fieldCompany').value.trim(),
            email: obtenerElemento('fieldEmail').value.trim(), phone: obtenerElemento('fieldPhone').value.trim(),
            status: obtenerElemento('fieldStatus').value,
        };
    }
    async function guardar(evento) {
        evento.preventDefault();
        limpiarErroresFormulario();
        const datos = obtenerDatos();
        const errores = validarCliente(datos);
        if (Object.keys(errores).length) {
            mostrarErroresFormulario(errores);
            notificar(Object.values(errores)[0], true);
            return;
        }
        const boton = obtenerElemento('saveBtn');
        boton.disabled = true;
        try {
            if (idClienteEnEdicion === null) await crearCliente(datos);
            else await actualizarCliente(idClienteEnEdicion, datos);
            const fueCreacion = idClienteEnEdicion === null;
            cerrar();
            notificar(fueCreacion ? 'Cliente creado correctamente' : 'Cliente actualizado correctamente');
            await alGuardar();
        } catch (error) {
            console.error(error);
            mostrarErroresFormulario(error.detalles);
            notificar(error.estado === 403 ? 'Acceso denegado: verifica CSRF' : error.message, true);
        } finally { boton.disabled = false; }
    }
    obtenerElemento('addBtn').addEventListener('click', () => abrir());
    formulario.addEventListener('submit', guardar);
    obtenerElemento('statusTrigger').addEventListener('click', () => {
        const abrirMenu = obtenerElemento('statusOptions').hidden;
        obtenerElemento('statusOptions').hidden = !abrirMenu;
        obtenerElemento('statusTrigger').setAttribute('aria-expanded', String(abrirMenu));
        obtenerElemento('statusSelect').classList.toggle('is-open', abrirMenu);
    });
    document.querySelectorAll('#statusOptions [data-value]').forEach(botonEstado => {
        botonEstado.addEventListener('click', () => cambiarEstado(botonEstado.dataset.value));
    });
    return { abrir, cerrar };
}
