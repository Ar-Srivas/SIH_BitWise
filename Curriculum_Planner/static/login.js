document.getElementById("loginBtn").onclick = () => {
    const userid = document.getElementById("userid").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userid, password })
    })
    .then(r => r.json())
    .then(d => {
        if (d.success) {
            localStorage.setItem("userId", d.id);
            localStorage.setItem("role", d.role);
            if (d.role === "teacher")
                window.location.href = "/frontend/teacher.html";
            else
                window.location.href = "/frontend/student.html";
        } else {
            alert("Login failed");
        }
    });
};
