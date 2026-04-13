from flask import Flask, render_template, request, redirect, url_for
from questions import questions

app = Flask(__name__)

current_question = 0
score = 0
feedback = ""
selected_category = ""

@app.route('/', methods=['GET', 'POST'])
def home():
    global current_question, score, feedback, selected_category

    if request.method == 'POST':
        if 'category' in request.form:
            selected_category = request.form.get('category')
            current_question = 0
            score = 0
            feedback = ""

        else:
            answer = request.form.get('answer')

            if answer and len(answer) > 5:
                score += 1
                feedback = "Good Answer 👍"
            else:
                feedback = "Improve your answer ❗"

            current_question += 1

            if current_question >= len(questions[selected_category]):
                return redirect(url_for('result')) 
            
    total = len(questions[selected_category]) if selected_category else 0

    return render_template(
        "index.html",
        question=questions[selected_category][current_question] if selected_category else "",
        feedback=feedback,
        category=selected_category,
        current=current_question,
        total=total
    )

@app.route('/result')
def result():
    total = len(questions[selected_category])

    percentage = (score / total) * 100

    if percentage >= 80:
        message = "🔥 Excellent Performance"
    elif percentage >= 60:
        message = "👍 Good Job"
    elif percentage >= 40:
        message = "⚠️ Average"
    else:
        message = "❗ Needs Improvement"

    return render_template("result.html", 
                           score=score, 
                           total=total,
                           message=message,
                           category=selected_category)
if __name__ == "__main__":
    app.run(debug=True)