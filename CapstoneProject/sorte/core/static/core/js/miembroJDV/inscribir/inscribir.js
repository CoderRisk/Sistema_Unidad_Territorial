document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');
    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');

    let inputs = document.querySelectorAll('#archivos');

    inputs.forEach(input => {
        let label = input.nextElementSibling;

        input.addEventListener('change', (e) => {
            

            var archivosSeleccionados = input.files;

           if (archivosSeleccionados.length > 0) {
            // Muestra la cantidad de archivos seleccionados en el label
                label.innerHTML = archivosSeleccionados.length + (archivosSeleccionados.length === 1 ? ' archivo' : ' archivos');
            } else {
                // No hay archivos seleccionados
                label.innerHTML = 'Selecciona archivo/s';
            }

            
        })
        
    }) 

    formulario.addEventListener('submit', (e) => {
        submit.style.display = "none";
        cargar.style.display = "flex";

      

        if(nombre.value != '' && apellido != '' ){
            submit.style.display = "none";
            cargar.style.display = "flex";
            
        } else {
            e.preventDefault()
        }

                
          
      
    })
    
})

