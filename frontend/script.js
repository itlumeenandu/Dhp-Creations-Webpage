const API = "https://dhp-creations-webpage-1.onrender.com";

const form = document.getElementById("form");
const statusText = document.getElementById("status");

let isSubmitting = false; // prevent double submit

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (isSubmitting) return;
    isSubmitting = true;

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        role: document.getElementById("role").value,
        message: document.getElementById("message").value
    };

    try {
        const res = await fetch(API + "/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();

        if (!res.ok) throw new Error(result.msg || "Failed");

        statusText.innerText = "✅ Application submitted!";
        form.reset();
        loadData();

    } catch (err) {
        statusText.innerText = "❌ Submission failed (check backend)";
        console.error(err);
    }

    isSubmitting = false;
});


// Scroll animation
const cards = document.querySelectorAll(".card");

window.addEventListener("scroll", () => {
    cards.forEach(card => {
        const top = card.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            card.classList.add("show");
        }
    });
});


// Load data
async function loadData() {
    try {
        const res = await fetch(API + "/data");
        const users = await res.json();

        let html = "<table><tr><th>Name</th><th>Email</th><th>Role</th><th>Message</th></tr>";

        users.data.forEach(u => {
            html += `<tr>
                <td>${u.Name}</td>
                <td>${u.Email}</td>
                <td>${u.Role}</td>
                <td>${u.Message}</td>
            </tr>`;
        });

        html += "</table>";
        document.getElementById("submitted-data").innerHTML = html;

    } catch (err) {
        console.error("Error loading data:", err);
    }
}

loadData();