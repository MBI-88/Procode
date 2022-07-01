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

function getSelector(event){
    const id = event.target.id
    switch (id){
        case 'login':
            goGet('../login/');
            break;
        case 'register':
            goGet('../register/');
            break;
        case 'perfil':
            goGet('../login/');
            break;
    }

}




// goPost hace la peticion post por medio de fetch
function goPost(form,urlpost,urlredic){
    const formdata = new URLSearchParams(new FormData(form))

    fetch(urlpost,{
        method: 'POST',
        body: formdata,
        
    }).then(response => response.text())
    .then(html => {
        if (html == '302'){
            window.location.href = urlredic
        }
        document.querySelector('.modal-body').innerHTML = html
    })
    
    
}

/*Evento para enviar formulario */
function postSelector(event){
    event.preventDefault()
    // crear identificador pra pk en update y delete
    // Selector de post
    const postselect = document.getElementsByTagName('form')[0]
    switch (postselect.id){
        case 'loginForm':
            goPost(postselect,'../login/','../profile/');
            break;
        case 'registerForm':
            goPost(postselect,'../register/','../index/');
            break;
        case 'updateproForm':
            goPost(postselect,'../update/profile/<'+postselect.dataset.updatepro+'>/','../profile/');
            break;
        case 'deleteproForm':
            goPost(postselect,'../delete/profile/<'+postselect.dataset.deletepro+'>/','../index/');
            break;
        case 'createitemForm':
            goPost(postselect,'../create/item/','../profile/');
            break;
        case 'deleteitemForm':
            goPost(postselect,'../delete/item/<'+postselect.dataset.deleteitem+'>/','../profile/');
            break;
        case 'updateitemForm':
            goPost(postselect,'../update/item/<'+postselect.dataset.updateitem+'>/','../profile/');
            break;
            
    }

}


window.addEventListener('submit',postSelector)



