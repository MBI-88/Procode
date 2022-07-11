'use strict'

function goGet(urlget){
    fetch(urlget,{
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'text/html; char set=UTF-8',
        },
        mode: 'same-origin',
        cache: 'default',
        credentials: 'same-origin',
    
    }).then(response => response.text())
    .then(html => {
        document.getElementById('body-content').innerHTML = html
    
        
    }).catch(reject => console.log(reject))
}

function login(event){
    document.getElementById('modaltitle').innerHTML = 'Entrar'
    goGet('../login/');
}

function register(event){
    document.getElementById('modaltitle').innerHTML = 'Registrarse'
    goGet('../register/');
}

function deleteitem(event){
    const pk = event.target.dataset.pk
    document.getElementById('modaltitle').innerHTML = 'Borrar articulo'
    document.getElementById('body-content').innerHTML = '<h5>Vuelva a intentarlo</h5>'
    while (pk == undefined) {
        pk = document.getElementById(event.target.id).dataset.pk
    }
    goGet('../delete/item/'+pk+'/');
}

function deleteprofile(event){
    document.getElementById('modaltitle').innerHTML = 'Eliminar cuenta'
    goGet('../delete/profile/');
}


function itemdetail(event){
    // Union item-{{pk }} forman el id
    const pk = event.target.dataset.pk
    document.getElementById('modaltitle').innerHTML = 'Articulo'
    document.getElementById('body-content').innerHTML = '<h5>Vuelva a intentarlo</h5>'
    while (pk == undefined) {
       pk =  document.getElementById(event.target.id).dataset.pk
       
    }
    goGet('../shoping/'+pk+'/');
}





