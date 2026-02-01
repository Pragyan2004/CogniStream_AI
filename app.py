from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from groq import Groq
import asyncio
import os
from dotenv import load_dotenv
import markdown
from datetime import datetime
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///learning.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    saved_responses = db.relationship('SavedResponse', backref='user', lazy=True)

class SavedResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    response_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CourseProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.String(50), nullable=False)
    progress = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Groq Client
def get_groq_client(api_key):
    return Groq(api_key=api_key)

async def ask_groq(prompt: str, api_key: str, model="llama-3.3-70b-versatile") -> str:
    try:
        client = get_groq_client(api_key)
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI teaching assistant. Reply in Markdown format with well-structured sections, code examples when appropriate, and learning tips."
                },
                {"role": "user", "content": prompt}
            ],
            model=model,
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def run_agents(topic, api_key, user_id=None):
    prompts = {
        "professor": f"Create a comprehensive knowledge base on '{topic}' including:\n1. Key concepts and definitions\n2. Fundamental principles\n3. Real-world applications\n4. Common misconceptions\n5. Future trends\nFormat in Markdown with headings, bullet points, and examples.",
        "advisor": f"Design a structured learning roadmap for '{topic}' covering:\n1. Beginner level (0-3 months)\n2. Intermediate level (3-6 months)\n3. Advanced level (6-12 months)\n4. Expert level (12+ months)\nInclude time estimates, prerequisites, and milestone projects.",
        "librarian": f"Curate learning resources for '{topic}' in this format:\n## 📚 Books\n- [Title] by Author (Year) - Description\n\n## 🎥 Video Courses\n- [Course Name] on Platform - Description\n\n## 📄 Documentation\n- [Resource Name] - Description\n\n## 🚀 Projects\n- [Project Idea] - Skills practiced",
        "assistant": f"Create interactive learning materials for '{topic}':\n## Practice Exercises\n1. Basic exercises with solutions\n2. Intermediate challenges\n3. Advanced problems\n\n## Projects\n1. Beginner project with requirements\n2. Intermediate project\n3. Advanced real-world application\n\nInclude code snippets where applicable."
    }
    
    tasks = [ask_groq(prompts[role], api_key) for role in prompts]
    raw_responses = await asyncio.gather(*tasks)

    responses = {}
    for role, markdown_text in zip(prompts.keys(), raw_responses):
        html = markdown.markdown(
            markdown_text,
            extensions=["fenced_code", "nl2br", "tables", "sane_lists", "codehilite"]
        )
        responses[role] = html
        
        # Save response to database if user is logged in
        if user_id:
            saved_response = SavedResponse(
                user_id=user_id,
                topic=topic,
                response_type=role,
                content=html
            )
            db.session.add(saved_response)
    
    if user_id:
        db.session.commit()
    
    return responses

