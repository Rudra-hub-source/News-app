import env from './env.js'

export async function apiFetch(path, opts={}){
  const url = env.API_BASE + path;
  const res = await fetch(url, opts);
  if (!res.ok) {
    const body = await res.text();
    throw new Error(body || res.statusText);
  }
  return res.json();
}

export async function listArticles(q){
  const url = '/api/articles' + (q ? '?q='+encodeURIComponent(q):'');
  const res = await fetch(url);
  return res.json();
}

export async function createArticle(form){
  const res = await fetch('/api/articles', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(form)});
  return res.json();
}
