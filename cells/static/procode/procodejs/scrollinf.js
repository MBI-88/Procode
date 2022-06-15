'use strict'

let page = 1
let empty_page = false
let blocke_request = false

function scrollInf(){
    let margin = document.body.clientHeight - window.innerHeight - 200
    if (window.screenTop > margin && empty_page == false && blocke_request == false){
        blocke_request = true
        page += 1
        fetch('http://localhost:8000/cells/shopin/?page='+ page,{
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'text/html; char set=UTF-8',
            },
            mode: 'same-origin',
            cache: 'default',
            credentials: 'same-origin',

        }).then((response) =>{
            if (response.text() == ''){
                empty_page = true

            }
            else{
                blocke_request = false
                document.getElementById('items').append(response.text())
            }
        })
        
    }
}

window.addEventListener('scroll',scrollInf)