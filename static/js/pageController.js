import { listArticles, createArticle } from './service.js'
import { showAlert } from './alert.js'

export async function initIndex(){
  try{
    const resp = await listArticles();
    // simple rendering into #app
    const app = document.getElementById('app');
    if(!app) return;
    const items = (resp.data || []);
    app.innerHTML = items.map(it => `<div class="p-3 bg-white rounded mb-3"><h3>${it.title}</h3><small>${it.author}</small></div>`).join('');
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
