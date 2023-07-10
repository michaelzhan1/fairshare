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
            <div class="col-1">
              <p>${month}</p>
              <p>${day}</p>
            </div>
            <div class="col-8">
              <p>${description}</p>
              <p>Paid by ${payer}</p>
            </div>
            <div class="col-2">
              <p>$${amount}</p>
            </div>
            <div class="col-1">
              <a href="/">Edit</a>
              <a href="/">See details</a>
            </div>
          </div>
        </div>
      `
      if (container.children.length > 0) {
        container.appendChild(document.createElement('hr'));
      }
      container.innerHTML += html;
    });
  });
});