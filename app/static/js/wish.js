function updatePreview() {
  const description = document.getElementById('wishForm').description.value;
  const url = document.getElementById('wishForm').url.value;

  document.getElementById('previewDescription').innerText = description || 'Your Wish Description Here';
  
  const previewURL = document.getElementById('previewURL');
  if (url) {
      previewURL.innerHTML = `<a href="${url}" target="_blank">${url}</a>`;
  } else {
      previewURL.innerHTML = 'Your URL Here';
  }
}

function updateImagePreview(input) {
  const file = input.files[0];
  const previewImage = document.getElementById('previewImage');
  const previewImageContainer = document.getElementById('previewImageContainer');

  if (file) {
      const reader = new FileReader();
      reader.onload = function(e) {
          previewImage.src = e.target.result;
          previewImageContainer.style.display = 'block';
      };
      reader.readAsDataURL(file);
  } else {
      previewImageContainer.style.display = 'none';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const tabLinks = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');

  tabLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();

      tabLinks.forEach(link => link.parentElement.classList.remove('is-active'));
      tabContents.forEach(content => content.classList.remove('is-active'));

      link.parentElement.classList.add('is-active');
      const targetContent = document.getElementById(link.getAttribute('href').substring(1));
      targetContent.classList.add('is-active');
    });
  });
});
