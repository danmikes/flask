document.addEventListener('DOMContentLoaded', function() {
  function getDomain(url) {
    try {
      const urlParts = new URL(url);
      return urlParts.hostname.replace('www.', '');
    } catch (e) {
      return '';
    }
  }

  const descriptionInput = document.getElementById('description-input');
  const descriptionPreview = document.getElementById('description-preview');
  const urlInput = document.getElementById('url-input');
  const urlPreview = document.getElementById('url-preview');
  const fileName = document.getElementById('file-name');
  const imageInput = document.getElementById('image-input');
  const imagePreview = document.getElementById('image-preview');
  const addBtn = document.getElementById('add-image-btn');
  const deleteBtn = document.getElementById('delete-image-btn');

  descriptionPreview.innerText = document.getElementById('description-input').value;
  const initialUrl = urlInput.value;
  urlPreview.href = initialUrl;
  urlPreview.innerText = getDomain(initialUrl);

  descriptionInput.addEventListener('input', function() {
    descriptionPreview.innerText = this.value;
  });

  urlInput.addEventListener('input', function() {
    const url = this.value;
    urlPreview.href = url;
    urlPreview.innerText = getDomain(url);
  });

  addBtn.addEventListener('click', function() {
    imageInput.click()
  });

  imageInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      const file = this.files[0]
      fileName.value = file.name;

      const reader = new FileReader();
      reader.onload = function(event) {
        imagePreview.src = event.target.result;
      };
      reader.readAsDataURL(file);
      deleteBtn.removeAttribute('disabled');
    } else {
      fileName.value = 'No file';
      deleteBtn.setAttribute('disabled');
      imagePreview.src = '';
    }
  });

  deleteBtn.addEventListener('click', function() {
    if (!deleteBtn.hasAttribute('disabled')) {
      if (confirm('Delete this image?')) {
        imageInput.value = '';
        fileName.value = 'No file';
        imagePreview.src = '';
        deleteBtn.setAttribute('disabled', true);

        fetch(`/util/file/delete/${wishId}`, { method: 'GET' })
        .then(response => {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(data => {
          if (data.success) {
            alert('Image deleted');
          } else {
            alert('Image not deleted');
          }
        })
        .catch(error => {
          console.error('Error deleting image:', error);
          alert('An error occurred at image deletion');
        });

        const deleteForm = document.getElementById('delete-form');
        deleteForm.submit();
      }
    }
  });
});
