function toggleModal(isActive) {
  const modal = document.getElementById('infoModal');
  if (isActive) {
      modal.classList.add('is-active');
  } else {
      modal.classList.remove('is-active');
  }
}

document.getElementById('closeModal').addEventListener('click', () => toggleModal(false));
document.querySelector('.modal-close').addEventListener('click', () => toggleModal(false));
document.querySelector('.modal-background').addEventListener('click', () => toggleModal(false));

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
      toggleModal(false);
  }
});

function openModal() {
  toggleModal(true);
}
