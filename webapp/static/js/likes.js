(function(){
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
  }

  const csrftoken = getCookie('csrftoken');

  async function toggleLike(postId, liked) {
    const url = `/api/v1/post/${postId}/like/`;
    const resp = await fetch(url, {
      method: liked ? 'DELETE' : 'POST',
      headers: {
        'X-CSRFToken': csrftoken || '',
        'Accept': 'application/json'
      },
      credentials: 'same-origin'
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return resp.json();
  }

  document.addEventListener('click', async function(e){
    const btn = e.target.closest('.post-like-btn[data-post-id]');
    if (!btn) return;
    const postId = btn.dataset.postId;
    const liked = btn.dataset.liked === 'true';
    btn.disabled = true;
    try {
      const data = await toggleLike(postId, liked);
      btn.dataset.liked = String(data.liked);
      const icon = btn.querySelector('i');
      if (icon) icon.className = 'bi ' + (data.liked ? 'bi-heart-fill' : 'bi-heart');
      const counter = document.querySelector(`.post-likes[data-post-id="${postId}"]`);
      if (counter) counter.textContent = data.likes_count;
    } catch (err) {
      console.error(err);
      alert('Не удалось выполнить действие. Возможно, вы не авторизованы.');
    } finally {
      btn.disabled = false;
    }
  });
})();
