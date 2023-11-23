import Swal from "../../../../node_modules/sweetalert2/src/sweetalert2.js";

import { format, validate, clean, getCheckDigit } from "../rut/index.js";

const formulario = document.querySelector('#formulario');

const rut = document.querySelector('#rut');
const nombre = document.querySelector('#nombre');
const apellido = document.querySelector('#apellido');
const direccion = document.querySelector('#direccion');
const fechaNacimiento = document.querySelector('#fechaNacimiento');
const correo = document.querySelector('#correo');
const genero = document.querySelector('#genero');
const contrasena1 = document.querySelector('#password1');
const contrasena2 = document.querySelector('#password2');

const visualizar = document.querySelectorAll('.formulario__visualizar');
const oculto = document.querySelectorAll('.formulario__oculto');


const submit = document.querySelector('.formulario__iniciar');

const cargar = document.querySelector('.load');

let captchaReady = false;

window.thecallback = function () {
    captchaReady = true;
    validarCampos()
};

window.Expiredcallback = function(){
    captchaReady = false;
    validarCampos();
}

document.addEventListener('DOMContentLoaded', () => {

    submit.disabled = true;
    submit.style.background = "#DE3D3D";
    submit.style.cursor = "not-allowed";
    submit.value = "Completar Inscripción";

    formulario.addEventListener('input', validarCampos)

    // Escuchar eventos de entrada y validar
    apellido.addEventListener("input", () => {
        
        const valor = apellido.value;
        if (/[^\p{L}\s]/u.test(valor)) {
            // Si contiene caracteres no permitidos, eliminarlos
            apellido.value = valor.replace(/[^\p{L}\s]/gu, "");
        }

    });

    // Escuchar eventos de entrada y validar
    nombre.addEventListener("input", () => {
        
        const valor = nombre.value;
        if (/[^\p{L}\s]/u.test(valor)) {
            // Si contiene caracteres no permitidos, eliminarlos
            nombre.value = valor.replace(/[^\p{L}\s]/gu, "");
        }
        
    });

    correo.addEventListener('focus', focusElement);
    correo.addEventListener('blur', blurElement);
    fechaNacimiento.addEventListener('focus', focusElement);
    fechaNacimiento.addEventListener('blur', blurElement);

    formulario.addEventListener('submit', e => {

        // const fechaActual = new Date().getTime();
        // const fechaFormato = new Date(fechaNacimiento.value).getTime();

        // const fechaMilisegundos = fechaActual - fechaFormato;

        // const milisegundosEnUnAnio = 365.25 * 24 * 60 * 60 * 1000;
        // const fechaEnAños = parseInt(fechaMilisegundos / milisegundosEnUnAnio);

        // console.log((fechaEnAños));
        // const formato = format(rut.value);
        // const validar = validate(rut.value);

        // // Expresión regular para validar el formato de correo electrónico
        // const regexCorreo = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        submit.disabled = true;
        submit.style.background = "#DE3D3D";
        submit.style.cursor = "not-allowed";
        submit.value = "Completar Inscripción";

        cargar.style.display = 'flex';
        submit.style.display = 'none';

        

            // console.log(regexCorreo.test(correo.value));

            //     const Toast = Swal.mixin({
            //         toast: true,
            //         position: 'top-end',
            //         showConfirmButton: true,
            //         timer: 6000,
            //         width: "31.25rem",
            //         timerProgressBar: true,
            //         didOpen: (toast) => {
            //           toast.addEventListener('mouseenter', Swal.stopTimer)
            //           toast.addEventListener('mouseleave', Swal.resumeTimer)
            //         }
            //       })
                  
            //     Toast.fire({
            //         icon: 'info',
            //         title: 'Su inscripción será revisada por nuestro equipo. Por favor, esté atento a su correo.',
                   
            //     });
    
    
            //     rut.value = '';
            //     nombre.value = '';
            //     apellido.value = '';
            //     correo.value = '';
            //     genero.value = '';
            //     direccion.value = '';
            //     contrasena1.value = '';
            //     contrasena2.value = '';
            //     fechaNacimiento.value = '';

            //     submit.disabled = true;
            //     submit.style.background = "#DE3D3D";
            //     submit.style.cursor = "not-allowed";
            //     submit.value = "Completar Inscripción";
            

            // if(fechaEnAños < 18){
            //     const Toast = Swal.mixin({
            //         toast: true,
            //         position: 'top-end',
            //         showConfirmButton: true,
            //         timer: 4000,
            //         width: "31.25rem",
            //         timerProgressBar: true,
            //         didOpen: (toast) => {
            //           toast.addEventListener('mouseenter', Swal.stopTimer)
            //           toast.addEventListener('mouseleave', Swal.resumeTimer)
            //         }
            //       })
                  
            //     Toast.fire({
            //         icon: 'error',
            //         title: 'Su inscripción presenta errores con la fecha ingresada, por favor ingrese la fecha correctamente.',
                   
            //     });
                

            //     fechaNacimiento.style.borderBottom = "0.125rem solid red";
            // }

       



        
        // const limpiar = clean(rut.value);
        // const digitoV = getCheckDigit(rut.value);

        
        // console.log(limpiar);
        // console.log(digitoV);
    })

    
    

    


    visualizar.forEach((e, i) => {
        e.addEventListener('click', mostrar);
        
    }); 


    oculto.forEach((e, i) => {
            
        e.addEventListener('click', ocultar);
    }); 
        
    
    
});

function validarCampos(){
    const formato = format(rut.value);
    const validar = validate(rut.value);


    const campos = [rut.value,nombre.value,apellido.value,fechaNacimiento.value,correo.value,genero.value,direccion.value,contrasena1.value,contrasena2.value]

    const resultado = campos.every(campo => campo !== '');

    if(!resultado){
        submit.disabled = true;
        submit.style.background = "#DE3D3D";
        submit.style.cursor = "not-allowed";
        submit.value = "Completar Inscripción";
    } else {

        if(formato && validar === true && resultado && captchaReady === true){
            
            submit.disabled = false;
            submit.style.background = "#1464f6";
            submit.style.cursor = "pointer";
            submit.value = "Envíar Inscripción";
        } else {
            submit.disabled = true;
            submit.style.background = "#DE3D3D";
            submit.style.cursor = "not-allowed";
            submit.value = "Completar Inscripción";
        }
    }
}

function focusElement(e){
    e.target.style.borderBottom = "0.125rem solid #1464f6";
}

function blurElement(e){
    e.target.style.borderBottom = "0.125rem solid #00000049";
}


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