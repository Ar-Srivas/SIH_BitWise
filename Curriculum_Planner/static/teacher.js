document.getElementById("createBtn").onclick = () => {
    const teacher_id = localStorage.getItem("userId");
    const date = document.getElementById("date").value;
    const start_time = document.getElementById("start").value;
    const end_time = document.getElementById("end").value;

    if (!date || !start_time || !end_time) {
        alert("Please fill all fields");
        return;
    }

    fetch("/create_slot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ teacher_id, date, start_time, end_time })
    })
    .then(r => r.json())
    .then(() => {
        alert("Slot created");
        document.getElementById("date").value = "";
        document.getElementById("start").value = "";
        document.getElementById("end").value = "";
    });
};
