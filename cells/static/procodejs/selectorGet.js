'use strict'

const detail = /^detail/
const del = /^delete/

async function goGet(urlget) {
    await fetch(urlget, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'text/html; charset=UTF-8',
        },
        mode: 'same-origin',
        cache: 'default',
        credentials: 'same-origin',

    }).then(response => response.text())
        .then(html => {
            document.getElementById('body-content').innerHTML = html

        }).catch(reject => reject)
}

async function login() {
    document.getElementById('modaltitle').innerHTML = 'Login'
    await goGet('../login/')
}

async function register() {
    document.getElementById('modaltitle').innerHTML = 'Register'
    await goGet('../register/')
}

async function deleteitem(target) {
    const pk = target.dataset.pk
    document.getElementById('modaltitle').innerHTML = 'Delete item'
    while (pk === undefined) {
        pk = document.getElementById(target.id).dataset.pk
    }
    await goGet('../delete/item/' + pk + '/')
}

async function deleteprofile() {
    document.getElementById('modaltitle').innerHTML = 'Delete account'
    await goGet('../delete/profile/');
}

async function itemdetail(target) {
    // Union item-{{pk }} forman el id
    const pk = target.dataset.pk
    document.getElementById('modaltitle').innerHTML = 'Item'
    while (pk === undefined) {
        pk = document.getElementById(target.id).dataset.pk
    }
    await goGet('../shopping/'+ pk +'/')
}


async function changepassword() {
    document.getElementById('modaltitle').innerHTML = 'Change password'
    await goGet('../register/changepassword/')

}

async function restorepassword() {
    document.getElementById('modaltitle').innerHTML = 'Restore password'
    await goGet('../restore/password/')
}


// Navbar scroll event

window.addEventListener('scroll', async () => {
    const navbar = document.getElementById('navbar')
    navbar.className = navbar.offsetTop < document.documentElement.scrollTop ?
        'navbar navbar-expand-lg navbar-light navbar-onscroll' : 'navbar navbar-expand-lg navbar-light navbar-bg'
})

const handleSelect = (target) => {
    if (del.test(target.id)) deleteitem(target)
    if (detail.test(target.id)) itemdetail(target)
    if (target.id === 'deleteprofile') deleteprofile()
    if (target.id === 'restorepassword') restorepassword()
    if (target.id === 'changepassword') changepassword()
    if (target.id === 'login') login()
    if (target.id === 'register') register()
}

window.addEventListener('show.bs.modal', event => {
    window.addEventListener('click', e => {
        const target = e.target
        switch (target.tagName) {
            case "A":
                handleSelect(target)
                break;
            case "svg":
                const targetSvg =  target.parentNode
                handleSelect(targetSvg)
                break;
            case "path":
                const targetPath = target.parentNode.parentNode
                handleSelect(targetPath)
                break;
        }
    })
    document.getElementById('modaltitle').innerHTML = ''
    document.getElementById('body-content').innerHTML = ''
    window.removeEventListener('click', e => { })
})
