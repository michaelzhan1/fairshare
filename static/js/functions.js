// functions
async function getPeople(groupid) {
  let response = await fetch('/api/get_people', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"groupid": groupid}),
  });
  let data = await response.json();
  return data.names;
}

async function getDebts(groupid) {
  let response = await fetch('/api/calculate', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"groupid": groupid})
  });
  let data = await response.json();
  return data.debts;
}

async function getPayments(groupid) {
  let response = await fetch('/api/get_payments', {
    method: 'POST',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"groupid": groupid}),
  });
  let data = await response.json();
  return data.payments;
}


async function getSinglePayment(id) {
  let response = await fetch('/api/get_single_payment', {
    method: 'POST',
    mode: 'cors',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"paymentid": id})
  });
  let data = await response.json();
  return data.payment;
}


async function updatePayment(paymentid, payment, groupid) {
  await fetch('/api/edit_payment', {
    method: 'POST',
    mode: 'cors',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"paymentid": paymentid, "payment": payment, "groupid": groupid})
  }).then(response => {
    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  });
}


async function deletePayment(paymentid, groupid) {
  await fetch('/api/delete_payment', {
    method: 'POST',
    mode: 'cors',
    headers: {
      "Content-Type": "application/json",
      "Accept": "application/json"
    },
    body: JSON.stringify({"paymentid": paymentid, "groupid": groupid})
  }).then(response => {
    if (response.status == 200) {
      return true;
    } else {
      return false;
    }
  });
}


// populate choose involved checklist
function populateChecklistWithPeople(element) {
  getPeople(groupid).then(people => {
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
  element.innerHTML = '';

  let involved = people.querySelectorAll('input:checked');
  involved.forEach(person => {
    let option = document.createElement('option');
    option.value = person.value;
    option.textContent = person.value;
    element.appendChild(option);
  });
}