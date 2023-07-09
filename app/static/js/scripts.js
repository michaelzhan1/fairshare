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


  // functions
  async function getPeople() {
    let response = await fetch('/get_people', {method: 'POST'});
    let data = await response.json();
    return data.names;
  }


  // populate choose involved checklist
  function populateChecklistWithPeople(element) {
    getPeople().then(people => {
      element.innerHTML = '<legend>Select people involved in payment:</legend>';
      let i = 0;
      people.forEach(person => {
        let option = document.createElement('input');
        option.type = 'checkbox';
        option.id = `person${i++}`;
        option.name = 'involved';
        option.value = person;
        
        
        element.appendChild(option);

        let label = document.createElement('label');
        label.htmlFor = option.id;
        label.textContent = person;
        element.appendChild(label);

        let br = document.createElement('br');
        element.appendChild(br);
      });
    });
  }


  // populate choose payer dropdown
  function populatePayerDropdown(element, people) {
    element.innerHTML = '<option disabled selected>--</option>';

    let involved = people.querySelectorAll('input:checked');
    involved.forEach(person => {
      let option = document.createElement('option');
      option.value = person.value;
      option.textContent = person.value;
      element.appendChild(option);
    });
  }


  // Event listeners
  // Open forms
  newPaymentBtn.addEventListener('click', async function() {
    addPaymentFormContainer.style.display = 'block';
    addPaymentForm.innerHTML = '';

    let paymentAmount = document.createElement('input');
    paymentAmount.type = 'number';
    paymentAmount.name = 'amount';
    paymentAmount.id = 'payment-amount';
    paymentAmount.placeholder = 'Amount';
    paymentAmount.required = true;
    paymentAmount.step = '0.01';
    paymentAmount.min = '0.01';

    let paymentAmountLabel = document.createElement('label');
    paymentAmountLabel.htmlFor = paymentAmount.id;
    paymentAmountLabel.textContent = 'Amount:';

    let chooseInvolved = document.createElement('fieldset');
    chooseInvolved.id = 'choose-involved';
    populateChecklistWithPeople(chooseInvolved)

    let choosePayer = document.createElement('select');
    choosePayer.name = 'payer';
    choosePayer.id = 'choose-payer';
    choosePayer.required = true;
    choosePayer.innerHTML = '<option disabled selected>--</option>';

    let choosePayerLabel = document.createElement('label');
    choosePayerLabel.htmlFor = choosePayer.id;
    choosePayerLabel.textContent = 'Payer: ';

    chooseInvolved.addEventListener('change', function() {
      populatePayerDropdown(choosePayer, chooseInvolved);
    });

    let submitBtn = document.createElement('button');
    submitBtn.type = 'submit';
    submitBtn.textContent = 'Submit';

    let lineBreak = document.createElement('br');

    addPaymentForm.appendChild(paymentAmountLabel);
    addPaymentForm.appendChild(paymentAmount);
    addPaymentForm.appendChild(lineBreak);
    addPaymentForm.appendChild(chooseInvolved);
    addPaymentForm.appendChild(choosePayerLabel);
    addPaymentForm.appendChild(lineBreak);
    addPaymentForm.appendChild(choosePayer);
    addPaymentForm.appendChild(submitBtn);
  });

  // Open person add form
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