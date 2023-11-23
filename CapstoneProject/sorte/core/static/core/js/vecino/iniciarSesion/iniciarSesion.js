import Swal from "../../../../node_modules/sweetalert2/src/sweetalert2.js";
import { format, validate, clean, getCheckDigit } from "../rut/index.js";

const formulario = document.querySelector('#formulario');
const rut = document.querySelector('#rut');
const contrasena = document.querySelector('#password');
const submit = document.querySelector('#iniciarSesion');
const visualizar = document.querySelector('.formulario__visualizar');
const oculto = document.querySelector('.formulario__oculto');

const cargar = document.querySelector('.load');

let captchaReady = false;

window.thecallback = function () {
    captchaReady = true;
    validarCampos();
};

window.Expiredcallback = function(){
    captchaReady = false;
    validarCampos();
}

document.addEventListener('DOMContentLoaded', () => {



  submit.disabled = true;
  submit.style.background = "#DE3D3D";
  submit.style.cursor = "not-allowed";
  submit.value = "No puedes Iniciar";

  formulario.addEventListener('input', validarCampos);

  formulario.addEventListener('submit', e => {
   

      const formato = format(rut.value);
      const validarRUT = validate(rut.value);
      const contrasenaValida = contrasena.value !== '';

      
        submit.style.display = "none";
        cargar.style.display = 'flex';
      
  });


  visualizar.addEventListener('click', mostrar);
  oculto.addEventListener('click', ocultar);
});

function validarCampos() {
    const formato = format(rut.value);
    const validarRUT = validate(rut.value);
    const contrasenaValida = contrasena.value !== '';

    if (formato && validarRUT && contrasenaValida && captchaReady === true) {
      submit.disabled = false;
      submit.style.background = "#1464f6";
      submit.style.cursor = "pointer";
      submit.value = "Iniciar Sesión";
    } else {
      submit.disabled = true;
      submit.style.background = "#DE3D3D";
      submit.style.cursor = "not-allowed";
      submit.value = "No puedes Iniciar";
    };
};

function mostrar(){
  oculto.style.display = "block"
  oculto.transition = "display .5s ease";

  visualizar.style.display = "none"
  visualizar.transition = "display .5s ease";

  contrasena.type = "password";
};

function ocultar(){
  visualizar.style.display = "block"
  visualizar.transition = "display .5s ease";

  oculto.style.display = "none"
  oculto.transition = "display .5s ease";

  contrasena.type = "text";
};



