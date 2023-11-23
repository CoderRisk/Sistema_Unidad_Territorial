const formulario = document.querySelector('#formulario');
const submit = document.querySelector('#formulario__enviar');
const cargar = document.querySelector('.load');

document.addEventListener('DOMContentLoaded', () => {
    formulario.addEventListener('submit', () => {
        submit.style.display = 'none';
        cargar.style.display = 'flex';
    })
})