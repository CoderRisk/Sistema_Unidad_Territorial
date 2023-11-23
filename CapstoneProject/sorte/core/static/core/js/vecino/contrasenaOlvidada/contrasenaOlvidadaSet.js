const formulario = document.querySelector('#formulario');
const submit = document.querySelector('.cambiar');
const cargar = document.querySelector('.load');

document.addEventListener('DOMContentLoaded', () => {
    formulario.addEventListener('submit', () => {
        submit.style.display = 'none';
        cargar.style.display = 'flex';
    })
})