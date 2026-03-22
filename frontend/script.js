const API = "https://dhp-creations-webpage-1.onrender.com";

const form = document.getElementById("form");
const statusText = document.getElementById("status");

let isSubmitting = false;

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

        // ✅ safer handling
        if (!res.ok) {
            const text = await res.text();
            throw new Error(text || "Failed");
        }

        const result = await res.json();
        console.log(result);

        statusText.innerText = "✅ Application submitted!";
        form.reset();
        loadData();

    } catch (err) {
        console.error(err);
        statusText.innerText = "❌ Submission failed (check backend)";
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


// ✅ SAFE LOAD DATA
async function loadData() {
    try {
        const res = await fetch(API + "/data");
        const users = await res.json();

        if (!users || !users.data) return;

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