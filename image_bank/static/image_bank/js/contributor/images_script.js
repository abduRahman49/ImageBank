function togglePriceField(modalId) {
    const paymentCheckbox = document.querySelector(`#${modalId} #id_payment_required`);
    const priceField = document.querySelector(`#${modalId} .price`);

    paymentCheckbox.addEventListener('change', () => {
        if (paymentCheckbox.checked) {
            priceField.style.display = 'block';
        } else {
            priceField.style.display = 'none';
        }
    });
}

// Call the function for each modal
function initChoices() {
document.querySelectorAll('.edit-modal').forEach(modal => {
    if(!modal.classList.contains('choice-initialized')) {
      const choices = new Choices(modal.querySelector('#id_new_tags'), {
      searchEnabled: false,
      removeItemButton: true, // Allow removing tags
      delimiter: ','
    });
    }
    modal.classList.add('choice-initialized');
    togglePriceField(modal.getAttribute('id'));
})
}

function reinitChoices() {
initChoices();
}

function showToast(message, type) {
  Toastify({
    text: message,
    duration: 3000, // Set the duration for how long the toast message should appear (in milliseconds)
    gravity: 'top', // Set the position where the toast should appear
    position: 'center', // Set the position where the toast should appear
    close: true, // Allow users to close the toast manually
    backgroundColor: type === 'error' ? 'red' : 'green', // Customize the background color based on the message type
  }).showToast();
}

initChoices();

document.querySelector('#edit-form').addEventListener('submit', (e) => {
  e.preventDefault();
  console.log('Form submitted!');
  const name = document.querySelector('#id_name');
  const auteur = document.querySelector('#id_auteur');
  const image = document.querySelector('#id_image');
  const description = document.querySelector('#id_description');
  const licence = document.querySelector('#id_licence');
  const tags = document.querySelector('#id_new_tags');
  const payment_required = document.querySelector('#id_payment_required');
  const price = document.querySelector('#id_price');
  const imageId = document.querySelector('#id_id');

  let formData = new FormData();
  formData.append('name', name.value);
  formData.append('auteur', auteur.value);
  if(image.files.length > 0){
    formData.append('image', image.files[0]);
  }
  formData.append('description', description.value);
  formData.append('licence', licence.value);
  formData.append('new_tags', tags.value);
  if(payment_required.checked) {
    formData.append('payment_required', payment_required.checked);
    formData.append('price', price.value);
  }
  formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

  fetch(`/api/v1/edit/images/${imageId.value}/`, {
    method: 'POST',
    body: formData
  }).then(response => {
    if(response.ok) {
      response.json().then(data => {
        console.log(data);
        showToast(data.message, data.type);
      })
    }
  })
})

document.querySelector('#iconSidenav').addEventListener('click', (e) => {
  document.querySelector('body').classList.toggle('g-sidenav-pinned');
});

document.querySelector('#iconNavbarSidenav').addEventListener('click', (e) => {
    document.querySelector('body').classList.toggle('g-sidenav-pinned');
})

