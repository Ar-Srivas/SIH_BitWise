document.addEventListener("DOMContentLoaded", () => {
    // --- DOM Elements ---
    const firstButton = document.querySelector(".first.next");
    const secondButton = document.querySelector(".second.next");
    const resetButton = document.querySelector(".reset");
    const container = document.querySelector(".container");
    const predictionText = document.getElementById("prediction-text");

    // --- Form Inputs ---
    const greInput = document.getElementById("gre");
    const toeflInput = document.getElementById("toefl");
    const cgpaInput = document.getElementById("cgpa");
    const lorInput = document.getElementById("lor");
    const uniRatingInput = document.getElementById("uni_rating");
    
    // Object to store all student data
    const studentData = {};

    // --- Event Listeners ---
    firstButton.addEventListener("click", () => {
        // Collect data from the first form
        studentData.gre = parseFloat(greInput.value);
        studentData.toefl = parseFloat(toeflInput.value);
        studentData.cgpa = parseFloat(cgpaInput.value);

        // Animate to the next step
        container.classList.add("slider-two-active");
        container.classList.remove("slider-one-active");
    });

    secondButton.addEventListener("click", () => {
        // Collect data from the second form
        const researchRadio = document.querySelector('input[name="research"]:checked');
        studentData.lor = parseFloat(lorInput.value);
        studentData.uni_rating = parseInt(uniRatingInput.value);
        studentData.research = parseInt(researchRadio.value);

        // Animate to the final step and fetch prediction
        container.classList.add("slider-three-active");
        container.classList.remove("slider-two-active");
        
        getPrediction();
    });

    resetButton.addEventListener("click", () => {
        // Reset to the first step
        container.classList.add("slider-one-active");
        container.classList.remove("slider-three-active");
        predictionText.textContent = "Calculating...";
        
        // Clear all form fields
        document.querySelectorAll('input[type="number"]').forEach(input => input.value = '');
        document.querySelectorAll('input[type="radio"]').forEach(radio => radio.checked = false);
    });

    // --- API Call Function ---
    async function getPrediction() {
        try {
            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(studentData),
            });

            if (!response.ok) {
                throw new Error("Prediction request failed");
            }

            const result = await response.json();
            // console.log(result);
            const prediction = (parseFloat(result.prediction) * 100).toFixed(2);
            // console.log(admissionChance);
            predictionText.textContent = `${prediction}% Chance of Admission`;

        } catch (error) {
            console.error("Error fetching prediction:", error);
            predictionText.textContent = "Could not get prediction.";
        }
    }
});
