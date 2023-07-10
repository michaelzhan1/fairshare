// functions
async function getPeople() {
  let response = await fetch('/get_people', {method: 'POST'});
  let data = await response.json();
  return data.names;
}

async function getDebts() {
  let response = await fetch('/calculate', {method: 'POST'});
  let data = await response.json();
  return data.debts;
}

async function getPayments() {
  let response = await fetch('/get_payments', {method: 'POST'});
  let data = await response.json();
  return data.payments;
}


async function getSinglePayment(id) {
  let response = await fetch('/get_single_payment', {
    method: 'POST',
    mode: 'cors',
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({"paymentid": id})
  });
  let data = await response.json();
  return data.payment;
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