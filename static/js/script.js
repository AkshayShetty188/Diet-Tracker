document.addEventListener("DOMContentLoaded", () => {
    console.log("Website Loaded with Animations!");

    // 1. Animate cards on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("animate__fadeInUp");
            }
        });
    });

    document.querySelectorAll(".card").forEach((card) => observer.observe(card));

    // 2. Button hover animations
    document.querySelectorAll("button").forEach((button) => {
        button.addEventListener("mouseenter", () => button.classList.add("animate__pulse"));
        button.addEventListener("mouseleave", () => button.classList.remove("animate__pulse"));
    });

    // 3. Confirmation for meal logging
    const yesButton = document.getElementById("yes-btn");
    if (yesButton) {
        yesButton.addEventListener("click", (e) => {
            e.preventDefault(); // Prevent form submission
            const confirmation = document.getElementById("confirmation");
            const form = document.getElementById("meal-form");
            if (confirmation && form) {
                confirmation.classList.remove("d-none");
                form.classList.add("d-none");
            }
        });
    }

    // 4. Tooltip for interactive elements
    const tooltipElements = document.querySelectorAll("[data-bs-toggle='tooltip']");
    tooltipElements.forEach((tooltipEl) => {
        new bootstrap.Tooltip(tooltipEl);
    });

    // 5. Scroll-to-top animation
    const scrollToTopButton = document.getElementById("scrollToTop");
    if (scrollToTopButton) {
        window.addEventListener("scroll", () => {
            if (window.scrollY > 300) {
                scrollToTopButton.classList.remove("d-none");
                scrollToTopButton.classList.add("animate__fadeIn");
            } else {
                scrollToTopButton.classList.add("d-none");
            }
        });

        scrollToTopButton.addEventListener("click", () => {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    // 6. Interactive plot enhancements (optional)
    if (typeof Plotly !== "undefined" && document.getElementById("chart")) {
        Plotly.newPlot("chart", window.plotData, window.plotLayout, { responsive: true });
    }
});
