document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("login-form");
    const loginError = document.getElementById("login-error");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault()
        const email = event.target.email.value;
        const password = event.target.password.value;
        loginError.textContent = "";

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email: email,
                    password: password,
                }),
            });
            if (response.ok) {
                const result = await response.json();
                console.log("login successful", result);
                window.location.href("/dashboard");
            } else {
                const errorData = await response.json();
                loginError.textContent = errorData.detail || "login failed"
            }
        } catch (e) {
            console.error("login req failed", e);
            loginError.textContent = "an error occured try again later";
        }
    });
});