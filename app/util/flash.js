function setupFlashMessagesDismissal() {
  const flashMessages = document.getElementById('flash-messages');
  
  if (flashMessages) {
    const dismissFlashMessages = () => {
      setTimeout(() => {
        flashMessages.style.opacity = '0';
        setTimeout(() => {
          flashMessages.style.visibility = 'hidden';
          flashMessages.style.opacity = '1';
        }, 500);
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
  setupFlashMessagesDismissal();
});
