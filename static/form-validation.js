/* 
Form validation

https://getbootstrap.com/docs/5.2/forms/validation/#how-it-works
*/
// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      }

      form.classList.add('was-validated')
    }, false)
  })

  /* Revert form state to before validatation */
  document.getElementById("clear").addEventListener("click", function () {
    Array.from(forms).forEach(form => {
      form.classList.remove('was-validated')
    })
  })
})()
