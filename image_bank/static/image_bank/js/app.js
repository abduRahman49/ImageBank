/**
 * Define comopents used to display in app
 */

class ImageCard extends HTMLElement {
    
    // Logic used for initialising component
    constructor() {
        super();
        this.card = document.createElement('div');
        this.card.setAttribute('class', 'card');
        this.image = document.createElement('img');
        this.card.appendChild(this.image);
        this.cardBody = document.createElement('div');
        this.cardBody.setAttribute('class', 'card-body');
        this.card.appendChild(this.cardBody);
    }
}

class AccueilPage extends HTMLElement {

    constructor() {
        super();
        this.images = [];
        this.currentPage = 1;
        this.template = document.querySelector('#home-template');
        this.templateContent = this.template.innerHTML;
        this.innerHTML = this.templateContent;
    }

    connectedCallback () {
        if(this.isConnected){
            this.fetchAndDisplayImages(this.currentPage);
        }
    }

    disconnectedCallback () {
    }

    async fetchImagesForPage(page) {
        const response = await fetch(`/api/images/search?page=${page}`);
        const data = await response.json();
        return data;
    }

    async fetchAndDisplayImages(page) {
        const data = await this.fetchImagesForPage(page);
        this.images = data.results;
        this.renderContent();
    }

    renderContent() {
        this.images.forEach(image => {
            const gridContainer = this.querySelector('#content')
            const gridItem= document.createElement('div');
            gridItem.setAttribute('class', 'col-md-3 mb-4');
            const imageItem = document.createElement('img');
            imageItem.setAttribute('class', 'img-thumbnail');
            imageItem.src = image.image;
            gridItem.appendChild(imageItem);
            gridContainer.appendChild(gridItem);
        });
    }
}

class UploadPage extends HTMLElement {

    constructor() {
        super();
        this.div = document.createElement('div');
        this.template = document.querySelector('#upload-template');
        this.templateContent = this.template.innerHTML;
        this.div.innerHTML = this.templateContent;
        this.appendChild(this.div);
        this.querySelector('.price_row').classList.add('hidden');
        this.tags = new Tagify(this.querySelector('#id_tags'));
        this.querySelector('#id_tags').classList.add('hidden');
    }

    // Once the element is connected to the DOM, events/actions are attached to its elements
    connectedCallback () {
        if(this.isConnected){
            this.querySelector('#id_payment_required').addEventListener('change', togglePriceField);
            this.querySelector('#upload').addEventListener('submit', uploadFormSubmit);
        }
    }

    // Once the element is disconnected from the DOM, events/actions are detached from its elements
    disconnectedCallback () {
        this.querySelector('#id_payment_required').removeEventListener('change', togglePriceField);
        this.querySelector('#upload').removeEventListener('submit', uploadFormSubmit);
    }
}

class ManagePage extends HTMLElement {

   constructor() {
    super();
    // Initialize the images array
    this.currentPage = 1;
    this.images = [];
    this.template = document.querySelector('#manage-template').cloneNode(true);
    this.div = this.template.content;
    this.deleteModal = this.div.querySelector('#deleteModal');
    this.editModal = this.div.querySelector('#editModal');
    // Initialize the pagination bloc
    this.setAttribute('page', this.currentPage);
    // Render the content
    this.appendChild(this.div);
   }

   // Get the observed attributes
   static get observedAttributes() {
       return ['page'];
   }

