'use strict'

// Commun Variables
const dict = {
    'block-1': document.getElementById('mainSlider').offsetTop,
    'block-2': document.getElementById('block-2').offsetTop,
    'middle-block': document.getElementById('middle-block').offsetTop,
}
const flag = {
    'flag-1': false,
    'flag-2': false,
    'flag-3': false,
}
const element4 = document.getElementById('img-inter1')
const stringClass = 'image-carousel img-fluid rounded-pill w-75 h-75'

// Animations
function animationOne() {
    for (let i = 0; i < element4.children.length; i++) {
        const child = element4.children[i].children[0]
        child.hidden = false
        child.classList.add('procode-pres3')
    }

    const element3 = document.getElementById('text-inter1')
    element3.hidden = false
    element3.classList.add('procode-pres3')

}
function animationTwo() {
    const element3 = document.getElementById('text-inter2')
    element3.hidden = false
    element3.className += ' procode-pres5'
    const element4 = document.getElementById('img-inter2')
    element4.hidden = false
    element4.classList.add('procode-pres6')
}
function animationThree() {
    const element = document.getElementById('text-bg-2')
    element.hidden = false
    element.classList.add('text-middle-2')

}

// Wrappers

const handleScroll = async () => {
    if (dict["block-1"] - 500 < document.documentElement.scrollTop && !flag['flag-1']) {
        animationOne(flag['flag-1'])
        flag['flag-1'] = true
        for (let i = 0; i < element4.children.length; i++) {
            const child = element4.children[i].children[0]
            child.className = stringClass
        }
    }
    if (dict["block-2"] - 500 < document.documentElement.scrollTop && !flag['flag-2']) {
        animationTwo(flag['flag-2'])
        flag['flag-2'] = true
    }
    if (dict["middle-block"] - 700 < document.documentElement.scrollTop && !flag['flag-3']) {
        animationThree(flag['flag-3'])
        flag['flag-3'] = true
    }
    if (flag['flag-1'] && flag['flag-2'] && flag['flag-3']) {
        window.removeEventListener('scroll', handleScroll, false)
    }
}

// Handlers

window.addEventListener('scroll', handleScroll)

