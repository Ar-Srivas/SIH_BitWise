window.addEventListener("DOMContentLoaded", () => {
    fetch("/teachers")
        .then(res => res.json())
        .then(data => {
            const teacherSelect = document.getElementById("teacherSelect");
            data.forEach(t => {
                const opt = document.createElement("option");
                opt.value = t.id;                   // teacher_id
                opt.textContent = ${t.name} (${t.subject});
                teacherSelect.appendChild(opt);
            });
        })
        .catch(err => console.error("Error loading teachers:", err));
});

document.getElementById("loadBtn").addEventListener("click", async () => {
    const date = document.getElementById("date").value;
    const teacher_id = document.getElementById("teacherSelect").value;
    const slotSelect = document.getElementById("slotSelect");
    const bookBtn = document.getElementById("bookBtn");

    if (!date || !teacher_id) {
        alert("Please select a date and a teacher");
        return;
    }

    try {
        const res = await fetch(/available_slots/${date}/${teacher_id});
        if (!res.ok) throw new Error("Slots not found or backend route missing");
        const slots = await res.json();

        // Clear previous slots
        slotSelect.innerHTML = "";

        if (slots.length === 0) {
            const opt = document.createElement("option");
            opt.value = "";
            opt.textContent = "No slots available";
            slotSelect.appendChild(opt);
            bookBtn.disabled = true;
        } else {
            slots.forEach(s => {
                const opt = document.createElement("option");
                opt.value = s.id;                   // slot_id
                opt.textContent = ${s.start} - ${s.end};
                slotSelect.appendChild(opt);
            });
            bookBtn.disabled = false;
        }
    } catch (err) {
        alert("Error loading slots: " + err.message);
    }
});

// Book selected slot
document.getElementById("bookBtn").addEventListener("click", async () => {
    const student_id = localStorage.getItem("userId"); // must be set after login
    const slot_id = document.getElementById("slotSelect").value;

    if (!slot_id) {
        alert("Please select a slot");
        return;
    }

    try {
        const res = await fetch("/book_slot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ student_id, slot_id })
        });

        const data = await res.json();
        alert(data.message);

        document.getElementById("loadBtn").click();
    } catch (err) {
        alert("Booking failed: " + err.message);
    }
});