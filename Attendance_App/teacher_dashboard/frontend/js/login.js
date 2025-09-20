document.addEventListener("DOMContentLoaded", () => {
    const body = document.querySelector("body");
    const modal = document.querySelector(".modal");
    const modalButton = document.querySelector(".modal-button");
    const closeButton = document.querySelector(".close-button");
    const scrollDown = document.querySelector(".scroll-down");
    // Use a more descriptive name for the state flag.
    let hasBeenOpenedOnScroll = false;

    const openModal = () => {
        modal.classList.add("is-open");
        body.style.overflow = "hidden";
        if (scrollDown) {
        scrollDown.style.display = "none";
        }
    };

    const closeModal = () => {
        modal.classList.remove("is-open");
        body.style.overflow = "initial";
        // We no longer need to reset a flag here. The scroll listener will handle it.
        if (scrollDown) {
        scrollDown.style.display = "flex";
        }
    };

    // This is the new, more robust scroll logic.
    window.addEventListener("scroll", () => {
        const scrollPosition = window.scrollY;
        const triggerPoint = window.innerHeight / 3;

        // Condition to open: scrolling down past the trigger point for the first time.
        if (scrollPosition > triggerPoint && !hasBeenOpenedOnScroll) {
        hasBeenOpenedOnScroll = true;
        openModal();
        }

        // Condition to reset: user has scrolled back up near the top of the page.
        // This allows the scroll-to-open feature to be used again.
        if (scrollPosition < 100 && hasBeenOpenedOnScroll) {
        hasBeenOpenedOnScroll = false;
        }
    });


    if (modalButton) {
        modalButton.addEventListener("click", openModal);
    }
    if (closeButton) {
        closeButton.addEventListener("click", closeModal);
    }


    document.onkeydown = (evt) => {
        evt = evt || window.event;
        if (evt.keyCode === 27) {
        closeModal();
        }
    };


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
                // console.log(result.email);
                sessionStorage.setItem("teacherId", result.email);
                sessionStorage.setItem("teacherName", result.name);
                window.location.href = "/dashboard";
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