
const items = document.querySelectorAll('.carousel__item');
const slider = document.querySelector('.carousel__slider');
const atras = document.querySelector('#atras');
const siguiente = document.querySelector('#siguiente');
const carouselPuntos = document.querySelector('.carousel__puntos');


document.addEventListener('DOMContentLoaded', () => {

    let slideIndex = 0;
    
    
    items.forEach((item, index) => {
        const punto = document.createElement('div');
        punto.classList.add('punto');
        punto.id = index;
        carouselPuntos.appendChild(punto);
    });


    function actualizarCarousel() {
        puntos.forEach((item, index) => {
            if (index === slideIndex) {
                item.classList.add('activo');
            } else {
                item.classList.remove('activo');
            }
        });
    
        slider.style.left = slideIndex * -100 + '%';
    }
    
    function avanzarCarousel() {
        slideIndex = (slideIndex + 1) % items.length;
        actualizarCarousel();
    }
    
    function retrocederCarousel() {
        slideIndex = (slideIndex - 1 + items.length) % items.length;
        actualizarCarousel();
    }

    const puntos = document.querySelectorAll('.punto');
    
    // Agrega event listeners a los puntos
    puntos.forEach((punto, index) => {
        punto.addEventListener('click', () => {
            clearInterval(intervalId);
            slideIndex = index;
            actualizarCarousel();
            intervalId = setInterval(avanzarCarousel, 3000);
        });
    });
    
    let intervalId;

    // Actualizar el carrusel inmediatamente al cargar la página
    actualizarCarousel();

    // Iniciar el intervalo después de 3000 milisegundos
    intervalId = setInterval(avanzarCarousel, 3000);

    atras.addEventListener('click', () => {
        clearInterval(intervalId);
        retrocederCarousel();
        intervalId = setInterval(avanzarCarousel, 3000);
    });

    siguiente.addEventListener('click', () => {
        clearInterval(intervalId);
        avanzarCarousel();
        intervalId = setInterval(avanzarCarousel, 3000);
    });
});
