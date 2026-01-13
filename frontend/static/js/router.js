// Very small client-side router placeholder
export function navigate(path){
  history.pushState({}, '', path);
  // dispatch a simple event
  window.dispatchEvent(new CustomEvent('routechange', {detail: {path}}));
}

window.addEventListener('popstate', ()=>{
  window.dispatchEvent(new CustomEvent('routechange',{detail:{path: location.pathname}}));
});
