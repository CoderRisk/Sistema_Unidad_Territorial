// import Swal from "../../../../node_modules/sweetalert2/src/sweetalert2.js";

document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.formulario__file');

    const formulario = document.querySelector('#formulario');
    const imagen = document.querySelector('#imagenMostrada');
    // const nombre = document.querySelector('#nombre__proyecto');
    // const descripcion = document.querySelector('#descripcion');
    // const requisitos = document.querySelector('#requisitos');
    // const cupos = document.querySelector('#cupos');
    // const fechaInicio = document.querySelector('#fechaInicio');
    // const fechaTermino = document.querySelector('#fechaTermino');

    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');

    console.log(imagen)

     inputs.forEach(input => {
     
         let label = input.nextElementSibling,
         labelVal = label.innerHTML;
 
 
         input.addEventListener('change', (e) => {
             
 
            var archivoSeleccionado = input.files[0];

            console.log(e)
            console.log(archivoSeleccionado)
            if (archivoSeleccionado) {
                // Crea un elemento de imagen
                

                var lector = new FileReader();

                lector.onload = function (e) {
                    imagen.src = e.target.result;
                };

                lector.readAsDataURL(archivoSeleccionado);
                
                // imagen.src = archivoSeleccionado;
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