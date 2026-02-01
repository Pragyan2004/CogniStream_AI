# 🧠 CogniStream AI  
### Master Any Subject with Precision

![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Framework](https://img.shields.io/badge/framework-Flask-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Style](https://img.shields.io/badge/style-Tailwind_CSS-38B2AC.svg)
![Open Source](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)

**CogniStream AI** is a state-of-the-art educational platform that leverages **High-Speed Hybrid Intelligence** to democratize personalized learning.  
By combining the power of **Llama 3.3 (via Groq API)** with a premium UI, it transforms curiosity into expertise through **structured roadmaps, curated resources, and hands-on practice**.

---

## ✨ Key Features

### 🚀 AI Learning Lab
Enter any topic and receive a **4-pillar deep-dive**:

- **👨‍🏫 Professor** – Core concepts & strong foundations  
- **🧭 Advisor** – Structured milestones (Beginner → Expert)  
- **📚 Librarian** – Curated books, courses & documentation  
- **🛠️ Workshop** – Practical exercises & real-world projects  

### 📚 Curated Course Explorer
Pre-built learning paths for:
- Python
- Web Development
- Machine Learning
- Cybersecurity
- Blockchain

### 🎥 Immersive Video Integration
Integrated **YouTube modal player** for distraction-free learning.

### 📈 Progress Tracking
- Visual progress indicators  
- Module completion status  

### 🛡️ Secure Profiles
- Personalized goals  
- Saved learning history  
- SQLAlchemy-backed storage  

### 🎨 Premium UI/UX
- Glassmorphism design  
- Smooth animations  
- Vibrant gradients  
- Tailwind CSS powered  

---

## 📸 Screenshots

### 🏠 Home Page
<img width="1441" height="924" alt="Screenshot 2026-02-01 211306" src="https://github.com/user-attachments/assets/2e7f07cb-7dc8-432d-943b-9e930401a988" />
<img width="1446" height="726" alt="Screenshot 2026-02-01 211316" src="https://github.com/user-attachments/assets/c98ea3f9-103f-4db3-8140-cd126343aa8c" />



### 📚 Course Explorer
<img width="1415" height="902" alt="Screenshot 2026-02-01 211332" src="https://github.com/user-attachments/assets/4f971208-f2fc-4081-a44f-447330e48da9" />
<img width="1408" height="792" alt="Screenshot 2026-02-01 211344" src="https://github.com/user-attachments/assets/f464d9f1-8afa-40e3-a0b6-04f6d5d46ebc" />

### 🤖 AI Learning Lab
<img width="1481" height="689" alt="Screenshot 2026-02-01 211356" src="https://github.com/user-attachments/assets/141c4489-cde5-45d5-a3ae-9e6303920259" />
<img width="1373" height="838" alt="Screenshot 2026-02-01 211419" src="https://github.com/user-attachments/assets/7a8a49fb-c450-409f-a78f-669495bbb6bc" />

### 👤 Resources
<img width="1456" height="924" alt="Screenshot 2026-02-01 211430" src="https://github.com/user-attachments/assets/382b752b-db59-4268-b2d0-c5cfce0a9ad9" />

### 🎥 About
<img width="1448" height="924" alt="Screenshot 2026-02-01 211439" src="https://github.com/user-attachments/assets/fb7e9fee-26da-492c-b883-e139c0d16778" />

### Contact
<img width="1414" height="927" alt="Screenshot 2026-02-01 211454" src="https://github.com/user-attachments/assets/4d6846d4-fd34-49f6-a2da-58e6f1ab49c4" />

---

```
CogniStream_AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── Procfile
├── LICENSE
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── courses.html
│ ├── course_detail.html
│ ├── learn.html
│ ├── resources.html
│ └── profile.html
├── static/
│ ├── css/styles.css
│ ├── js/main.js
│ └── images/
│ ├── logo.png
│ ├── hero-bg.jpg
│ └── screenshots/
├── database/
│ └── learning.db
└── docs/
├── API.md
└── DEPLOYMENT.md
```

---

## 🛠️ Tech Stack

### Backend
- Python 3.8+
- Flask
- Flask-SQLAlchemy
- Flask-Login
- python-dotenv

### AI Integration
- **Groq API**
- **Llama 3.3 70B**
- Async inference

### Frontend
- HTML5
- Tailwind CSS
- JavaScript (ES6+)
- Font Awesome
- Markdown rendering

### Database
- SQLite (development)
- SQLAlchemy ORM

### Deployment
- Gunicorn
- Render / Heroku ready

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key
- Git

### Installation

```bash
git clone https://github.com/Pragyan2004/CogniStream_AI.git
cd CogniStream_AI
```
## Create virtual environment:

# Windows
```
python -m venv venv
venv\Scripts\activate
```

# Linux / Mac
```
python3 -m venv venv
source venv/bin/activate
```

## Install dependencies:

    pip install -r requirements.txt


## Configure environment:

    cp .env.example .env


## Initialize database:
```
python
>>> from app import db, app
>>> with app.app_context():
...     db.create_all()
...     print("Database initialized successfully!")
```

---

## Run app:

    python app.py
---
    Open browser → http://localhost:5000

## 📦 Environment Variables
```
SECRET_KEY=your_secret_key
FLASK_ENV=development
FLASK_APP=app.py
```
    GROQ_API_KEY=your_groq_api_key

    DATABASE_URL=sqlite:///database/learning.db

## 🔌 API Endpoints
```
Method	Endpoint	Description
GET	/	Home page
GET	/courses	Course listing
GET	/course/<id>	Course details
GET	/learn	AI Learning Lab
POST	/learn	Generate learning plan
GET	/resources	Resources
GET	/profile	User profile
POST	/save_response	Save AI output
POST	/api/generate	AI API
```
---
## 📄 License

This project is licensed under the MIT License.

## 🏗️ Project Structure