COURSES_DATA = {
    "python": {
        "title": "Python Programming",
        "description": "Master the world's most popular programming language. From basic syntax to advanced AI libraries.",
        "duration": "3 months",
        "level": "Beginner",
        "icon": "🐍",
        "modules": [
            {"title": "Python Basics", "duration": "2 weeks", "video_id": "kqtD5dpn9C8", "external_url": "https://docs.python.org/3/tutorial/index.html"},
            {"title": "Data Structures", "duration": "3 weeks", "video_id": "8hly31xKli0", "external_url": "https://realpython.com/python-data-structures/"},
            {"title": "OOP in Python", "duration": "2 weeks", "video_id": "Ej_02ICOIgs", "external_url": "https://realpython.com/python3-object-oriented-programming/"},
            {"title": "Web Development with Flask", "duration": "3 weeks", "video_id": "Z1RJmh_OqeA", "external_url": "https://flask.palletsprojects.com/en/stable/tutorial/"},
            {"title": "Data Analysis", "duration": "2 weeks", "video_id": "r-uOLxNrNk8", "external_url": "https://pandas.pydata.org/docs/getting_started/index.html"}
        ]
    },
    "webdev": {
        "title": "Web Development",
        "description": "Learn to build modern, responsive websites using HTML, CSS, JavaScript, and professional frameworks.",
        "duration": "4 months",
        "level": "Intermediate",
        "icon": "🌐",
        "modules": [
            {"title": "HTML5 & Semantic Web", "duration": "2 weeks", "video_id": "UB1O30fS-EE", "external_url": "https://developer.mozilla.org/en-US/docs/Learn/HTML"},
            {"title": "CSS3 & Modern Layouts", "duration": "3 weeks", "video_id": "yfoY53QXEnI", "external_url": "https://developer.mozilla.org/en-US/docs/Learn/CSS"},
            {"title": "JavaScript Fundamentals", "duration": "4 weeks", "video_id": "hdI2bqOjy3c", "external_url": "https://javascript.info/"},
            {"title": "React.js Framework", "duration": "4 weeks", "video_id": "w7ejDZ8SWv8", "external_url": "https://react.dev/learn"},
            {"title": "Backend Integration", "duration": "3 weeks", "video_id": "vjf774gz1L0", "external_url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs"}
        ]
    },
    "ml": {
        "title": "Machine Learning",
        "description": "Dive deep into the world of Artificial Intelligence and build predictive models using real-world data.",
        "duration": "6 months",
        "level": "Advanced",
        "icon": "🤖",
        "modules": [
            {"title": "Mathematics for ML", "duration": "4 weeks", "video_id": "K73W8N08Pzo", "external_url": "https://mml-book.github.io/"},
            {"title": "Supervised Learning", "duration": "5 weeks", "video_id": "7eh4d6sabA0", "external_url": "https://scikit-learn.org/stable/supervised_learning.html"},
            {"title": "Unsupervised Learning", "duration": "4 weeks", "video_id": "j9Wp-oXp_Hk", "external_url": "https://scikit-learn.org/stable/unsupervised_learning.html"},
            {"title": "Deep Learning & Neural Networks", "duration": "6 weeks", "video_id": "aircAruvnKk", "external_url": "https://www.tensorflow.org/tutorials"},
            {"title": "MLOps & Deployment", "duration": "5 weeks", "video_id": "O3h7CAdYn78", "external_url": "https://ml-ops.org/"}
        ]
    },
    "data-science": {
        "title": "Data Science",
        "description": "Extract insights from complex data and master the tools used by professional data scientists.",
        "duration": "5 months",
        "level": "Intermediate",
        "icon": "📊",
        "modules": [
            {"title": "Statistical Analysis", "duration": "4 weeks", "video_id": "0K99qV6IPh8", "external_url": "https://onlinestatbook.com/2/index.html"},
            {"title": "Data Visualization", "duration": "3 weeks", "video_id": "673_A4-lRCA", "external_url": "https://seaborn.pydata.org/tutorial.html"},
            {"title": "SQL & Big Data", "duration": "4 weeks", "video_id": "HXV3zeQKqGY", "external_url": "https://sqlbolt.com/"},
            {"title": "Predictive Modeling", "duration": "5 weeks", "video_id": "Wngoqn7JAdE", "external_url": "https://machinelearningmastery.com/predictive-modeling/ "},
            {"title": "Data Science Capstone", "duration": "4 weeks", "video_id": "i2G_m9G2Fos", "external_url": "https://www.kaggle.com/learn/overview"}
        ]
    },
    "cybersecurity": {
        "title": "Cybersecurity",
        "description": "Protect systems and networks from digital attacks and become an information security expert.",
        "duration": "4 months",
        "level": "Advanced",
        "icon": "🔒",
        "modules": [
            {"title": "Network Security", "duration": "3 weeks", "video_id": "U_W3_v6shY8", "external_url": "https://www.comptia.org/content/guides/what-is-network-security"},
            {"title": "Ethical Hacking", "duration": "4 weeks", "video_id": "fNzpcB7ODxQ", "external_url": "https://www.eccouncil.org/cybersecurity-exchange/ethical-hacking/what-is-ethical-hacking/"},
            {"title": "Cryptography", "duration": "3 weeks", "video_id": "jhXCTbFnK8o", "external_url": "https://www.tutorialspoint.com/cryptography/index.htm"},
            {"title": "Incident Response", "duration": "3 weeks", "video_id": "f62H3S9W4S0", "external_url": "https://csrc.nist.gov/publications/detail/sp/800-61/rev-2/final"},
            {"title": "Cloud Security", "duration": "3 weeks", "video_id": "jRE9N2B0t80", "external_url": "https://www.cloudflare.com/learning/cloud/what-is-cloud-security/"}
        ]
    },
    "blockchain": {
        "title": "Blockchain Development",
        "description": "Build decentralized applications and master the substrate of the future internet.",
        "duration": "5 months",
        "level": "Advanced",
        "icon": "⛓️",
        "modules": [
            {"title": "Blockchain Fundamentals", "duration": "3 weeks", "video_id": "gyMwXuJrbJQ", "external_url": "https://ethereum.org/en/learn/"},
            {"title": "Smart Contracts (Solidity)", "duration": "5 weeks", "video_id": "M576WGiDBdQ", "external_url": "https://docs.soliditylang.org/"},
            {"title": "Web3 Integration", "duration": "4 weeks", "video_id": "pDSidvi1n6A", "external_url": "https://docs.ethers.org/v6/"},
            {"title": "DApp Development", "duration": "4 weeks", "video_id": "va6_7YfAatU", "external_url": "https://trufflesuite.com/docs/"},
            {"title": "Governance & DAOs", "duration": "4 weeks", "video_id": "YvIsSreV13s", "external_url": "https://dao-stack.readthedocs.io/en/latest/"}
        ]
    }
}

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/courses")
def courses():
    available_courses = [{"id": k, **v} for k, v in COURSES_DATA.items()]
    return render_template("courses.html", courses=available_courses)

