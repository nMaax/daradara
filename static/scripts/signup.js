'use strict'

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
    let checkLenght = false

    if (password.length >= 8) {
        checkLenght = true
        strength++;
    }
    if (password.length >= 12) {
        strength++;
    }
    if (password.match(/[a-z]/)) {
        strength++;
    }
    if (password.match(/[A-Z]/)) {
        strength++;
    }
    if (password.match(/[0-9]/)) {
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

    passwordTooltip.innerText = strengthText;

    if (checkLenght) {
        passwordInfoIcon.classList.remove("fa-times-circle");
        passwordInfoIcon.classList.add("fa-circle-check");
    } else {
        passwordInfoIcon.classList.remove("fa-circle-check");
        passwordInfoIcon.classList.add("fa-times-circle");
    }
}  