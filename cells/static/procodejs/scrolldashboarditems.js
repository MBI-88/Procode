/*Evento scroll en la tienda */
let page = 1
let empty_page = false
let blocke_request = false

function GetFetch(page,search){
    fetch('?page='+page+'&'+'search='+search,{
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'text/html; char set=UTF-8',
        },
        mode: 'same-origin',
        cache: 'default',
        credentials: 'same-origin',

    }).then(response => response.text()).then((html) =>{
        if (html == ''){
            empty_page = true
        }
        else{
            blocke_request = false
            document.getElementById('items-ajax').insertAdjacentHTML('beforeend',html)
        }
    })
}

function scrollInf(){
    const search = document.getElementById('id-search').value
    const margin = document.body.clientHeight - window.innerHeight - 200
    let search_valid = ''
    if (search.lehgth > 4) {search_valid = search}
    
    if (window.screenTop > margin && empty_page == false && blocke_request == false){
        blocke_request = true
        page += 1
        GetFetch(page,search_valid)
        
    }
}
window.addEventListener('scroll',scrollInf)

function takeKeypress(event){
    const search = event.target.value
    if (search.lehgth > 4){
        document.getElementById('items-ajax').innerHTML = ''
        GetFetch(1,search)
    }
}