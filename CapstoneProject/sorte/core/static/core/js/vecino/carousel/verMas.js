const contenido = document.querySelector('.contenido__descripcion');
const contenidoSeparado = document.querySelector('.contenido__separado');

document.addEventListener('DOMContentLoaded', () => {
    // Dividir el contenido en oraciones utilizando el punto como separador
    let oraciones = contenido.innerHTML.split('.');

    let nuevoContenido = oraciones.map(function(oracion) {
        let oracionLimpia = oracion.trim();
        return oracionLimpia.length > 0 ? '<p>' + oracionLimpia + '.</p>' : '';
    }).join('');


    contenido.innerHTML = nuevoContenido;
    
})