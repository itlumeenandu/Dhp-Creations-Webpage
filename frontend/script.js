const API = "https://dhp-creations-webpage-1.onrender.com";

const form = document.getElementById("form");
const statusText = document.getElementById("status");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        talent: document.getElementById("role").value,
        message: document.getElementById("message").value
    };

    await fetch(API + "/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    statusText.innerText = "✅ Application submitted!";
    form.reset();
});

const cards = document.querySelectorAll(".card");

window.addEventListener("scroll", () => {
    cards.forEach(card => {
        const top = card.getBoundingClientRect().top;
        if (top < window.innerHeight - 100) {
            card.classList.add("show");
        }
    });
});

// Load user data
async function loadData() {
    const res = await fetch(API + "/data");
    const users = await res.json();

    let html = "<table><tr><th>Name</th><th>Email</th><th>Role</th><th>Message</th></tr>";
    users.forEach(u => {
        html += `<tr>
            <td>${u.name}</td>
            <td>${u.email}</td>
            <td>${u.role}</td>
            <td>${u.message}</td>
        </tr>`;
    });
    html += "</table>";
    document.getElementById("submitted-data").innerHTML = html;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        role: document.getElementById("role").value,
        message: document.getElementById("message").value
    };
    await fetch(API + "/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    document.getElementById("status").innerText = "Application Submitted ✅";
    form.reset();
    loadData();
});

loadData(); // initial load