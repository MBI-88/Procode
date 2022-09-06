'use strict'

const dict = {
    'block-1': document.getElementById('block-1').offsetTop,
    'block-2': document.getElementById('block-2').offsetTop,
    'middle-block': document.getElementById('middle-block').offsetTop,
}
function animationOne(){ 
    const element4 = document.getElementById('img-inter1')
    element4.hidden = false
    element4.className += ' procode-pres3'
    const element3 = document.getElementById('text-inter1')
    element3.hidden = false
    element3.className += ' procode-pres3'
    
}
function animationTwo(){
    const element3 = document.getElementById('text-inter2')
    element3.hidden = false
    element3.className += ' procode-pres5'
    const element4 = document.getElementById('img-inter2')
    element4.hidden = false
    element4.className += ' procode-pres6'
}
function animationThree(){
    const element = document.getElementById('text-bg-2')
    element.hidden = false
    element.className += ' text-middle-2'

}
window.addEventListener('scroll',e => {
   if (dict["block-1"] - 500 < document.documentElement.scrollTop){
    animationOne()
   }
   if (dict["block-2"] - 500 < document.documentElement.scrollTop){
    animationTwo()
   }
   if (dict["middle-block"] - 700 < document.documentElement.scrollTop){
    animationThree()
   }
})

