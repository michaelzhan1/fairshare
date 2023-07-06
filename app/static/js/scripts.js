document.addEventListener('DOMContentLoaded', function() {
  // buttons
  const newPaymentBtn = document.getElementById('new-payment-btn');
  const newPersonBtn = document.getElementById('new-person-btn');

  // pop up forms
  const addPaymentForm = document.getElementById('add-payment-form');
  const addPersonForm = document.getElementById('add-person-form');


  // Event listeners
  // Open forms
  newPaymentBtn.addEventListener('click', function() {
    addPaymentForm.style.display = 'block';
    addPaymentForm.addEventListener('click', outsideClick);
  });

  newPersonBtn.addEventListener('click', function() {
    addPersonForm.style.display = 'block';
    addPersonForm.addEventListener('click', outsideClick);
  });

  // Close forms
  addPaymentForm.addEventListener('click', function(e) {
    let formPopup = addPaymentForm.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target)) {
      addPaymentForm.style.display = 'none';
    }
  });

  addPersonForm.addEventListener('click', function(e) {
    let formPopup = addPersonForm.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target)) {
      addPersonForm.style.display = 'none';
    }
  });
});