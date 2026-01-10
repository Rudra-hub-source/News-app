import { listArticles, createArticle } from './service.js'
import { showAlert } from './alert.js'

let currentPage = 1;
let currentQuery = '';
let currentQuery = '';

function renderCard(it){
  const date = new Date(it.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  return `<article class="bg-dark-card rounded-xl shadow-lg hover:shadow-xl transition duration-300 overflow-hidden border border-dark-border">
    <div class="p-6">
      <div class="flex items-start justify-between mb-4">
        <h2 class="text-xl font-bold text-white leading-tight hover:text-orange-400 transition duration-200">
          <a href="/articles/article/${it.id}" class="block">${it.title}</a>
        </h2>
      </div>

      <div class="flex items-center text-sm text-gray-400 mb-4">
        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
        </svg>
        <span class="font-medium">${it.author || 'Anonymous'}</span>
        <span class="mx-2">•</span>
        <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"></path>
        </svg>
        <span>${date}</span>
      </div>

      <p class="text-gray-300 line-clamp-3 mb-4">
        ${it.content.length > 150 ? it.content.substring(0, 150) + '...' : it.content}
      </p>

      <div class="flex items-center justify-between">
        <a href="/articles/article/${it.id}"
           class="inline-flex items-center px-4 py-2 bg-gradient-to-r from-orange-500 to-red-500 text-white text-sm font-medium rounded-lg hover:from-orange-600 hover:to-red-600 transition duration-200">
          <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"></path>
            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"></path>
          </svg>
          Read More
        </a>

        <div class="flex space-x-2">
          <a href="/articles/edit/${it.id}"
             class="p-2 text-yellow-400 hover:bg-gray-700 rounded-lg transition duration-200"
             title="Edit">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z"></path>
            </svg>
          </a>

          <button onclick="deleteArticle(${it.id})"
                  class="p-2 text-red-400 hover:bg-gray-700 rounded-lg transition duration-200"
                  title="Delete">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </article>`;
}

function renderPagination(meta){
  const container = document.getElementById('pagination');
  if(!container) return;
  const {page, per_page, total} = meta;
  const totalPages = Math.ceil(total / per_page) || 1;

  if(totalPages <= 1) {
    container.innerHTML = '';
    return;
  }

  let html = '<div class="flex items-center justify-center space-x-2">';

  // Previous button
  if(page > 1) {
    html += `<button data-page="${page - 1}" class="px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg hover:bg-gray-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200 text-gray-200">
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path>
      </svg>
    </button>`;
  }

  // Page numbers
  const startPage = Math.max(1, page - 2);
  const endPage = Math.min(totalPages, page + 2);

  if(startPage > 1) {
    html += `<button data-page="1" class="px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg hover:bg-gray-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200 text-gray-200">1</button>`;
    if(startPage > 2) {
      html += '<span class="px-2 py-2 text-gray-400">...</span>';
    }
  }

  for(let p = startPage; p <= endPage; p++){
    html += `<button data-page="${p}" class="px-3 py-2 ${p === page ? 'bg-gradient-to-r from-orange-500 to-red-500 text-white' : 'bg-gray-800 border border-gray-600 hover:bg-gray-700 text-gray-200'} rounded-lg focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200">${p}</button>`;
  }

  if(endPage < totalPages) {
    if(endPage < totalPages - 1) {
      html += '<span class="px-2 py-2 text-gray-400">...</span>';
    }
    html += `<button data-page="${totalPages}" class="px-3 py-2 bg-gray-800 border border-gray-600 rounded-lg hover:bg-gray-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200 text-gray-200">${totalPages}</button>`;
  }

  // Next button
  if(page < totalPages) {
    html += `<button data-page="${page + 1}" class="px-4 py-2 bg-gray-800 border border-gray-600 rounded-lg hover:bg-gray-700 focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 transition duration-200 text-gray-200">
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path>
      </svg>
    </button>`;
  }

  html += '</div>';
  container.innerHTML = html;

  container.querySelectorAll('button[data-page]').forEach(b => {
    b.addEventListener('click', () => {
      const p = parseInt(b.dataset.page, 10);
      currentPage = p;
      initIndex();
    });
  });
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
