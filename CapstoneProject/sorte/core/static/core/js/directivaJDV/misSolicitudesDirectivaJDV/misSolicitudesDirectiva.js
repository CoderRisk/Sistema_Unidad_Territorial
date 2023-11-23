document.addEventListener('DOMContentLoaded', () => {
    const link = document.querySelectorAll('.main__link');

    const linkInscripcion = link[0];
    const linkPostulacion = link[1];

    const enlace = document.querySelector('.main__enlace.activo');
    
    linkInscripcion.addEventListener('click', () => {
        inscripciones();

        

        console.log(enlace)

        if(enlace.classList.contains('activo')){
            enlace.classList.remove('activo');
        } else {
            enlace.classList.add('activo');
        }

    })

    linkPostulacion.addEventListener('click', () => {
        postulaciones();
    })
})

function inscripciones(){
    const solicitudInscripcion = document.querySelectorAll('.solicitud__inscripcion');

    const link = document.querySelectorAll('.main__link');

    const linkInscripcion = link[0];


    solicitudInscripcion.forEach(inscripcion => {

        let inscripcionDisplay = window.getComputedStyle(inscripcion);
        
        if(inscripcionDisplay.display === '' && linkInscripcion.style.backgroundColor === ''){
            inscripcion.style.display = "block";
            linkInscripcion.style.backgroundColor = '#3d8af7';

        }else if(inscripcionDisplay.display === 'block'){
            inscripcion.style.display = "none";
            linkInscripcion.style.backgroundColor = '';

            
        }else{
            inscripcion.style.display = "block";
            linkInscripcion.style.backgroundColor = '#3d8af7';
            
            
        }
    })
}

function postulaciones(){
    const solicitudPostulacion = document.querySelectorAll('.solicitud__postulacion');

    const link = document.querySelectorAll('.main__link');

    const linkPostulacion = link[1];

    solicitudPostulacion.forEach(postulacion => {

        if(postulacion.style.display === '' && linkPostulacion.style.backgroundColor === ''){
            postulacion.style.display = "block";
            linkPostulacion.style.backgroundColor = '#3d8af7';

        }else if(postulacion.style.display === 'block'){
            postulacion.style.display = "none";
            linkPostulacion.style.backgroundColor = '';

        }else{
            postulacion.style.display = "block";
            linkPostulacion.style.backgroundColor = '#3d8af7';
        }
    })
}