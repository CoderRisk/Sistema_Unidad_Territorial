document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');
    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');
    const nombre = document.querySelector('#id_nombre');
    const apellido = document.querySelector('#id_apellido');

    let inputs = document.querySelectorAll('#archivos');

    inputs.forEach(input => {
        let label = input.nextElementSibling;

        input.addEventListener('change', (e) => {
            

            var archivosSeleccionados = input.files;

           if (archivosSeleccionados.length > 0) {
            // Muestra la cantidad de archivos seleccionados en el label
            label.innerHTML = archivosSeleccionados.length + (archivosSeleccionados.length === 1 ? ' archivo' : ' archivos');
                if(archivosSeleccionados.length > 0 && nombre.value != '' && apellido != ''){
                    submit.style.cursor = 'pointer';
                    submit.style.backgroundColor = '#1464f6';
                }
            } else {
                // No hay archivos seleccionados
                submit.style.cursor = 'not-allowed';
                submit.style.backgroundColor = '#cb3939';
                label.innerHTML = 'Selecciona archivo/s';
            }

            
        })
        
    }) 

    formulario.addEventListener('submit', (e) => {
        
        inputs.forEach(input => {
            let label = input.nextElementSibling;
    
           
                
    
                var archivosSeleccionados = input.files;
    

                if(archivosSeleccionados.length > 0 && nombre.value != '' && apellido != '' ){
                    submit.style.display = "none";
                    cargar.style.display = "flex";
                    
                } else {
                    e.preventDefault()
                }
    
                
          
            
        }) 
        
    })
})