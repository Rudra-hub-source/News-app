function ajaxDelete(articleId) {
  if (!confirm('Are you sure you want to delete this article? This action cannot be undone.')) return;
  fetch('/delete/' + articleId, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  })
    .then(r => {
      if (r.ok) {
        location.reload();
      } else {
        alert('Delete failed. Please try again.');
      }
    })
    .catch(() => alert('Network error. Please check your connection.'));
}

// Make it global for onclick
window.deleteArticle = ajaxDelete;
