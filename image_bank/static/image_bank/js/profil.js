
document.querySelector('#iconSidenav').addEventListener('click', (e) => {
    document.querySelector('body').classList.toggle('g-sidenav-pinned');
});

document.querySelector('#iconNavbarSidenav').addEventListener('click', (e) => {
    document.querySelector('body').classList.toggle('g-sidenav-pinned');
})

document.querySelectorAll('.nav-tabs').forEach(link => {
    link.addEventListener('click', (e) => {
        // Remove 'active' class from all links
        document.querySelectorAll('.nav-tabs').forEach(otherLink => {
            otherLink.classList.remove('active');
        });
        // Add 'active' class to the clicked link
        console.log(e.target);
        e.target.classList.add('active');
        if(e.target.getAttribute('aria-selected') === false){
            e.target.setAttribute('aria-selected', "true");
        }
    });
})

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
    
htmx.on('afterRequest', function (event) {
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