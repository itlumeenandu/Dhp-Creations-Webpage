const API = "http://127.0.0.1:5000";

const form = document.getElementById("form");
const dataDiv = document.getElementById("data");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        name: form.name.value,
        age: form.age.value,
        location: form.location.value,
        role: form.role.value,
        skills: form.skills.value,
        email: form.email.value,
        phone: form.phone.value,
        portfolio: form.portfolio.value
    };

    await fetch(API + "/submit", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    loadData();
});

async function loadData() {
    const res = await fetch(API + "/data");
    const users = await res.json();

    dataDiv.innerHTML = "";

    users.forEach(u => {
        dataDiv.innerHTML += `
        <div>
            <h3>${u.name} (${u.role})</h3>
            <p>${u.location}</p>
            <p>${u.skills}</p>
        </div>`;
    });
}

loadData();