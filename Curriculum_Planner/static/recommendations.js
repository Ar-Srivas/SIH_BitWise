function highlightResources() {
    const items = document.querySelectorAll("#recommendations li");
    items.forEach(item => {
        if (item.textContent.includes("Easy")) {
            item.style.backgroundColor = "#e0f7fa";
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("recommendations")) {
        highlightResources();
    }
});
