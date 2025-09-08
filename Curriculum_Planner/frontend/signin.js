const loginBtn = document.querySelector(".login");
const signupBtn = document.querySelector(".signup");
const formSection = document.querySelector(".form-section");
const slider = document.querySelector(".slider");

loginBtn.addEventListener("click", () => {
  formSection.classList.remove("move");
  slider.classList.remove("move");
});

signupBtn.addEventListener("click", () => {
  formSection.classList.add("move");
  slider.classList.add("move");
});
