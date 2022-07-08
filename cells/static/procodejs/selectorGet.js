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
        document.querySelector('.modal-body').innerHTML = html
    
        
    }).catch(reject => console.log(reject))
}

function login(event){
    goGet('../login/');
}

function register(event){
    goGet('../register/');
}

function deleteitem(event){
    const pk = event.target.dataset.pk
    goGet('../delete/item/'+pk+'/');
}

function deleteprofile(event){
    goGet('../delete/profile/');
}


function itemdetail(event){
    const pk = event.target.dataset.pk
    goGet('../shoping/'+pk+'/');
}





