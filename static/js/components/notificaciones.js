export function notificar(mensaje, esError = false) {
    const contenedorNotificaciones = document.getElementById('toastArea');
    const notificacion = document.createElement('div');
    notificacion.className = `toast${esError ? ' error' : ''}`;
    const texto = document.createElement('span');
    texto.textContent = mensaje;
    const botonCerrar = document.createElement('button');
    botonCerrar.type = 'button';
    botonCerrar.textContent = '×';
    botonCerrar.setAttribute('aria-label', 'Cerrar notificación');
    botonCerrar.addEventListener('click', () => notificacion.remove());
    notificacion.append(texto, botonCerrar);
    contenedorNotificaciones.appendChild(notificacion);
    setTimeout(() => notificacion.remove(), 4000);
}
