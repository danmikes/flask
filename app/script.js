function setActiveTab(tabId) {
  const tabLinks = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');

  tabLinks.forEach(link => link.parentElement.classList.remove('is-active'));
  tabContents.forEach(content => content.classList.remove('is-active'));

  const activeLink = document.querySelector(`[href="#${tabId}"]`);
  const activeContent = document.getElementById(tabId);

  if (activeLink && activeContent) {
    activeLink.parentElement.classList.add('is-active');
    activeContent.classList.add('is-active');
    localStorage.setItem('activeTab', tabId);

    const newWishButton = activeContent.querySelector('.card-new');
    if (newWishButton) {
      newWishButton.style.display = newWishButton.dataset.owner === "True" ? 'block' : 'none';
    }
  }
}

function initializeTabs(defaultTab) {
  const savedTab = localStorage.getItem('activeTab');

  if (savedTab && document.getElementById(savedTab)) {
    setActiveTab(savedTab);
  } else {
    setActiveTab(defaultTab);
  }

  const tabLinks = document.querySelectorAll('.tab-link');
  tabLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const tabId = link.getAttribute('href').substring(1);
      setActiveTab(tabId);
    });
  });
}

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

function setupFlashMessagesDismissal() {
  const flashMessages = document.getElementById('flash-messages');
  
  if (flashMessages) {
    const dismissFlashMessages = () => {
      setTimeout(() => {
        flashMessages.style.opacity = '0';
        setTimeout(() => {
          flashMessages.style.visibility = 'hidden';
          flashMessages.style.opacity = '1'; // Reset opacity for next message
        }, 500); // Wait for fade out to complete
      }, 2000);
    };

    dismissFlashMessages();

    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
          dismissFlashMessages();
        }
      });
    });

    observer.observe(flashMessages, { childList: true });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const burgers = document.querySelectorAll('.navbar-burger');
  burgers.forEach(burger => {
    burger.addEventListener('click', () => {
      const target = burger.dataset.target;
      const menu = document.getElementById(target);

      burger.classList.toggle('is-active');
      menu.classList.toggle('is-active');
    });
  });

  const defaultTab = `tab-${currentUserId}`;
  initializeTabs(defaultTab);

  setupFlashMessagesDismissal();
});
