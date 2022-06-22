'use strict'

/*Evento para peticion de login */
function loginform(event){
    fetch('../login/',{
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

/* Evento para peticion de registro */
function registerform(event){
    fetch('../register/',{
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

// goPost hace la peticion post por medio de fetch
function goPost(form,urlpost,urlredic){
    const formdata = new URLSearchParams(new FormData(form))

    fetch(urlpost,{
        method: 'POST',
        body: formdata,
        
    }).then(response => response.text())
    .then(html => {
        if (html == 'redirec'){
            window.location.href = urlredic
        }
        document.querySelector('.modal-body').innerHTML = html
    })
    
    
}

/*Evento para enviar formulario */
function postSelector(event){
    event.preventDefault()

    // Selector de post
    const postselect = document.getElementsByTagName('form')[0]
    switch (postselect.id){
        case 'loginForm':
            goPost(postselect,'../login/','../profile/');
            break;
        case 'registerForm':
            goPost(postselect,'../register/','../index/');
            break;
            
    }

}


window.addEventListener('submit',postSelector)



