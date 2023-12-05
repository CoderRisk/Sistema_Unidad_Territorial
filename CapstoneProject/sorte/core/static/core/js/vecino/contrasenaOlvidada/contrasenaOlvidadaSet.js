const formulario = document.querySelector('#formulario');
const submit = document.querySelector('.cambiar');
const cargar = document.querySelector('.load');

const visualizar = document.querySelectorAll('.formulario__visualizar');
const oculto = document.querySelectorAll('.formulario__oculto');
const contrasena1 = document.querySelector('#id_new_password1');
const contrasena2 = document.querySelector('#id_new_password2');

document.addEventListener('DOMContentLoaded', () => {
    formulario.addEventListener('submit', () => {
        submit.style.display = 'none';
        cargar.style.display = 'flex';
    })


    visualizar.forEach((e, i) => {
        e.addEventListener('click', mostrar);
        
    }); 


    oculto.forEach((e, i) => {
            
        e.addEventListener('click', ocultar);
    }); 
})

function mostrar(e){

    let siguiente = e.target.nextElementSibling;

    let contrasena = siguiente.previousElementSibling.previousElementSibling.previousElementSibling;

    if(siguiente){
        e.target.style.display = "none"
        e.target.transition = "display .5s ease";

        siguiente.style.display = "block"
        siguiente.transition = "display .5s ease";

        contrasena.type = "password";
    }


}

function ocultar(e){

    let adyacente = e.target.previousElementSibling;

    let contrasena = adyacente.previousElementSibling.previousElementSibling;

    if(adyacente){
        adyacente.style.display = "block"
        adyacente.transition = "display .5s ease";

        e.target.style.display = "none"
        e.target.transition = "display .5s ease";

        contrasena.type = "text";
    }
  
    
}