   // When an attribute is changed
   attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'page' && oldValue !== newValue) {
            // Convert the newValue to a number if needed
            const newPage = parseInt(newValue, 10);
            if (!isNaN(newPage) && newPage !== this.currentPage) {
                this.currentPage = newPage;
                // Update the content section and pagination bloc with the new page value
                this.fetchAndDisplayImages(this.currentPage);
            }
        }
    }
    // When connectedCallback is fired, fetch all images from server at /api/images/ endpoint and add them to the images array
    connectedCallback () {
        if(this.isConnected){
            this.fetchAndDisplayImages(this.currentPage);
            this.deleteModal.querySelector('.btn.btn-danger').addEventListener('click', this.deleteImage.bind(this));
            this.editModal.querySelector('#edit').addEventListener('submit', this.submitEditForm.bind(this));
            new Tagify(this.editModal.querySelector('#tags'));
        }
    }

    async fetchImagesForPage(page) {
        // Make the fetch call to the endpoint with the appropriate query parameters
        const response = await fetch(`/api/images/?page=${page}`);
        const data = await response.json();
        return data;
    }

    // async fetchImageForId(id) {
    //     const response = await fetch(`/api/images/${id}/`);
    //     const data = await response.json();
    //     return data;
    // }
    
    async fetchAndDisplayImages(page) {
        const data = await this.fetchImagesForPage(page);
        // Update the images state with the fetched images
        this.images = data.results;
        // Update the content section to display the images
        this.renderContent();
        // Update the pagination bloc based on the total number of pages
        this.renderPagination(data.num_pages);
    }

    deleteImage (e) {
    e.preventDefault();
    const id = e.target.dataset.id;
    fetch(`/api/images/${id}/`, {
        method: 'DELETE'
    }).then(response => {
        if (response.ok) {
            this.querySelector(`[data-id="${id}"]`).remove();
            this.fetchAndDisplayImages(this.currentPage);
            Toastify({text: 'Image supprimée avec succès', duration: 3000}).showToast();
        } else {
            Toastify({text: 'Une erreur est survenue', duration: 3000}).showToast();
        }
    }).catch(error => {
        Toastify({text: error, duration: 3000}).showToast();
    })
    
    }

    submitEditForm (e) {
        e.preventDefault();
        const tags = [];
        const tagElements = this.editModal.querySelector('tags').querySelectorAll('tag');
        tagElements.forEach(tag => {
            tags.push(tag.getAttribute('value'));
        })
        const csrfToken = e.target.querySelector('input[name="csrfmiddlewaretoken"]').value;
        const formData = new FormData(e.target);
        formData.append('tags', tags);
        fetch(`api/v1/edit/images/${e.target.dataset.id}/`, {
            method: 'POST',
            body: formData
        }).then(response => response.json())
        .then(data => {
            this.fetchAndDisplayImages(this.currentPage);
            Toastify({
                text: data.message,
                duration: 3000
            }).showToast()
        })
        .catch(error => {
            Toastify({
                text: error,
                duration: 3000
            }).showToast()
        })
    }

    // function to get licences items via ajax
    async getLicenceItems(){
        const response = await fetch(`/api/licences/`);
        const data = await response.json();
        return data;
    }

    // Function used to transfer the image id to the modal
    transferImageIdToDeleteModal(image) {
        this.deleteModal.querySelector('.btn.btn-danger').setAttribute('data-id', image.id);
    }

    populateEditModal(image) {
        this.editModal.querySelector('#edit').setAttribute('data-id', image.id);
        this.editModal.querySelector('#name').value = image.name;
        this.editModal.querySelector('#auteur').value = image.auteur;
        this.editModal.querySelector('#description').value = image.description;
        // set the image field with the image value of the image
        this.editModal.querySelector('#image').setAttribute('src', image.image);
        if(image.price !== null){
            this.editModal.querySelector('#payment_required').checked = true;
            this.editModal.querySelector('.price_row').setAttribute('style', 'display: block');
            this.editModal.querySelector('#price').value = image.price;
        }

        this.editModal.querySelector('#payment_required').addEventListener('change', (e) => {
            if(e.target.checked) {
                this.editModal.querySelector('.price_row').setAttribute('style', 'display: block');
            } else {
                this.editModal.querySelector('.price_row').setAttribute('style', 'display: none');
            }
        })
        const tagItems = image.tags.map(tag => {
            return tag.name
        }).join(', ');
        
        this.getLicenceItems().then(data => {
            // create select input based on licences available
            let licenceItems = data.results.map(licence => {
                return `<option value="${licence.id}" ${licence.name === image.licence ? 'selected' : ''}>${licence.name}</option>`
            }).join('');
            if(image.licence === "") {
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.innerText = 'Choisissez une licence';
                licenceItems = defaultOption.outerHTML + licenceItems;
            }
            this.editModal.querySelector('#licence').innerHTML = licenceItems;
        });

        // create a select input based on licences available
        this.editModal.querySelector('#tags').value = tagItems;
    }
    
    renderContent() {
        // Clear the existing content section
        this.querySelector('#content').querySelector('tbody').innerHTML = '';
        this.images.forEach(image => {
            // Edit button creation
            const editIcon = document.createElement('i');
            editIcon.setAttribute('class', 'fas fa-edit');
            const editButton = document.createElement('a');
            editButton.setAttribute('class', 'btn btn-primary btn-sm');
            editButton.addEventListener('click', this.openEditImageForm.bind(this, image));
            editButton.setAttribute('data-mdb-toggle', 'modal');
            editButton.setAttribute('data-mdb-target', '#editModal');
            editButton.addEventListener('click', this.populateEditModal.bind(this, image));
            editButton.appendChild(editIcon);
            // Delete button creation
            const deleteIcon = document.createElement('i');
            deleteIcon.setAttribute('class', 'fas fa-trash');
            const deleteButton = document.createElement('a');
            deleteButton.setAttribute('class', 'btn btn-danger btn-sm');
            deleteButton.setAttribute('data-mdb-toggle', 'modal');
            deleteButton.setAttribute('data-mdb-target', '#deleteModal');
            deleteButton.addEventListener('click', this.transferImageIdToDeleteModal.bind(this, image));
            deleteButton.appendChild(deleteIcon);
            // Table rows and data population
            const tableRow = document.createElement('tr');
            const tableDataImage = document.createElement('td');
            const imageContainer = document.createElement('div');
            const imageElt = document.createElement('img');
            imageElt.src = image.image;
            imageElt.classList.add('avatar', 'avatar-sm', 'me-3');
            imageContainer.appendChild(imageElt);
            tableDataImage.appendChild(imageContainer);
            tableRow.appendChild(tableDataImage);
            const tableDataAuteur = document.createElement('td');
            const auteurParagraph = document.createElement('p');
            auteurParagraph.classList.add('text-xs', 'font-weight-bold', 'mb-0')
            auteurParagraph.innerText = image.auteur;
            tableDataAuteur.appendChild(auteurParagraph);
            tableRow.appendChild(tableDataAuteur);
            const tableDataFormat = document.createElement('td');
            const formatParagraph = document.createElement('p');
            formatParagraph.classList.add('text-xs', 'font-weight-bold', 'mb-0');
            formatParagraph.innerText = image.format;
            tableDataFormat.appendChild(formatParagraph);
            tableRow.appendChild(tableDataFormat);
            const tableDataType = document.createElement('td');
            const typeSpan = document.createElement('span');
            typeSpan.innerText = image.payment_required ? 'Payant' : 'Gratuit';
            typeSpan.classList.add('badge', 'badge-sm', image.payment_required ? 'badge-danger' : 'badge-success');
            tableDataType.appendChild(typeSpan);
            tableRow.appendChild(tableDataType);
            const tableDataEdit = document.createElement('td');
            tableDataEdit.setAttribute('class', 'align-middle');
            tableDataEdit.appendChild(editButton);
            tableRow.appendChild(tableDataEdit);
            const tableDataDelete = document.createElement('td');
            tableDataDelete.setAttribute('class', 'align-middle');
            tableDataDelete.appendChild(deleteButton);
            tableRow.appendChild(tableDataDelete);
            this.querySelector('#content').querySelector('tbody').appendChild(tableRow);

        });
        
    }

    // Function used to open the form to edit an image
    openEditImageForm(image) {
        const editImageForm = document.querySelector('#edit-image-form');
        editImageForm.querySelector('#id_image').value = image.id;
        editImageForm.querySelector('#id_description').value = image.description;
        editImageForm.querySelector('#id_tags').value = image.tags;
        editImageForm.querySelector('#id_price').value = image.price;
        editImageForm.querySelector('#id_payment_required').checked = image.payment_required;
        
    }

    renderPagination(numPages) {
        const paginationContainer = this.querySelector('#pagination');
        // Clear the existing pagination
        paginationContainer.innerHTML = '';
        // Create the pagination links for each page
        const navbar = document.createElement('nav');
        navbar.setAttribute('aria-label', '...');
        const ulist = document.createElement('ul');
        ulist.setAttribute('class', 'pagination pagination-circle mt-5');
        for (let i = 1; i <= numPages; i++) {
        const list = document.createElement('li');
        list.setAttribute('class', 'page-item');
        const pageLink = document.createElement('a');
        pageLink.setAttribute('class', 'page-link');
        pageLink.textContent = i;
        pageLink.addEventListener('click', () => {
            // When a pagination link is clicked, update the 'page' attribute
            this.setAttribute('page', i);
        });
        list.appendChild(pageLink);
        ulist.appendChild(list);
        }
        navbar.appendChild(ulist);
        paginationContainer.appendChild(navbar);
    }
}

