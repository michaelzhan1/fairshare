document.addEventListener('DOMContentLoaded', function() {
  // buttons
  const newPaymentBtn = document.getElementById('new-payment-btn');
  const newPersonBtn = document.getElementById('new-person-btn');

  // pop up form containers
  const addPaymentFormContainer = document.getElementById('add-payment-form-container');
  const addPersonFormContainer = document.getElementById('add-person-form-container');

  // forms
  const addPaymentForm = document.getElementById('add-payment-form');
  const addPersonForm = document.getElementById('add-person-form');


  // Event listeners
  // Open forms
  newPaymentBtn.addEventListener('click', function() {
    addPaymentFormContainer.style.display = 'block';
  });

  newPersonBtn.addEventListener('click', function() {
    addPersonFormContainer.style.display = 'block';
  });

  // Close forms
  addPaymentFormContainer.addEventListener('click', function(e) {
    let formPopup = addPaymentFormContainer.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target)) {
      addPaymentFormContainer.style.display = 'none';
    }
  });

  addPersonFormContainer.addEventListener('click', function(e) {
    let formPopup = addPersonFormContainer.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target)) {
      addPersonFormContainer.style.display = 'none';
    }
  });


  async function getPeople() {
    let response = await fetch('/get_people');
    let data = await response.json();
    return data.names;
  }


  // Validate person submission
  addPersonForm.addEventListener('submit', function(e) {
    e.preventDefault();
    let name = document.getElementById('new-person-name').value;
    if (name === '') {
      alert('Please enter a name');
      return;
    }
    getPeople().then(people => {
      if (people.includes(name)) {
        alert('That name already exists');
        return;
      }
      addPersonForm.submit();
    });
  });
});