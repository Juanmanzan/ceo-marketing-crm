// Django genera el token mediante {% csrf_token %} dentro del formulario.
export function obtenerTokenCsrf() {
    return document.querySelector('[name="csrfmiddlewaretoken"]')?.value || '';
}
