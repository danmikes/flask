function setUpBurgers(burgers) {
  burgers.forEach(burger => {
    burger.addEventListener('click', () => {
      const target = burger.dataset.target;
      const menu = document.getElementById(target);

      burger.classList.toggle('is-active');
      menu.classList.toggle('is-active');
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const burgers = document.querySelectorAll('.navbar-burger');
  setUpBurgers(burgers)
});


function toggleNavbar(burger) {
  const target = document.getElementById(burger.dataset.target);
  burger.classList.toggle('is-active');
  target.classList.toggle('is-active');
}

document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
      const navbarBurger = document.querySelector('.navbar-burger');
      const navbarMenu = document.getElementById(navbarBurger.dataset.target);
      if (navbarMenu.classList.contains('is-active')) {
          toggleNavbar(navbarBurger); // Close the menu
      }
  }
});
