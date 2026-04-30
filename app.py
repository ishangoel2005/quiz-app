from flask import Flask, render_template, request

app = Flask(__name__)

# Quiz questions - add/edit freely
QUESTIONS = [
    {
        "question": "Which AWS is used for virtual servers?",
        "options": ["S3", "EC2", "RDS", "Lambda"],
        "answer": "EC2"
    },
    {
        "question": "What tool automates CI/CD pipelines in this project?",
        "options": ["Jenkins", "Photoshop", "Excel", "Word"],
        "answer": "Jenkins"
    },
    {
        "question": "Which command builds a Docker image?",
        "options": ["docker run", "docker build", "docker pull", "docker kill"],
        "answer": "docker build"
    },
    {
        "question": "What triggers the Jenkins pipeline?",
        "options": ["Manual click", "GitHub webhook on push", "Email", "A cron job only"],
        "answer": "GitHub webhook on push"
    },
    {
        "question": "Which port does this Flask app run on?",
        "options": ["3000", "8080", "5000", "80"],
        "answer": "5000"
    },
    {
        "question": "Which port does this Flask app run on?",
        "options": ["3000", "8080", "5000", "80"],
        "answer": "5000"
    }
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", questions=QUESTIONS)


@app.route("/submit", methods=["POST"])
def submit():
    score = 0
    results = []
    for i, q in enumerate(QUESTIONS):
        user_answer = request.form.get(f"q{i}")
        is_correct = user_answer == q["answer"]
        if is_correct:
            score += 1
        results.append({
            "question": q["question"],
            "your_answer": user_answer or "No answer",
            "correct_answer": q["answer"],
            "is_correct": is_correct
        })
    return render_template("result.html", score=score, total=len(QUESTIONS), results=results)


@app.route("/health")
def health():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
