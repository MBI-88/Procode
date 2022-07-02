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
    const pk = event.target.dataset.pk
    switch (id){
        case 'login':
            goGet('../login/');
            break;
        case 'register':
            goGet('../register/');
            break;
        case 'profile':
            goGet('../login/');
            break;
        case 'createitem':
            goGet('../create/item/');
            break;
        case 'updateitem-'+pk:
            goGet('../update/item/<'+pk+'>/');
            break;
        case 'deleteitem-'+pk:
            goGet('../delete/item/<'+pk+'>/');
            break;
        case 'updateprofile':
            goGet('../update/profile/<'+pk+'>/');
            break;
        case 'deleteprofile':
            goGet('../delete/profile/<'+pk+'>/');
            break;
        case 'itemdetail-'+pk:
            goGet('../shoping/<'+pk+'>/');
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
    // Selector de post
    const postselect = document.getElementsByTagName('form')[0]
    switch (postselect.id){
        case 'login':
            goPost(postselect,'../login/','../profile/');
            break;
        case 'register':
            goPost(postselect,'../register/','../index/');
            break;
        case 'updateprofile':
            goPost(postselect,'../update/profile/<'+postselect.dataset.pk+'>/','../profile/');
            break;
        case 'deleteprofile':
            goPost(postselect,'../delete/profile/<'+postselect.dataset.pk+'>/','../index/');
            break;
        case 'createitem':
            goPost(postselect,'../create/item/','../profile/');
            break;
        case 'deleteitem':
            goPost(postselect,'../delete/item/<'+postselect.dataset.pk+'>/','../profile/');
            break;
        case 'updateitem':
            goPost(postselect,'../update/item/<'+postselect.dataset.pk+'>/','../profile/');
            break;
            
    }

}


window.addEventListener('submit',postSelector)



