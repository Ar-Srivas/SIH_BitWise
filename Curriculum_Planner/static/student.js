document.addEventListener("DOMContentLoaded", () => {
    const teacherSelect = document.getElementById('teacher-select');
    const datePicker = document.getElementById('date-picker');
    const slotsList = document.getElementById('slots-list');
    const message = document.getElementById('message');

    // For local testing, use http://127.0.0.1:8000. 
    // For deployment, replace with your Render URL.
    const API_BASE_URL = ''; 

    // 1. Fetch and populate teachers from the API
    async function loadTeachers() {
        try {
            const response = await fetch(`/teachers`);
            if (!response.ok) throw new Error('Failed to load teachers');
            
            const teachers = await response.json();
            
            teachers.forEach(teacher => {
                // The backend now sends name and id from the User table
                const option = new Option(teacher.name, teacher.id);
                teacherSelect.add(option);
            });
        } catch (error) {
            message.textContent = `Error: ${error.message}`;
        }
    }

    // 2. Fetch and display available slots based on selection
    async function fetchSlots() {
        const teacherId = teacherSelect.value;
        const date = datePicker.value;

        if (!teacherId || !date) {
            slotsList.innerHTML = '<p>Please select a teacher and a date.</p>';
            return;
        }

        slotsList.innerHTML = '<p>Loading slots...</p>';
        try {
            const response = await fetch(`/available_slots/${date}/${teacherId}`);
            if (!response.ok) throw new Error('Failed to fetch slots');
            const slots = await response.json();
            
            if (slots.length === 0) {
                slotsList.innerHTML = '<p>No available slots for this teacher on this day.</p>';
                return;
            }

            slotsList.innerHTML = ''; // Clear loading message
            slots.forEach(slot => {
                const slotElement = document.createElement('div');
                slotElement.className = 'slot';
                slotElement.innerHTML = `<span>Time: ${slot.start} - ${slot.end}</span>`;
                
                const bookButton = document.createElement('button');
                bookButton.textContent = 'Book Now';
                bookButton.onclick = () => bookSlot(slot.id);
                
                slotElement.appendChild(bookButton);
                slotsList.appendChild(slotElement);
            });
        } catch (error) {
            slotsList.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    // 3. Book the selected slot
    async function bookSlot(slotId) {
        message.textContent = 'Booking slot...';
        // For this demo, student_id is hardcoded. In a real app, this would come from a login session.
        // The seed script in your canvas doesn't create students, so we'll use a placeholder ID.
        const studentId = 99; 

        try {
            const response = await fetch(`/book_slot`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ slot_id: slotId, student_id: studentId })
            });
            const result = await response.json();
            if (!response.ok || !result.success) {
                throw new Error(result.message || 'Booking failed');
            }
            
            message.textContent = 'Slot booked successfully!';
            fetchSlots(); // Refresh the slot list to show it's no longer available
        } catch (error) {
            message.textContent = `Error: ${error.message}`;
        }
    }

    // Add event listeners to trigger fetching slots
    teacherSelect.addEventListener('change', fetchSlots);
    datePicker.addEventListener('change', fetchSlots);

    // Load the initial list of teachers when the page opens
    loadTeachers();
});