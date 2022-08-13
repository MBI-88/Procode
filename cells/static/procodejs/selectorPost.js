'use strict'

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
        case 'changepassword':
            goPost(postselect,'../register/changepassword/','../index/');
            break;
        case 'deleteprofile':
            goPost(postselect,'../delete/profile/','../index/');
            break;
        case 'restorepassword':
            goPost(postselect,'../restore/password/', '../index/');
            break;
        case 'deleteprofile':
            goPost(postselect,'/delete/profile/','../index/');
            break;
        case 'deleteitem':
            goPost(postselect,'/delete/item/'+postselect.dataset.pk+'/','../profile/')
    }
}


window.addEventListener('submit',postSelector)