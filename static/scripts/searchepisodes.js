'use strict'

const searchbar = document.getElementById('searchbar');
const episodes = document.getElementsByClassName('episode');

searchbar.addEventListener('input', search);

function search() {
  const searchString = this.value.toLowerCase();
  for (let episode of episodes) {

    let title, description;
    try {
        title = episode.getElementsByClassName('episode-title')[0].innerText.toLowerCase();
    } catch(err) {
        title = '';
    }
    try {
        description = episode.getElementsByClassName('episode-description')[0].innerText.toLowerCase();
    } catch(err) {
        description = '';
    }

    if (title.includes(searchString) || description.includes(searchString)) {
      episode.parentNode.classList.remove('d-none');
    } else {
      episode.parentNode.classList.add('d-none');
    }
  }
}