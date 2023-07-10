document.addEventListener('DOMContentLoaded', function() {
  // buttons
  const newPaymentBtn = document.getElementById('new-payment-btn');
  const newPersonBtn = document.getElementById('new-person-btn');
  const calculateBtn = document.getElementById('calculate-btn');

  // pop up form containers
  const addPaymentFormContainer = document.getElementById('add-payment-form-container');
  const addPersonFormContainer = document.getElementById('add-person-form-container');
  const editPaymentFormContainer = document.getElementById('edit-payment-form-container');

  // Calculate stuff
  const calculateContainer = document.getElementById('calculate-container');
  const calculateBody = document.getElementById('calculate-body');

  // forms
  const addPaymentForm = document.getElementById('add-payment-form');
  const addPersonForm = document.getElementById('add-person-form');
  const editPaymentForm = document.getElementById('edit-payment-form');

  // payment display body
  const paymentContainer = document.getElementById('payment-container');


  // Event listeners
  // Open forms
  newPaymentBtn.addEventListener('click', async function() {
    addPaymentFormContainer.style.display = 'block';
    addPaymentForm.innerHTML = '';

    let description = document.createElement('input');
    description.type = 'text';
    description.name = 'description';
    description.id = 'payment-description';
    description.placeholder = 'Description (max 100 chars)';
    description.required = true;

    let descriptionLabel = document.createElement('label');
    descriptionLabel.htmlFor = description.id;
    descriptionLabel.textContent = 'Description:';

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

    addPaymentForm.appendChild(descriptionLabel);
    addPaymentForm.appendChild(description);
    addPaymentForm.appendChild(paymentAmountLabel);
    addPaymentForm.appendChild(document.createElement('br'));
    addPaymentForm.appendChild(paymentAmount);
    addPaymentForm.appendChild(chooseInvolved);
    addPaymentForm.appendChild(choosePayerLabel);
    addPaymentForm.appendChild(document.createElement('br'));
    addPaymentForm.appendChild(choosePayer);
    addPaymentForm.appendChild(submitBtn);
  });

  // Open person add form
  newPersonBtn.addEventListener('click', function() {
    addPersonFormContainer.style.display = 'block';
  });

  // Calculate button
  calculateBtn.addEventListener('click', function() {
    calculateContainer.style.display = 'block';
    calculateBody.innerHTML = '<p class="calculateHeader"><strong>Who owes who how much:</strong></p>';
    getDebts().then(debts => {
      for(let i = 0; i < debts.length; i++) {
        let from = debts[i][0];
        let to = debts[i][1];
        let amount = debts[i][2].toFixed(2);
        calculateBody.innerHTML += `<p><strong>${from}</strong> owes <strong>${to}</strong> $${amount}</p>`;
      }
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

  calculateContainer.addEventListener('click', function(e) {
    let formPopup = calculateContainer.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target)) {
      calculateContainer.style.display = 'none';
    }
  });

  editPaymentFormContainer.addEventListener('click', function(e) {
    let formPopup = editPaymentFormContainer.querySelector('.form-popup');
    if (e.target.classList.contains('close') || !formPopup.contains(e.target) || e.target.classList.contains('cancel-button')) {
      editPaymentFormContainer.style.display = 'none';
    }
  });


  // Open payment edit display
  paymentContainer.addEventListener('click', function(e) {
    if (e.target.classList.contains('edit-button')) {
      editPaymentFormContainer.style.display = 'block';
      let paymentid = e.target.parentElement.parentElement.dataset.paymentid;
      console.log(paymentid);

      getSinglePayment(paymentid).then(payment => {
        let descriptionValue = payment.description;
        let amountValue = payment.amount;
        let payerValue = payment.payer;
        let involvedValue = payment.involved;

        editPaymentFormContainer.style.display = 'block';
        editPaymentForm.innerHTML = '';

        let description = document.createElement('input');
        description.type = 'text';
        description.name = 'description';
        description.id = 'payment-description';
        description.placeholder = 'Description (max 100 chars)';
        description.required = true;
        description.value = descriptionValue;

        let descriptionLabel = document.createElement('label');
        descriptionLabel.htmlFor = description.id;
        descriptionLabel.textContent = 'Edit description:';

        let paymentAmount = document.createElement('input');
        paymentAmount.type = 'number';
        paymentAmount.name = 'amount';
        paymentAmount.id = 'payment-amount';
        paymentAmount.placeholder = 'Amount';
        paymentAmount.required = true;
        paymentAmount.step = '0.01';
        paymentAmount.min = '0.01';
        paymentAmount.value = amountValue;

        let paymentAmountLabel = document.createElement('label');
        paymentAmountLabel.htmlFor = paymentAmount.id;
        paymentAmountLabel.textContent = 'Edit amount:';

        let chooseInvolved = document.createElement('fieldset');
        chooseInvolved.id = 'choose-involved';
        
        getPeople().then(people => {
          chooseInvolved.innerHTML = '<legend>Select people involved in payment:</legend>';
          let i = 0;
          people.forEach(person => {
            let option = document.createElement('input');
            option.type = 'checkbox';
            option.id = `person${i++}`;
            option.name = 'involved';
            option.value = person;
            if (involvedValue.includes(person)) {
              option.checked = true;
            }
            
            chooseInvolved.appendChild(option);
      
            let label = document.createElement('label');
            label.htmlFor = option.id;
            label.textContent = person;
            chooseInvolved.appendChild(label);
      
            let br = document.createElement('br');
            chooseInvolved.appendChild(br);
          });
        });

        let choosePayer = document.createElement('select');
        choosePayer.name = 'payer';
        choosePayer.id = 'choose-payer';
        choosePayer.required = true;

        let choosePayerLabel = document.createElement('label');
        choosePayerLabel.htmlFor = choosePayer.id;
        choosePayerLabel.textContent = 'Payer: ';

        let involved = chooseInvolved.querySelectorAll('input:checked');
        involved.forEach(person => {
          let option = document.createElement('option');
          option.value = person.value;
          option.textContent = person.value;
          element.appendChild(option);
          if (payerValue === person.value) {
            option.selected = true;
          }
        });

        chooseInvolved.addEventListener('change', function() {
          populatePayerDropdown(choosePayer, chooseInvolved); //
        });

        let submitBtn = document.createElement('button');
        submitBtn.type = 'submit';
        submitBtn.textContent = 'Submit';

        let cancelBtn = document.createElement('button');
        cancelBtn.classList.add('cancel-button');
        cancelBtn.textContent = 'Cancel';

        editPaymentForm.appendChild(descriptionLabel);
        editPaymentForm.appendChild(description);
        editPaymentForm.appendChild(paymentAmountLabel);
        editPaymentForm.appendChild(document.createElement('br'));
        editPaymentForm.appendChild(paymentAmount);
        editPaymentForm.appendChild(chooseInvolved);
        editPaymentForm.appendChild(choosePayerLabel);
        editPaymentForm.appendChild(document.createElement('br'));
        editPaymentForm.appendChild(choosePayer);
        editPaymentForm.appendChild(submitBtn);
        editPaymentForm.appendChild(cancelBtn);
      });
    }

    // LOGIC FLOW:
    // 1. add data field to parent of parent of edit, which should be the div container for that row
    // 2. in the data field, store the id of the payment, from the database
    // 3. when either edit or see details is clicked, get the data of that single id (new route)
    // 3.5 the form can look very similar to newpayment for edit
    // 3.5.1 The see details can be similar, but with just a text field for the description and amount and who was paid for
    // 4. depending on whether edit or see details was clicked, create 2 new routes, one for each to do the update or delete task
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