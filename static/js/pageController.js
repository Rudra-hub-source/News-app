import { listArticles, createArticle } from './service.js'
import { showAlert } from './alert.js'

let currentPage = 1;
let currentQuery = '';

function renderCard(it){
  return `<article class="bg-white p-5 rounded shadow mb-4">
    <h2 class="text-xl font-semibold mb-2">${it.title}</h2>
    <p class="text-sm text-gray-600 mb-3">By ${it.author || 'Unknown'}</p>
    <div class="text-gray-700">${it.created_at}</div>
  </article>`;
}

function renderPagination(meta){
  const container = document.getElementById('pagination');
  if(!container) return;
  const {page, per_page, total} = meta;
  const totalPages = Math.ceil(total / per_page) || 1;
  let html = '';
  for(let p=1;p<=totalPages;p++){
    html += `<button data-page="${p}" class="px-3 py-1 mx-1 ${p===page ? 'bg-gray-800 text-white' : 'bg-white'} rounded">${p}</button>`;
  }
  container.innerHTML = html;
  container.querySelectorAll('button[data-page]').forEach(b=> b.addEventListener('click', ()=>{
    const p = parseInt(b.dataset.page,10);
    currentPage = p;
    initIndex();
  }));
}

export async function initIndex(page=1, q=''){
  try{
    currentPage = page || currentPage;
    currentQuery = q || currentQuery;
    const resp = await listArticles(currentQuery, currentPage, 6);
    const app = document.getElementById('app');
    if(!app) return;
    const items = (resp.data && resp.data.items) || [];
    app.innerHTML = items.map(it => renderCard(it)).join('');
    if(resp.data && resp.data.meta) renderPagination(resp.data.meta);
  }catch(err){
    showAlert('Failed to load articles', 'error');
  }
}

export async function handleCreate(form){
  try{
    const data = await createArticle(form);
    showAlert('Article created');
    return data;
  }catch(err){
    showAlert('Create failed: '+err.message, 'error');
  }
}

// wire search
document.addEventListener('DOMContentLoaded', ()=>{
  const btn = document.getElementById('search-btn');
  const qinput = document.getElementById('search-q');
  if(btn && qinput){
    btn.addEventListener('click', (e)=>{
      e.preventDefault();
      const q = qinput.value.trim();
      currentQuery = q;
      currentPage = 1;
      initIndex();
    });
  }
});
