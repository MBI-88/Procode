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


/*Evento para enviar formulario */
function loginPost(event){
    event.preventDefault()
    let form  = document.querySelector('#loginForm')
    form = new FormData(form)

    console.log(form)
    //onst form = new FormData(event.target)

    /*fetch('../login/',{
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'multipart/form-data',
        },
        mode: 'same-origin',
        cache: 'default',
        credentials: 'same-origin',
        body: form,
    })
    */
}
window.addEventListener('submit',loginPost)



