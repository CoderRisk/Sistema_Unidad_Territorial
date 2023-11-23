const lista = document.querySelector('#usuario__lista');

const user = document.querySelector('#header__imagen');
const path = document.querySelector('#path-header__imagen');


const userItems = document.querySelectorAll('.usuario__item');


document.addEventListener('DOMContentLoaded', () => {
    
    user.addEventListener('click', iconoClick);
    userItems.forEach(item => {
        item.addEventListener('mouseenter', scaleItem);
        item.addEventListener("mouseleave", unScaleItem);
    })

    document.addEventListener('click', e => {
        if(e.target !== user && e.target !== path){
            
            let items = lista.children;

            for(let i = 0; i < items.length; i++){

                if(items[i].style.display === "block"){

                    items[i].style.display = "none";
                    items[i].style.transition = "display .3s ease";
                }
            }

        }
    })

});


function iconoClick(e){

    let items = lista.children;

    for(let i = 0; i < items.length; i++){

        if(items[i].style.display === ""){

            items[i].style.display = "block";
            items[i].style.transition = "display .3s ease";
           
        } else if (items[i].style.display === "none"){

            items[i].style.display = "block";
            items[i].style.transition = "display .3s ease";

        } else {
            items[i].style.display = "none";
            items[i].style.transition = "display .3s ease";
           
        }
    }
}

function scaleItem(e){
    
    const li = e.target;

    if(li.style.transform === ''){
        li.style.transform = "scale(1.2)";
        li.style.zIndex = "2";
        li.style.transition = "transform .3s ease";

    } else if(li.style.transform === 'scale(1)'){
        li.style.transform = "scale(1.2)";
        li.style.zIndex = "2";
        li.style.transition = "transform .3s ease ";
    };

}

function unScaleItem(e){
    const li2 = e.target;

    if(li2.style.transform !== ''){
        li2.style.transform = "scale(1)";
        li2.style.zIndex = "0";
        li2.style.transition = "transform .3s ease";
    } 
}