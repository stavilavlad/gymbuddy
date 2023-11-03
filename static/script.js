function validateAndSubmit() {
  if (validateForm() && confirmPwd() && validateUsername()) {
    return true;
  } else {
    return false;
  }
}

function validateUsername() {
  var usernameInput = document.getElementById("floatingInputSign");
  var usernameError = document.getElementById("usernameError");

  if (usernameInput.value.length > 24) {
    usernameError.innerHTML = "Username must be less than 24 characters";
    usernameError.style.display = "block";
    return false;
  } else {
    usernameError.style.display = "none";
    return true;
  }
}

function validateForm() {
  var passwordInput = document.getElementById("floatingPasswordSign");
  var passwordError = document.getElementById("passwordError");

  if (passwordInput.value.length < 8) {
    passwordError.innerHTML = "Password must be at least 8 characters long.";
    passwordError.style.display = "block";
    return false;
  } else {
    passwordError.style.display = "none";
    return true;
  }
}

function confirmPwd() {
  var passwordInput = document.getElementById("floatingPasswordSign");
  var passwordConfirmInput = document.getElementById("floatingConfirmPassword");
  var passwordConfirmError = document.getElementById("passwordConfirmError");

  if (passwordInput.value !== passwordConfirmInput.value) {
    passwordConfirmError.innerHTML = "Passwords do not match.";
    passwordConfirmError.style.display = "block";
    return false;
  } else {
    passwordError.style.display = "none";
    return true;
  }
}

function changeInputValue(newValue) {
  var inputElements = document.querySelectorAll(".inputf");
  inputElements.forEach(function (inputElement) {
    inputElement.value = newValue;
  });
}

function changeInputValueRemove(newValue) {
  var inputElements = document.querySelectorAll(".inputr");
  inputElements.forEach(function (inputElement) {
    inputElement.value = newValue;
  });
}
