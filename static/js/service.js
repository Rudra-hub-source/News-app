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

export async function listArticles(q, page=1, per_page=10){
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (page) params.set('page', page);
  if (per_page) params.set('per_page', per_page);
  const url = `${env.API_BASE}/articles?${params.toString()}`;
  const res = await fetch(url);
  return res.json();
}

export async function createArticle(form){
  const res = await fetch(`${env.API_BASE}/articles`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(form)});
  return res.json();
}

export async function uploadFile(file){
  const fd = new FormData();
  fd.append('file', file);
  const res = await fetch(`${env.API_BASE}/uploads`, { method: 'POST', body: fd});
  return res.json();
}
