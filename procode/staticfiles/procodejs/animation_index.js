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
const elementCarousel = document.getElementById('img-inter1')

// Animations
function animationOne() {
    elementCarousel.children[0].children[0].className = 'image-carousel img-fluid rounded-pill w-75 h-75 procode-pres2'
    elementCarousel.children[0].children[0].hidden = false
    for (let i = 1; i < elementCarousel.children.length; i++) {
        const child = elementCarousel.children[i].children[0]
        child.className = 'image-carousel img-fluid rounded-pill w-75 h-75'
        child.hidden = false
    }
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

