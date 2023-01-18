'use strict'

const searchbar = document.getElementById('searchbar');
const podcasts = document.getElementsByClassName('podcast');

searchbar.addEventListener('input', search);

const urlParams = new URLSearchParams(window.location.search);
const query = urlParams.get('query');
if (query) {
    searchbar.value = query
    let event = new Event('input');
    searchbar.dispatchEvent(event);
}

function search() {
    const searchString = this.value.toLowerCase();
    for (let podcast of podcasts) {
        let title, description, category;
        try {
            title = podcast.getElementsByClassName('podcast-title')[0].innerText.toLowerCase();
        } catch(err) {
            title = '';
        }
        try {
            description = podcast.getElementsByClassName('podcast-description')[0].innerText.toLowerCase();
        } catch(err) {
            description = '';
        }
        try {
            category = podcast.getElementsByClassName('podcast-category')[0].innerText.toLowerCase();
        } catch(err) {
            category = '';
        }
        
        if (title.includes(searchString) || description.includes(searchString) || category.includes(searchString)) {
            podcast.parentNode.classList.remove('d-none');
        } else {
            podcast.parentNode.classList.add('d-none');
        }
    }
}