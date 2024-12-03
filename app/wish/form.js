document.addEventListener('DOMContentLoaded', function() {
  function getDomain(url) {
    try {
      const urlParts = new URL(url);
      return urlParts.hostname.replace(/^www\./, '');
    } catch (e) {
      return '';
    }
  }

  const descriptionPreview = document.getElementById('description-preview');
  const urlInput = document.getElementById('url-input');
  const urlPreview = document.getElementById('url-preview');

  descriptionPreview.innerText = document.getElementById('description-input').value;

  const initialUrl = urlInput.value;
  urlPreview.href = initialUrl;
  urlPreview.innerText = getDomain(initialUrl);

  document.getElementById('description-input').addEventListener('input', function() {
    descriptionPreview.innerText = this.value;
  });

  urlInput.addEventListener('input', function() {
    const url = this.value;
    urlPreview.href = url;
    urlPreview.innerText = getDomain(url);
  });

  document.getElementById('image-input').addEventListener('change', function() {
    const file = this.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
      document.getElementById('image-preview').src = event.target.result;
    };
    reader.readAsDataURL(file);
  });
});
