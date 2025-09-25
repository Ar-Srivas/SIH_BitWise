let slots = [];
let currentDate = new Date();
let selectedTeacher = null;

// Load teachers into dropdown
window.onload = () => {
    fetch("/teachers")
    .then(r => r.json())
    .then(data => {
        const sel = document.getElementById("teacherSelect");
        data.forEach(t => {
            const opt = document.createElement("option");
            opt.value = t.id;
            opt.textContent = `${t.name} (${t.subject})`;
            sel.appendChild(opt);
        });

        // auto-select first teacher if exists
        if (data.length > 0) {
            sel.value = data[0].id;
            selectedTeacher = data[0].id;
            loadSlots(selectedTeacher);
        }
    });

    generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
};

// Fetch slots for a teacher
function loadSlots(teacherId) {
    if (!teacherId) return;
    fetch(`/faculty_slots/${teacherId}`)
    .then(r => r.json())
    .then(data => {
        slots = data;
        updateSlotsList();
        generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
    });
}

// Add slot
document.getElementById("slotForm").addEventListener("submit", function(e) {
    e.preventDefault();
    const teacherId = document.getElementById("teacherSelect").value;
    const date = document.getElementById("slotDate").value;
    const start = document.getElementById("startTime").value;
    const end = document.getElementById("endTime").value;

    if (!teacherId || !date || !start || !end) {
        alert("All fields are required!");
        return;
    }

    if (start >= end) {
        alert("End time must be after start time!");
        return;
    }

    fetch("/create_slot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            teacher_id: teacherId,
            date: date,
            start_time: start,
            end_time: end
        })
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("successMessage").classList.add("show");
        setTimeout(() => {
            document.getElementById("successMessage").classList.remove("show");
        }, 3000);
        loadSlots(teacherId);
        e.target.reset();
    });
});

// Calendar functions
const monthNames = ["January","February","March","April","May","June",
                    "July","August","September","October","November","December"];
const dayNames = ["Sun","Mon","Tue","Wed","Thu","Fri","Sat"];

function generateCalendar(year, month) {
    const calendar = document.getElementById("calendar");
    const monthHeader = document.getElementById("currentMonth");
    monthHeader.textContent = `${monthNames[month]} ${year}`;
    calendar.innerHTML = "";

    dayNames.forEach(day => {
        const dayHeader = document.createElement("div");
        dayHeader.className = "day-header";
        dayHeader.textContent = day;
        calendar.appendChild(dayHeader);
    });

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();

    // Empty days before month start
    for (let i = 0; i < firstDay; i++) {
        const emptyDiv = document.createElement("div");
        emptyDiv.className = "calendar-day other-month";
        calendar.appendChild(emptyDiv);
    }

    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement("div");
        dayDiv.className = "calendar-day";
        const dateStr = `${year}-${String(month+1).padStart(2,'0')}-${String(day).padStart(2,'0')}`;

        const dayNumber = document.createElement("div");
        dayNumber.className = "day-number";
        dayNumber.textContent = day;
        dayDiv.appendChild(dayNumber);

        const daySlots = slots.filter(s => s.date === dateStr);
        daySlots.forEach(s => {
            const slotDiv = document.createElement("div");
            slotDiv.className = "slot";
            slotDiv.textContent = `${s.start} - ${s.end}`;
            dayDiv.appendChild(slotDiv);
        });

        if (daySlots.length > 0) {
            dayDiv.classList.add("selected");
        }
        calendar.appendChild(dayDiv);
    }
}

// Change month
function changeMonth(direction) {
    currentDate.setMonth(currentDate.getMonth() + direction);
    generateCalendar(currentDate.getFullYear(), currentDate.getMonth());
}

// Update slot list
function updateSlotsList() {
    const slotsList = document.getElementById("slotsList");
    if (slots.length === 0) {
        slotsList.innerHTML = '<p style="text-align: center; color: #666; font-style: italic;">No slots available.</p>';
        return;
    }

    slotsList.innerHTML = slots.map(s => `
        <div class="slot-item">
            <div class="slot-info">
                <div class="slot-name">Teacher ID: ${s.teacher_id}</div>
                <div class="slot-time">${s.date} • ${s.start} - ${s.end}</div>
                ${s.booked ? `<div style="color: red; font-size: 0.8rem;">Booked</div>` : `<div style="color: green; font-size: 0.8rem;">Available</div>`}
            </div>
        </div>
    `).join("");
}
