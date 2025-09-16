document.addEventListener("DOMContentLoaded", () => {
    const qrCodeContainer = document.getElementById("qr-code");
    const statusMessage = document.getElementById("status-message");
    let qrUpdateInterval;

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
            const response = await fetch("/api/session/start")
            if (!response.ok) {
                throw new Error("failed to start session");
            }
            const data = await response.json()
            const {teacherId, date, initialQr} = data;

            statusMessage.textContent = 'Session started! Generating QR code...';
            generateQrCode(initialToken);

            qrUpdateInterval = setInterval(() => {
                updateQrValue(teacherId, date);
            }, 6000);
        } catch (error) {
            statusMessage.textContent = `Error: ${error}`;
        }
    }

    async function updateQrValue(teacherId, date) {
        
    }
})