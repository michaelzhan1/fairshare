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

  // payment form inputs
  const chooseInvolved = document.getElementById('choose-involved');
  const choosePayer = document.getElementById('choose-payer-select');


  // functions
  async function getPeople() {
    let response = await fetch('/get_people');
    let data = await response.json();
    return data.names;
  }


  // Event listeners
  // Open forms
  newPaymentBtn.addEventListener('click', function() {
    addPaymentFormContainer.style.display = 'block';

    // Populate involved people
    getPeople().then(people => {
      chooseInvolved.innerHTML = '<legend>Select people involved in payment:</legend>';
      let i = 0;
      people.forEach(person => {
        let option = document.createElement('input');
        option.type = 'checkbox';
        option.value = person;
        option.name = 'involved';
        option.id = `person${i++}`;
        chooseInvolved.appendChild(option);

        let label = document.createElement('label');
        label.htmlFor = option.id;
        label.textContent = person;
        chooseInvolved.appendChild(label);

        let br = document.createElement('br');
        chooseInvolved.appendChild(br);
      });
    });
  });

  // Open person add form
  newPersonBtn.addEventListener('click', function() {
    addPersonFormContainer.style.display = 'block';
  });

  // Update payer select dropdown on selecting people involved
  chooseInvolved.addEventListener('change', function() {
    choosePayer.innerHTML = '<option disabled selected>--</option>';

    let involved = document.querySelectorAll('input[name="involved"]:checked');
    involved.forEach(person => {
      let option = document.createElement('option');
      option.value = person.value;
      option.textContent = person.value;
      choosePayer.appendChild(option);
    });
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