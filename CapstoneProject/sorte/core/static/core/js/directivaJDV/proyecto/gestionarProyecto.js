document.addEventListener('DOMContentLoaded', () => {

    const formulario = document.querySelectorAll('.formulario__solicitudes');

    formulario.forEach(form => {
        form.addEventListener('submit', (event) => {
            const aceptar = form.querySelector('.main__aceptar');
            const rechazar = form.querySelector('.main__rechazar');
            const loadAceptar = form.querySelector('.load__aceptar');
            const loadRechazar = form.querySelector('.load__rechazar');

            if (event.submitter === aceptar) {
                aceptar.style.display = 'none';
                loadAceptar.style.display = 'flex';
            } else if (event.submitter === rechazar) {
                rechazar.style.display = 'none';
                loadRechazar.style.display = 'flex';
            }
        });
    });
})