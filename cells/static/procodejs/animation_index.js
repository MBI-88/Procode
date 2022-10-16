'use strict'

// Commun Variables
const dict = {
    'block-1': document.getElementById('block-1').offsetTop,
    'block-2': document.getElementById('block-2').offsetTop,
}
const flag = {
    'flag-1': false,
    'flag-2': false,
}

// Animations
function animationOne() {
    const imageproductivity = document.getElementById('img-inter1')
    imageproductivity.classList.add('procode-pres2')
    imageproductivity.hidden = false
    const element = document.getElementById('text-inter1')
    element.classList.add('procode-pres2')
    element.hidden = false
}
function animationTwo() {
    const element = document.getElementById('text-bg-2')
    element.classList.add('procode-pres3')
    element.hidden = false
}

// Wrappers

const handleScroll = async () => {
    if (dict["block-1"] - 700 < document.documentElement.scrollTop && !flag['flag-1']) {
        animationOne()
        flag['flag-1'] = true
    }
    if (dict["block-2"] - 700 < document.documentElement.scrollTop && !flag['flag-2']) {
        animationTwo()
        flag['flag-2'] = true
        elementCarousel.children[0].children[0].classList.remove('procode-pres2')
    }
    if (flag['flag-1'] && flag['flag-2']) {
        window.removeEventListener('scroll', handleScroll, false)
    }
}

// Handlers

window.addEventListener('scroll', handleScroll)

const scrollText = async () => {
    let textBlock = document.getElementById('text-who')
    textBlock.className = (textBlock.offsetTop - 700 < document.documentElement.scrollTop &&
        document.documentElement.scrollTop < textBlock.offsetTop - 150) ? 
        'text-who-apper fs-4 fw-lighter' : 'text-who-hidde fs-4 fw-lighter'
}

window.addEventListener('scroll', scrollText)