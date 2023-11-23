document.addEventListener('DOMContentLoaded', () => {
    const inputs = document.querySelectorAll('.formulario__file');

    const formulario = document.querySelector('#formulario');
    const imagen = document.querySelector('#imagenMostrada');
    // const noticia = document.querySelector('#noticia');
    // const subtitulo = document.querySelector('#subtitulo');
    // const descripcion = document.querySelector('#descripcion');

    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');

     let guardarImagen = '';

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