// define renderContent method to populate images based on this.images value. Should first get the images container with selector '#content' and do the job

/**
 * Register custom components to use them as natively in html pages
 */

customElements.define('image-card', ImageCard);
customElements.define('accueil-page', AccueilPage);
customElements.define('upload-page', UploadPage);
customElements.define('manage-page', ManagePage);

/**
 * Define methods used by elements for user interaction with UI
 */


function navigate(e) {
    if(e.target.dataset.page === 'home'){
        document.querySelector('#content').innerHTML = '<accueil-page></accueil-page>';
    } else if(e.target.dataset.page === 'upload-images') {
        document.querySelector('#content').innerHTML = '<upload-page></upload-page>';
    } else if(e.target.dataset.page === 'manage-images') {
        document.querySelector('#content').innerHTML = '<manage-page></manage-page>';
    }
    
}

function togglePriceField(e) {
    if(e.target.checked){
        document.querySelector(".price_row").classList.remove('hidden');
        document.querySelector(".price_row").classList.add('visible');
    } else {
        document.querySelector(".price_row").classList.remove('visible');
        document.querySelector(".price_row").classList.add('hidden');
    }
}

function uploadFormSubmit(e) {
    e.preventDefault();
    const tags = [];
    const tagElements = document.querySelector('tags').querySelectorAll('tag');
    tagElements.forEach(tag => {
        tags.push(tag.getAttribute('value'));
    })
    const csrfToken = e.target.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const formData = new FormData(e.target);
    formData.append('tags', tags);

    fetch('api/v1/upload/images/', {
        method: "POST",
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    }).then(response => response.json())
    .then(data => {
        Toastify({
            text: data.message,
            duration: 3000
        }).showToast()
    }).catch(error => {
        Toastify({
            text: error,
            duration: 3000
        }).showToast()
    })
}

const links = document.querySelectorAll('.nav-link');
links.forEach(link => {
    link.addEventListener('click', navigate)
})
