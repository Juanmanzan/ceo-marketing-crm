export function limpiarErroresFormulario() {
    document.querySelectorAll('#clientForm .invalid').forEach(elemento => elemento.classList.remove('invalid'));
    document.querySelectorAll('#clientForm .error').forEach(elemento => { elemento.textContent = ''; });
}

export function validarCliente(datos) {
    const errores = {};
    if (!datos.name.trim()) errores.name = 'El nombre es obligatorio';
    else if (datos.name.length > 50) errores.name = 'Máximo 50 caracteres';
    else if (datos.name.trim().split(/\s+/).length < 2) errores.name = 'Ingresa al menos un nombre y un apellido';
    else if (!datos.name.trim().split(/\s+/).every(palabra => /^\p{L}+(?:[-'’]\p{L}+)*$/u.test(palabra))) {
        errores.name = 'El nombre solo puede contener letras, espacios, guiones y apóstrofes';
    }
    if (!datos.email.trim()) errores.email = 'El correo es obligatorio';
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(datos.email)) errores.email = 'Ingresa un correo válido';
    if (datos.company.length > 50) errores.company = 'Máximo 50 caracteres';
    if (datos.phone && (!/^\d+$/.test(datos.phone) || datos.phone.length > 10)) errores.phone = 'Solo números, máximo 10';
    if (!['Prospecto', 'Cliente', 'Inactivo'].includes(datos.status)) errores.status = 'Estado inválido';
    return errores;
}

export function mostrarErroresFormulario(errores) {
    const campos = {
        name: ['fieldName', 'errName'], email: ['fieldEmail', 'errEmail'],
        phone: ['fieldPhone', 'errPhone'],
    };
    for (const [campo, mensajes] of Object.entries(errores || {})) {
        const destino = campos[campo];
        if (!destino) continue;
        document.getElementById(destino[0]).classList.add('invalid');
        const texto = Array.isArray(mensajes)
            ? mensajes.map(mensaje => typeof mensaje === 'string' ? mensaje : mensaje.message).join(' ')
            : String(mensajes);
        document.getElementById(destino[1]).textContent = texto;
    }
}
