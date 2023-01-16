'use strict'

const searchbar = document.getElementById('searchbar');
const podcasts = document.getElementsByClassName('podcast');

searchbar.addEventListener('input', function() {
  const searchString = this.value.toLowerCase();
  for (let podcast of podcasts) {
    const title = podcast.getElementsByClassName('podcast-title')[0].innerText.toLowerCase();
    const description = podcast.getElementsByClassName('podcast-description')[0].innerText.toLowerCase();
    const category = podcast.getElementsByClassName('podcast-category')[0].innerText.toLowerCase();
    if (title.includes(searchString) || description.includes(searchString) || category.includes(searchString)) {
      podcast.style.display = 'block';
    } else {
      podcast.style.display = 'none';
    }
  }
});
