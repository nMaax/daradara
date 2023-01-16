'use strict'

const searchbar = document.getElementById('searchbar');
const episodes = document.getElementsByClassName('episode');

searchbar.addEventListener('input', function() {
  const searchString = this.value.toLowerCase();
  for (let episode of episodes) {
    const title = episode.getElementsByClassName('episode-title')[0].innerText.toLowerCase();
    const description = episode.getElementsByClassName('episode-description')[0].innerText.toLowerCase();
    if (title.includes(searchString) || description.includes(searchString)) {
      episode.style.display = 'block';
    } else {
      episode.style.display = 'none';
    }
  }
});
