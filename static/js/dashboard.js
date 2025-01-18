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

        // Send meal consumption data to the backend
        const protein = parseFloat(document.getElementById("mealProtein").textContent);
        const carbs = parseFloat(document.getElementById("mealCarbs").textContent);

        fetch("/consume_meal", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                meal_name: currentMeal,
                protein: protein,
                carbs: carbs
            })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.error) {
                // Update the profile section dynamically
                document.querySelector(".profile-total-meals").textContent = data.total_meals;
                document.querySelector(".profile-total-protein").textContent = `${data.total_protein}g`;
                document.querySelector(".profile-total-carbs").textContent = `${data.total_carbs}g`;
            } else {
                console.error("Error updating meal consumption:", data.error);
            }
        })
        .catch(error => {
            console.error("Error sending meal consumption data:", error);
        });
    }

    // Close the modal
    const mealModal = bootstrap.Modal.getInstance(document.getElementById("mealModal"));
    mealModal.hide();
}
