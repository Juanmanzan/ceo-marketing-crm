// Paginación por cursor: mantiene los cursores anteriores para poder regresar.
export function crearPaginacion(alCambiar) {
    const contenedor = document.getElementById('pager');
    let cursor = null;
    let cursorSiguiente = null;
    let historialCursores = [];
    let numeroPagina = 1;

    function dibujar() {
        contenedor.replaceChildren();
        function crearBoton(texto, deshabilitado, accion) {
            const elementoBoton = document.createElement('button');
            elementoBoton.type = 'button';
            elementoBoton.textContent = texto;
            elementoBoton.disabled = deshabilitado;
            elementoBoton.addEventListener('click', accion);
            contenedor.appendChild(elementoBoton);
        }
        crearBoton('Anterior', historialCursores.length === 0, () => {
            cursor = historialCursores.pop();
            numeroPagina--;
            alCambiar();
        });
        const texto = document.createElement('span');
        texto.textContent = `Página ${numeroPagina}`;
        texto.style.padding = '0 8px';
        contenedor.appendChild(texto);
        crearBoton('Siguiente', cursorSiguiente == null, () => {
            historialCursores.push(cursor);
            cursor = cursorSiguiente;
            numeroPagina++;
            alCambiar();
        });
    }
    function reiniciar() {
        cursor = null;
        cursorSiguiente = null;
        historialCursores = [];
        numeroPagina = 1;
        dibujar();
    }
    function actualizar(datos) {
        cursorSiguiente = datos.paginacion?.existeOtraPagina ? datos.paginacion.cursor_next : null;
        dibujar();
    }
    reiniciar();
    return { obtenerCursor: () => cursor, reiniciar, actualizar };
}
