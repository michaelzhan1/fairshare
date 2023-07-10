const container = document.getElementById('payment-container')

window.addEventListener('load', function() {
  getPayments().then(payments => {
    payments.forEach(payment => {
      let date_array = payment.date.split(' ');
      let month = date_array[2];
      let day = date_array[1];

      let description = payment.description;
      let amount = payment.amount.toFixed(2);
      let payer = payment.payer;

      let html = `
        <div class="container">
          <div class="row">
            <div class="col-1 date-display d-flex flex-column justify-content-center align-items-start">
              <p>${month}<br>${day}</p>
            </div>
            <div class="col-7 info-display d-flex flex-column justify-content-center align-items-start">
              <p class="desc-display">${description}</p>
              <p class="payer-display">Paid by ${payer}</p>
            </div>
            <div class="col-2 amt-display d-flex flex-column justify-content-center align-items-end">
              <p>$${amount}</p>
            </div>
            <div class="col-2 options-display d-flex flex-column justify-content-center align-items-center">
              <a href="/">Edit</a>
              <a href="/">See details</a>
            </div>
          </div>
        </div>
      `
      container.innerHTML += html;
      container.appendChild(document.createElement('hr'));
    });
  });
});