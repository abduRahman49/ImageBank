

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
      // Remove 'active' class from all links
      document.querySelectorAll('.nav-link').forEach(otherLink => {
        otherLink.classList.remove('active');
      });
  
      // Add 'active' class to the clicked link
      e.target.classList.add('active');
    });
});
  
document.querySelector('#iconSidenav').addEventListener('click', (e) => {
    console.log('button clicked!')
    document.querySelector('body').classList.toggle('g-sidenav-pinned');
});

document.querySelector('#iconNavbarSidenav').addEventListener('click', (e) => {
    document.querySelector('body').classList.toggle('g-sidenav-pinned');
})

// document.querySelector('#iconNavbarSidenav').addEventListener('click', (e) => {
//   console.log('burger button clicked!')
//   console.log(document.querySelector('body'))
//     // document.querySelector('body').classList.toggle('g-sidenav-pinned');
//   console.log(document.querySelector('body').classList.contains('g-sidenav-pinned'));