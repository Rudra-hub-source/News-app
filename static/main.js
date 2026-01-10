function ajaxDelete(articleId) {
  if (!confirm('Delete this article?')) return;
  fetch('/delete/' + articleId, { method: 'POST' })
    .then(r => {
      if (r.ok) location.href = '/';
      else alert('Delete failed');
    })
    .catch(() => alert('Network error'));
}
