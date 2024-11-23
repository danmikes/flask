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

  const tabLinks = document.querySelectorAll('.tab-link');
  const tabContents = document.querySelectorAll('.tab-content');

  function setActiveTab(tabId) {
    tabLinks.forEach(link => link.parentElement.classList.remove('is-active'));
    tabContents.forEach(content => content.classList.remove('is-active'));

    const activeLink = document.querySelector(`[href="#${tabId}"]`);
    const activeContent = document.getElementById(tabId);

    if (activeLink && activeContent) {
      activeLink.parentElement.classList.add('is-active');
      activeContent.classList.add('is-active');
      localStorage.setItem('activeTab', tabId);
    }
  }

  const defaultTab = `tab-${currentUserId}`;
  console.log("Current User:", currentUserId);

  const savedTab = localStorage.getItem('activeTab');

  if (savedTab) {
    setActiveTab(savedTab);
  } else {
    setActiveTab(defaultTab)
  }

  tabLinks.forEach(link => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      const tabId = link.getAttribute('href').substring(1);
      setActiveTab(tabId);
    });
  });
});
