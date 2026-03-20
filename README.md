# 🎬 DHP Creations – Casting Platform

A cinematic single-page web application for casting talent in short films and digital content creation.

---

## 🚀 Project Overview

DHP Creations is a creative production platform focused on:

* 🎥 Short Films
* 🎬 Cinematic Storytelling
* 🎞 Digital Content Creation

This web application allows users to:

* Submit their details for casting
* Store data in a database
* View submitted applications dynamically

---

## ✨ Features

* 🎭 Casting Application Form
* 💾 Data stored in PostgreSQL Database
* 🔄 Real-time data fetching and display
* 🎬 Cinematic UI Design (Dark Theme + Glass Effects)
* 📱 Responsive Single Page Website

---

## 🛠 Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* Python (Flask)
* Flask-CORS

### Database

* PostgreSQL

### Deployment

* Backend → Render
* Frontend → Netlify

---

## ⚙️ How It Works

1. User fills the casting form
2. Data is sent to backend (`/submit`)
3. Backend stores data in PostgreSQL
4. Frontend fetches data using (`/data`)
5. Submitted applications are displayed on the webpage

---

## 📂 Project Structure

```
Dhp-Creations-Webpage/
│
├── app.py
├── requirements.txt
├── index.html
├── style.css
├── script.js
└── README.md
```

---

## 🔗 API Endpoints

* `POST /submit` → Save user data
* `GET /data` → Fetch all submitted data

---

## 📦 Installation (Local Setup)

1. Clone repository:

```
git clone https://github.com/itlumeenandu/Dhp-Creations-Webpage.git
```

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run Flask app:

```
python app.py
```

---

## 🌐 Live Demo

* Frontend:
* Backend:

---

## 📌 Note

This project is developed as part of a **Modern Web Development Workflow** academic project, demonstrating:

* Full-stack development
* Database integration
* Deployment workflow
* CI/CD practices

---
