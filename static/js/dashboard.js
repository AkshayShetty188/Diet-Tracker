let currentMeal = ""; // Store the current meal being viewed

// Function to open meal details in the modal
function openMealDetails(name, protein, carbs, recipe) {
    currentMeal = name; // Store the current meal name
    document.getElementById("mealName").textContent = name;
    document.getElementById("mealProtein").textContent = protein;
    document.getElementById("mealCarbs").textContent = carbs;
    document.getElementById("mealRecipe").textContent = recipe;
}

// Function to mark the meal as consumed
function markConsumed() {
    if (currentMeal) {
        const tickElement = document.getElementById(`tick-${currentMeal}`);
        if (tickElement) {
            tickElement.classList.remove("d-none"); // Show the tick mark
        }
    }

    // Close the modal
    const mealModal = bootstrap.Modal.getInstance(document.getElementById("mealModal"));
    mealModal.hide();
}
