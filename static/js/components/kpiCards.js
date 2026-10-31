import { obtenerResumen } from '../services/clientesApi.js';

export async function cargarIndicadores() {
    const datos = await obtenerResumen();
    document.getElementById('statTotal').textContent = datos.totalClientes ?? 0;
    document.getElementById('statProspect').textContent = datos.prospectos ?? 0;
    document.getElementById('statClient').textContent = datos.clientesActivos ?? 0;
    document.getElementById('statInactive').textContent = datos.inactivos ?? 0;
}
