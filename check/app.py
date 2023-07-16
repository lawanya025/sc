from flask import Flask, render_template, request, session
import random


app = Flask(__name__)
app.secret_key = 'your_secret_key'

import os
import openai
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = "https://openairedflags.openai.azure.com/"
openai.api_key = "41d6760e6a674dae891eef613eae5b69"

# Define a global list to store selected symptoms



# Define the route to handle symptom selection and generate responses
backpain_template = """ using symptoms from symptoms checker genrate a paragraph including information about symptom, possible diagnosis,causes,risk factors and treatment.
give a informational paragraph.

{input}"""



def azure_openai_chat(prompt):
    response = openai.Completion.create(
        engine="symptoms",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/symptom-checker', methods=['GET', 'POST'])
def symptom_checker():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = " ".join(selected_symptoms.split(","))
        prompt = backpain_template.format(input=input_text)
        diagnosis_info = azure_openai_chat(prompt)

        # Redirect to result page with selected symptoms and diagnosis information
        return render_template('result.html', selected_symptoms=selected_symptoms, diagnosis_info=diagnosis_info)

    return render_template('symptom_checker.html')






@app.route('/show-questions', methods=['GET', 'POST'])
def show_questions():
    selected_questions = request.form.getlist('question')
    return render_template('questions.html', question=selected_questions)

@app.route('/checking', methods=['POST'])
def check_selection():
    question = request.form.getlist('question')

    if any(question):
        # At least one checkbox is selected, display the warning message
        return render_template('yes.html')
    else:
        # No checkboxes selected, redirect to a different route
        return render_template('interview.html')

@app.route('/more', methods=['GET', 'POST'])
def more():
    selected_questions = request.form.getlist('interview')
    return render_template('more.html', interview=selected_questions)


@app.route('/yellow-flags', methods=['GET', 'POST'])
def yellow_flags():
    selected_questions = request.form.getlist('yellow_flags')
    return render_template('yellow.html', yellow_flags=selected_questions)

@app.route('/yes-again', methods=['GET', 'POST'])
def yes_again():
    selected_questions = request.form.getlist('yellow_flags')
    return render_template('yes.html', yellow_flags=selected_questions)



if __name__ == '__main__':
    app.run(debug=True)


