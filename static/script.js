function validateAndSubmit() {
  if (validateForm() && confirmPwd()) {
    return true;
  } else {
    return false;
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

// function changeInputValue(newValue) {
//   var inputElement = document.querySelectorAll(".inputf");
//   inputElement.value = newValue;
// }

function changeInputValue(newValue) {
  // Find all input elements with the specified class
  var inputElements = document.querySelectorAll(".inputf");

  // Loop through each input element and change its value
  inputElements.forEach(function (inputElement) {
    // Perform your logic to change the input value
    inputElement.value = newValue; // Replace "new value" with your desired value
  });
}

function changeInputValueRemove(newValue) {
  // Find all input elements with the specified class
  var inputElements = document.querySelectorAll(".inputr");

  // Loop through each input element and change its value
  inputElements.forEach(function (inputElement) {
    // Perform your logic to change the input value
    inputElement.value = newValue; // Replace "new value" with your desired value
  });
}

// function changeInputValueRemove(newValue) {
//   var inputElement = document.querySelectorAll(".inputr");
//   inputElement.value = newValue;
// }
