function checkAuthAndRedirect(event, text) {
  event.preventDefault();
  alert(text);
}


function openModal(modalId) {
  closeAllModals();

  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "block";
  }
}

function closeAllModals() {
  const modals = document.querySelectorAll('.modal');
  modals.forEach((modal) => {
    modal.style.display = "none";
  });
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
}

