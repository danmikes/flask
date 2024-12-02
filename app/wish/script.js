document.addEventListener('DOMContentLoaded', function() {
  const tabs = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');

  function setActiveTab(tabId) {
    console.log(`Setting active tab: ${tabId}`);

    tabs.forEach(tab => tab.classList.remove('is-active'));
    tabContents.forEach(content => content.classList.remove('is-active'));

    const selectedTab = document.querySelector(`.tab-link[data-tab="${tabId}"]`);
    const selectedContent = document.getElementById(tabId);

    if (selectedTab && selectedContent) {
      selectedTab.classList.add('is-active');
      selectedContent.classList.add('is-active');
      localStorage.setItem('activeTab', tabId);
    } else {
      console.error(`Could not find tab with id: ${tabId}`);
    }
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', function(e) {
      e.preventDefault();
      const tabId = this.getAttribute('data-tab');
      setActiveTab(tabId);
    });
  });

  // Set initial active tab
  const savedTab = localStorage.getItem('activeTab');
  if (savedTab && document.getElementById(savedTab)) {
    setActiveTab(savedTab);
  } else {
    setActiveTab('current-user');
  }
});


function updatePreview() {
  const description = document.getElementById('wishForm').description.value;
  const url = document.getElementById('wishForm').url.value;

  document.getElementById('previewDescription').innerText = description || 'Wish Description';

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
