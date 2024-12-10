document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.navbar-item.has-dropdown');

  dropdowns.forEach(dropdown => {
    const toggle = dropdown.querySelector('.navbar-link');
    const menu = dropdown.querySelector('.navbar-dropdown');

    toggle.addEventListener('click', function(e) {
      e.preventDefault();

      menu.classList.toggle('is-active');

      dropdowns.forEach(otherDropdown => {
        if (otherDropdown !== dropdown) {
          otherDropdown.querySelector('.navbar-dropdown').classList.remove('is-active');
        }
      });
    });
  });

  document.addEventListener('click', function(e) {
    if (!e.target.closest('.navbar-item.has-dropdown')) {
      dropdowns.forEach(dropdown => {
        dropdown.querySelector('.navbar-dropdown').classList.remove('is-active');
      });
    }
  });
});
