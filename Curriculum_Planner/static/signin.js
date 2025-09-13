const loginBtn = document.querySelector(".login");
const signupBtn = document.querySelector(".signup");
const formSection = document.querySelector(".form-section");
const slider = document.querySelector(".slider");

// Initially show login form
loginBtn.classList.add("active");
loginBtn.addEventListener("click", () => {
formSection.classList.remove("move");
slider.classList.remove("move");
loginBtn.classList.add("active");
    signupBtn.classList.remove("active");
});
signupBtn.addEventListener("click", () => {
formSection.classList.add("move");
slider.classList.add("move");
signupBtn.classList.add("active");
loginBtn.classList.remove("active");
});