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