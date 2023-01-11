"use strict"

const newPodBtn = document.querySelector('#newPodBtn') 

newPodBtn.addEventListener('click', event => {
    window.location.href = "{{ url_for('new_podcast') }}"
}) 