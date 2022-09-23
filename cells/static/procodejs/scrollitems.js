/*Evento scroll en la tienda */
let page = 1
let empty_page = false
let block_request = false
document.getElementById('id-search').focus()

function GetFetch(page,search){
    fetch('?page='+page+'&search='+search,{
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
            block_request = false
            document.getElementById('items-ajax').insertAdjacentHTML('beforeend',html)
        }
    })
}

async function scrollInf(){
    const search = new String(document.getElementById('id-search').value)
    const itemsajax = document.getElementById('items-ajax')
    const margin = itemsajax.clientHeight - window.innerHeight - 500
    let search_valid = ''
    if (search.length >= 3) {search_valid = search.toString()}
    
    if (itemsajax.scrollHeight > margin && empty_page == false && block_request == false){
        block_request = true
        page += 1
        GetFetch(page,search_valid)
        
    }
}

function takeKeypress(event){
    // analizar empty_page
    const search =  new String(event.target.value)
    document.getElementById('items-ajax').innerHTML = ''
    empty_page = false
    page = 1
    GetFetch(page,search.toString())
    
    if (event.code == 'Backspace' && search.length == 1) {
        location.reload()
    }
    
}
