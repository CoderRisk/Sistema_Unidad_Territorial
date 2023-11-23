document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.querySelector('#formulario');
    const submit = document.querySelector('.formulario__submit');
    const cargar = document.querySelector('.load');

    formulario.addEventListener('submit', () => {
        submit.style.display = "none";
        cargar.style.display = "flex";
    })
})