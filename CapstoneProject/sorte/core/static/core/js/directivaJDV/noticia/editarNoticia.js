
document.addEventListener('DOMContentLoaded', () => {
    let inputs = document.querySelectorAll('.formulario__file');
    const img = document.querySelector('#imagen-preview');

    inputs.forEach(input => {
        let label = input.nextElementSibling;

        input.addEventListener('change', (e) => {
            

           var archivoSeleccionado = input.files[0];

           if (archivoSeleccionado) {

                // Crea un elemento de imagen
                label.innerHTML = archivoSeleccionado.name;

                var reader = new FileReader();
                reader.onload = function (e) {
                    img.src = e.target.result;
                };
                reader.readAsDataURL(input.files[0]);
               

            } 

            
        })
        
    }) 
});
