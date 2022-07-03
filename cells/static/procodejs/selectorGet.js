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
        case 'deleteitem-'+pk:
            goGet('../delete/item/?pk='+pk);
            break;
        case 'deleteprofile':
            goGet('../delete/profile/');
            break;
        case 'itemdetail-'+pk:
            goGet('../shoping/'+pk+'/?pk='+pk);
            break;

    }

}








