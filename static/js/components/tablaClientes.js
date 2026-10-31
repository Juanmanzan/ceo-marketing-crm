function crearCelda(valor) {
    const celda = document.createElement('td');
    celda.textContent = valor ?? '—';
    return celda;
}

function iniciales(nombre = '') {
    return nombre.trim().split(/\s+/).slice(0, 2).map(parteNombre => parteNombre[0] || '').join('').toUpperCase();
}

function crearBoton(accion, etiqueta, icono, cliente, alSeleccionar) {
    const boton = document.createElement('button');
    boton.type = 'button';
    boton.dataset.action = accion;
    boton.setAttribute('aria-label', `${etiqueta} a ${cliente.name}`);
    boton.title = etiqueta;
    const iconoSvg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const referenciaIcono = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    iconoSvg.setAttribute('viewBox', '0 0 24 24');
    iconoSvg.setAttribute('fill', 'none');
    iconoSvg.setAttribute('stroke', 'currentColor');
    referenciaIcono.setAttribute('href', `#i-${icono}`);
    iconoSvg.appendChild(referenciaIcono);
    boton.appendChild(iconoSvg);
    boton.addEventListener('click', () => alSeleccionar(cliente));
    return boton;
}

export function renderizarClientes(clientes, totalClientes, { editar, eliminar }, totalFiltrados = totalClientes) {
    const cuerpoTabla = document.getElementById('tableBody');
    const estadoVacio = document.getElementById('emptyState');
    const contador = document.getElementById('resultCount');
    cuerpoTabla.replaceChildren();
    estadoVacio.hidden = clientes.length !== 0;
    contador.textContent = `${clientes.length} de ${totalFiltrados} resultados (${totalClientes} registrados)`;

    for (const cliente of clientes) {

        const fila = document.createElement('tr');
        
        const celdaNombre = document.createElement('td');
        const contenedorNombre = document.createElement('div');
        contenedorNombre.className = 'client-cell';
        const avatar = document.createElement('span');
        avatar.className = 'avatar';
        avatar.textContent = iniciales(cliente.name);
        const nombre = document.createElement('span');
        nombre.className = 'client-name';
        nombre.textContent = cliente.name;
        contenedorNombre.append(avatar, nombre);
        celdaNombre.appendChild(contenedorNombre);
        fila.append(celdaNombre, crearCelda(cliente.company || '—'), crearCelda(cliente.email), crearCelda(cliente.phone || '—'));

        const celdaEstado = document.createElement('td');
        const etiquetaEstado = document.createElement('span');
        etiquetaEstado.className = `badge ${String(cliente.status || '').toLowerCase()}`;
        etiquetaEstado.textContent = cliente.status;
        celdaEstado.appendChild(etiquetaEstado);
        fila.appendChild(celdaEstado);

        fila.appendChild(crearCelda(cliente.created_at ? new Date(cliente.created_at).toLocaleDateString('es-EC') : '—'));
        const celdaAcciones = document.createElement('td');
        const acciones = document.createElement('div');
        acciones.className = 'row-actions';
        acciones.append(
            crearBoton('edit', 'Editar', 'edit', cliente, editar),
            crearBoton('delete', 'Eliminar', 'trash', cliente, eliminar),
        );
        celdaAcciones.appendChild(acciones);
        fila.appendChild(celdaAcciones);
        cuerpoTabla.appendChild(fila);
    }
}
