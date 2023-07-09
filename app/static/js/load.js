const table = document.getElementById('table');

window.addEventListener('load', function() {
  people = getPeople();
  // create a header row for the table with the names of the people
  people.then(people => {
    let headerRow = document.createElement('tr');
    let headerCell = document.createElement('th');
    headerCell.textContent = 'Amount';
    headerRow.appendChild(headerCell);
    people.forEach(person => {
      headerCell = document.createElement('th');
      headerCell.textContent = person;
      headerRow.appendChild(headerCell);
    });
    table.appendChild(headerRow);
  });

  // create a row for each payment with the amount, and checkboxes for each person. check the boxes if the person was involved in the payment, and disable them. highlight the cell if the person paid for the payment.
  getPayments().then(payments => {
    payments.forEach(payment => {
      let row = document.createElement('tr');
      let cell = document.createElement('td');
      cell.textContent = `$${payment.amount.toFixed(2)}`;
      row.appendChild(cell);
      people.then(people => {
        people.forEach(person => {
          cell = document.createElement('td');
          let checkbox = document.createElement('input');
          checkbox.type = 'checkbox';
          checkbox.disabled = true;
          checkbox.checked = payment.involved.includes(person);
          checkbox.classList.add('custom-checkbox');
          if (payment.payer == person) {
            cell.classList.add('highlight');
          }
          cell.appendChild(checkbox);
          row.appendChild(cell);
        });
        table.appendChild(row);
      });
    });
  });
});