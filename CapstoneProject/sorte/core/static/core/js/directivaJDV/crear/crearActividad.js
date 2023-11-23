// import Swal from "../../../node_modules/sweetalert2/src/sweetalert2.js";

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.formulario__file');

    const formulario = document.querySelector('#formulario');
    const imagen = document.querySelector('#imagenMostrada');
    // const actividad = document.querySelector('#id_nombre_actividad');
    // const descripcion = document.querySelector('#id_descripcion');
    // const direccion = document.querySelector('#id_direccion');
    // const region = document.querySelector('#id_region');
    // const comuna = document.querySelector('#id_comuna');
    // const fechaActividad = document.querySelector('#id_fecha_actividad');
    // const fechaInicio = document.querySelector('#id_hora_inicio');
    // const fechaTermino = document.querySelector('#id_hora_termino');
    // const cupos = document.querySelector('#id_cupos_disponibles');

    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');


     inputs.forEach(input => {
     
         let label = input.nextElementSibling,
         labelVal = label.innerHTML;
 
 
         input.addEventListener('change', (e) => {
             
 
            var archivoSeleccionado = input.files[0];

            if (archivoSeleccionado) {
                // Crea un elemento de imagen

                var lector = new FileReader();

                lector.onload = function (e) {
                    imagen.src = e.target.result;
                };

                lector.readAsDataURL(archivoSeleccionado);
                

                label.innerHTML = archivoSeleccionado.name;

 
             } else {
                 label.textContent = 'Ningún archivo seleccionado';
             }
 
             
         })
         
     }) 
   
     

    formulario.addEventListener('submit', (e) => {

        submit.style.display = "none";
        cargar.style.display = "flex"

    })

    

    
})


function focusElement(e){
    e.target.style.borderBottom = "0.125rem solid #1464f6";
}

function blurElement(e){
    e.target.style.borderBottom = "0.125rem solid #00000049";
}