@app.route("/course/<course_id>")
def course_detail(course_id):
    course = COURSES_DATA.get(course_id)
    if not course:
        flash("Course not found.", "error")
        return redirect(url_for('courses'))
    return render_template("course_detail.html", course=course, course_id=course_id)

@app.route("/learn", methods=["GET", "POST"])
def learn():
    if request.method == "POST":
        topic = request.form.get("topic")
        api_key = os.getenv("GROQ_API_KEY")
        
        if not topic or not api_key:
            flash("Please enter a topic and ensure GROQ_API_KEY is set.", "error")
            return redirect(url_for("learn"))
        
        user_id = current_user.id if current_user.is_authenticated else None
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(run_agents(topic, api_key, user_id))
        
        return render_template("learn.html", topic=topic, responses=responses)
    
    return render_template("learn.html")

SOCIAL_LINKS = {
    "twitter": "https://twitter.com/cognistream_ai",
    "github": "https://github.com/cognistream-ai",
    "discord": "https://discord.gg/cognistream",
    "linkedin": "https://linkedin.com/company/cognistream-ai"
}

@app.context_processor
def inject_social_links():
    return dict(social_links=SOCIAL_LINKS)

@app.route("/resources")
def resources():
    resources_list = [
        {"title": "FreeCodeCamp", "type": "Platform", "url": "https://freecodecamp.org", "desc": "Thousands of hours of free coding tutorials and certifications."},
        {"title": "Coursera", "type": "Platform", "url": "https://coursera.org", "desc": "Online courses from top universities and industry leaders."},
        {"title": "MDN Web Docs", "type": "Documentation", "url": "https://developer.mozilla.org", "desc": "The definitive resource for web platform technologies."},
        {"title": "PyTorch Tutorials", "type": "Documentation", "url": "https://pytorch.org/tutorials/", "desc": "Official tutorials for mastering deep learning with PyTorch."},
    ]
    community_video = {"video_id": "aircAruvnKk", "title": "Inside our AI Community"}
    return render_template("resources.html", resources=resources_list, community_video=community_video)

@app.route("/profile")
@login_required
def profile():
    saved_responses = SavedResponse.query.filter_by(user_id=current_user.id).order_by(SavedResponse.created_at.desc()).limit(10).all()
    return render_template("profile.html", saved_responses=saved_responses)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

@app.route("/terms")
def terms():
    return render_template("terms.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/save_response", methods=["POST"])
@login_required
def save_response():
    data = request.json
    response = SavedResponse(
        user_id=current_user.id,
        topic=data['topic'],
        response_type=data['type'],
        content=data['content']
    )
    db.session.add(response)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/generate", methods=["POST"])
def api_generate():
    data = request.json
    topic = data.get("topic")
    api_key = os.getenv("GROQ_API_KEY")
    
    if not topic:
        return jsonify({"error": "Topic required"}), 400
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(run_agents(topic, api_key))
    
    return jsonify(responses)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)