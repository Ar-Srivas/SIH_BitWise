document.addEventListener("DOMContentLoaded", () => {
    const qrCodeContainer = document.getElementById("qr-code");
    const statusMessage = document.getElementById("status-message");
    let qrUpdateInterval;
    const teacherId = sessionStorage.getItem("teacherId");
    console.log(teacherId);
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
            const date = new Date().toISOString().split('T')[0];
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
            }, 60000);
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
            generateQrCode(new_qrvalue);
        } catch (error) {
            statusMessage.textContent = `Error updating token: ${error.message}`;
            clearInterval(qrUpdateInterval);
        }
    }

    document.getElementById('start-session-btn').addEventListener('click', startSession);
});