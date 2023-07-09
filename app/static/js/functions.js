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