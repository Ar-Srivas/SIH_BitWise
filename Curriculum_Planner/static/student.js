document.getElementById("loadBtn").onclick = () => {
    const date = document.getElementById("date").value;
    if (!date) {
        alert("Please choose a date");
        return;
    }

    fetch(`/available_slots/${date}`)
    .then(r => r.json())
    .then(data => {
        const sel = document.getElementById("slotSelect");
        sel.innerHTML = "";
        if (data.length === 0) {
            const opt = document.createElement("option");
            opt.textContent = "No slots available";
            sel.appendChild(opt);
        } else {
            data.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s.id;
                opt.textContent = `${s.start} - ${s.end}`;
                sel.appendChild(opt);
            });
        }
    });
};

document.getElementById("bookBtn").onclick = () => {
    const student_id = localStorage.getItem("userId");
    const slot_id = document.getElementById("slotSelect").value;

    if (!slot_id) {
        alert("Please select a slot");
        return;
    }

    fetch("/book_slot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id, slot_id })
    })
    .then(r => r.json())
    .then(d => alert(d.message));
};
