'use strict'

// check inputs respect the min and max length attributes if trimmed
let form = document.getElementById("new-episode-form");
form.addEventListener("submit", function(event) {
    event.preventDefault();
    let inputFields = form.getElementsByTagName("input");
    let valid = true;
    for (let i = 0; i < inputFields.length; i++) {
        let minlength = inputFields[i].getAttribute("minlength");
        if (minlength) {
            let value = inputFields[i].value.trim();
            if (value.length < minlength) {
                valid = false;
                alert("Il campo " + inputFields[i].name + " deve essere lungo almeno " + minlength + " caratteri (escludendo eventuali spazi all'inizio e/o alla fine)");
                break;
            }
        }
    }
    if (valid) {
        form.submit();
    }
});