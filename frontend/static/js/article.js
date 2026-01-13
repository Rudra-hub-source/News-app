import './env.js'
import { initIndex } from './pageController.js'

// Initialize index controller if #app element present
document.addEventListener('DOMContentLoaded', ()=>{
  if(document.getElementById('app')){
    initIndex();
  }
});

// simple routechange listener
window.addEventListener('routechange', (e)=>{
  if(document.getElementById('app')) initIndex();
});
