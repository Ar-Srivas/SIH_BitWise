document.addEventListener("DOMContentLoaded", () => {
    const qrCodeContainer = document.getElementById("qr-code");
    const statusMessage = document.getElementById("status-message");
    let qrUpdateInterval;
    const teacherId = sessionStorage.getItem("teacherId");
    // const date = new Date().toISOString().split('T')[0];
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const date = `${year}-${month}-${day}`;
    console.log(teacherId);
    console.log(date);
    if (!teacherId) {
        window.location.href = "/";
        return;
    }

    function generateQrCode(qrvalue) {
        qrCodeContainer.innerHTML = "";
        const qr = qrcode(0, "L");
        qr.addData(qrvalue);
        qr.make();
        qrCodeContainer.innerHTML = qr.createImgTag(6, 8);
        statusMessage.textContent = 'QR Code is active. Please scan now.';
    }

    async function startSession() {
        try {
            console.log("hello there");
            // const date = new Date().toISOString().split('T')[0];
            const response = await fetch("/api/session/start", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    teacher_id: teacherId,
                    date: date,
                }),
            })
            if (!response.ok) {
                throw new Error("failed to start session");
            }
            const data = await response.json()
            console.log(data);
            const {initial_qrvalue} = data;

            statusMessage.textContent = 'Session started! Generating QR code...';
            generateQrCode(initial_qrvalue);

            qrUpdateInterval = setInterval(() => {
                updateQrValue(teacherId, date);
            }, 6000);
        } catch (error) {
            statusMessage.textContent = `Error: ${error}`;
        }
    }

    async function updateQrValue(teacherId, date) {
        try {
            const response = await fetch("/api/session/update-qrvalue", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    teacher_id: teacherId,
                    date: date, 
                }),
            });
            if (!response.ok) {
                throw new Error("failed to update qr value");
            }
            const data = await response.json();
            const {new_qrvalue} = data;
            console.log(new_qrvalue);
            if (new_qrvalue === "session_ended") {
                window.location.href = "/dashboard";
                return;
            }
            generateQrCode(new_qrvalue);
        } catch (error) {
            statusMessage.textContent = `Error updating token: ${error.message}`;
            clearInterval(qrUpdateInterval);
        }
    }

    async function endSession() {
        try {
            const response = await fetch("/api/session/end", {
                method: "POST",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    teacher_id: teacherId,
                    date: date,
                }),
            })
            console.log(response);
            if (!response.ok) {
                throw new Error("failed to end session");
            }
            const result = await response.json();
        } catch (error) {
            statusMessage.textContent = `error ending session: ${error.message}`;
        }
    }

    document.getElementById('start-session-btn').addEventListener('click', startSession);
    document.getElementById('end-session-btn').addEventListener('click', endSession);
});