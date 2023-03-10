'use strict'

// check inputs respect the min and max length attributes if trimmed
let form = document.getElementById("signup-form");
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

// check password strength
const passwordInput = document.querySelector("#password-input");
const passwordInfoIcon = document.querySelector("#password-info-icon");
const passwordTooltip = document.querySelector("#password-tooltip");
passwordInput.addEventListener("input", checkPassword);

function checkPassword() {

    passwordInfoIcon.classList.remove("fa-info-circle");

    let password = passwordInput.value;
    let strength = 0;
    let strengthText = "";

    let check1 = false;
    let check2 = false;
    let check3 = false;
    let check4 = false;

    if (password.length >= 8) {
        check1 = true;
        strength++;
    }
    if (password.length >= 12) {
        strength++;
    }
    if (password.match(/[a-z]/)) {
        check2 = true;
        strength++;
    }
    if (password.match(/[A-Z]/)) {
        check3 = true;
        strength++;
    }
    if (password.match(/[0-9]/)) {
        check4 = true;
        strength++;
    }
    if (password.match(/[!@#\$%\^&\*]/)) {
        strength++;
    }

    switch (strength) {
        case 0:
            strengthText = "Password debole";
            break;
        case 1:
            strengthText = "Password debole";
            break;
        case 2:
            strengthText = "Password media";
            break;
        case 3:
            strengthText = "Password media";
            break;
        case 4:
            strengthText = "Password forte";
            break;
        case 5:
            strengthText = "Password forte";
            break;
        default:
            strengthText = "Password molto forte"
            break;
    }

    passwordTooltip.classList.remove('d-none')
    passwordTooltip.innerText = strengthText;

    if (check1 && check2 && check3 && check4) {
        passwordInfoIcon.classList.remove("fa-times-circle");
        passwordInfoIcon.classList.add("fa-circle-check");
    } else {
        passwordInfoIcon.classList.remove("fa-circle-check");
        passwordInfoIcon.classList.add("fa-times-circle");
    }
}