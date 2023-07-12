document.addEventListener('DOMContentLoaded', function() {
  const groupbutton = document.querySelector('#group-id-submit');
  groupbutton.addEventListener('click', function() {
    const groupid = document.querySelector('#group-id-input').value;
    window.location.href = '/g/' + groupid;
  });
});