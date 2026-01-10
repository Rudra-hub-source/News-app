export function showAlert(message, type='info'){
  const id = 'site-alert';
  let el = document.getElementById(id);
  if(!el){
    el = document.createElement('div');
    el.id = id;
    el.className = 'fixed top-4 right-4 max-w-sm';
    document.body.appendChild(el);
  }
  el.innerHTML = `<div class="p-3 rounded shadow ${type==='error' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}">${message}</div>`;
  setTimeout(()=> el.innerHTML='', 4000);
}
