function initializePaymentButtons() {
  const paymentCheckbox = document.querySelector("#id_payment_required");
  const priceField = document.querySelector(".price");

  const auteur = document.querySelector('#id_auteur');
  let auteurChoiceInitialized = false;
  if(!auteurChoiceInitialized) {
    new Choices(auteur);
    auteur.classList.add('choice-initialized');
  }
  auteurChoiceInitialized = true;

  const licence = document.querySelector('#id_licence');
  let licenceChoiceInitialized = false;
  if(!licenceChoiceInitialized) {
    new Choices(licence);
    licence.classList.add('choice-initialized');
  }
  licenceChoiceInitialized = true;

  paymentCheckbox.addEventListener('change', () => {
      if (paymentCheckbox.checked) {
          priceField.style.display = 'block';
      } else {
          priceField.style.display = 'none';
      }
  });
}

initializePaymentButtons()


function initializeTagInputs() {
    let tagInputsInitialized = false;
    if(!tagInputsInitialized){
      const choices = new Choices('#id_new_tags', {
      searchEnabled: false,
      removeItemButton: true, // Allow removing tags
      delimiter: ','
      });
    }
    tagInputsInitialized = true;
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

initializeTagInputs();

htmx.on('#form', 'htmx:xhr:progress', function(evt) {
      htmx.find('#progress').setAttribute('value', evt.detail.loaded/evt.detail.total * 100)
});

htmx.on('htmx:afterRequest', function (event) {
    if (event.detail.xhr.status === 200) { // Check if the request was successful (status code 200)
        // Assuming your response JSON contains a 'message' field
        const response = JSON.parse(event.detail.xhr.responseText);
        if (response.message) {
        showToast(response.message, 'success'); // Show a success toast message
        }
    } else if (event.detail.xhr.status === 400) { // If there was an error (status code 400)
        // Assuming your response JSON contains an 'error' field
        const response = JSON.parse(event.detail.xhr.responseText);
        if (response.message) {
        showToast(response.message, 'error'); // Show an error toast message
        }
    }
});

document.querySelector('#iconSidenav').addEventListener('click', () => {
  console.log('button clicked!')
  document.querySelector('body').classList.toggle('g-sidenav-pinned');
});

document.querySelector('#iconNavbarSidenav').addEventListener('click', (e) => {
  document.querySelector('body').classList.toggle('g-sidenav-pinned');
})


