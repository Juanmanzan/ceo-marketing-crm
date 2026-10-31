import { obtenerTokenCsrf } from '../utils/csrf.js';

const rutaBase = '/api/clientes/';

async function solicitar(ruta, opciones = {}) {
    const metodo = (opciones.method || 'GET').toUpperCase();
    const necesitaCsrf = !['GET', 'HEAD', 'OPTIONS'].includes(metodo);
    const respuesta = await fetch(ruta, {
        ...opciones,
        credentials: 'same-origin',
        headers: {
            Accept: 'application/json',
            ...(opciones.body ? {'Content-Type': 'application/json'} : {}),
            ...(necesitaCsrf ? {'X-CSRFToken': obtenerTokenCsrf()} : {}),
            ...opciones.headers,
        },
    });

    const tipoContenido = respuesta.headers.get('Content-Type') || '';
    const datos = tipoContenido.includes('application/json') ? await respuesta.json() : {};
    if (!respuesta.ok) {
        const error = new Error(datos.error || datos.mensaje || `Error HTTP ${respuesta.status}`);
        error.estado = respuesta.status;
        error.detalles = datos.errors || datos.errores || null;
        throw error;
    }
    return datos;
}

export function obtenerClientes({ buscar = '', estado = 'Todos', cursor = null } = {}) {
    const parametros = new URLSearchParams();
    if (buscar.trim()) parametros.set('buscar', buscar.trim());
    if (estado !== 'Todos') parametros.set('estado', estado);
    if (cursor !== null && cursor !== '') parametros.set('cursor', String(cursor));
    const cadenaConsulta = parametros.toString();
    return solicitar(rutaBase + (cadenaConsulta ? `?${cadenaConsulta}` : ''));
}

export const obtenerResumen = () => solicitar(`${rutaBase}resumen/`);
export const obtenerCliente = id => solicitar(`${rutaBase}${id}/`);
export const crearCliente = datos => solicitar(`${rutaBase}crear/`, { method: 'POST', body: JSON.stringify(datos) });
export const actualizarCliente = (id, datos) => solicitar(`${rutaBase}${id}/actualizar/`, { method: 'PUT', body: JSON.stringify(datos) });
export const eliminarCliente = id => solicitar(`${rutaBase}${id}/eliminar/`, { method: 'DELETE' });
