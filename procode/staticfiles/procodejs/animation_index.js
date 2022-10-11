'use strict'

function animationOne(){ 
    document.getElementById('block-1').onmouseover = null
    const element3 = document.getElementById('text-inter1')
    element3.hidden = false
    element3.className += ' procode-pres3'
    
    const element4 = document.getElementById('img-inter1')
    element4.hidden = false
    element4.className += ' procode-pres4'
}

function animationTwo(){
    document.getElementById('block-2').onmouseover = null
    const element3 = document.getElementById('text-inter2')
    element3.hidden = false
    element3.className += ' procode-pres5'
    
    const element4 = document.getElementById('img-inter2')
    element4.hidden = false
    element4.className += ' procode-pres6'
}

function animationThree(){
    document.getElementById('middle-block').onmouseover = null
    const element = document.getElementById('text-bg-2')
    element.hidden = false
    element.className += ' text-middle-2'

}


