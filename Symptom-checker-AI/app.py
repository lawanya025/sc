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
backpain_template = """ using symptoms from symptoms checker we get\
primary symptom.

{input}"""

template1= """ using question1 from OPQRST interview, we get\
information about onset(starting) of pain.

{input}"""

template2= """ using question2 from OPQRST interview, we get\
information about Provocation(stimulation) of pain.

{input}"""

template3= """ using question3 from OPQRST interview, we get\
information about intensity(quality) of pain.

{input}"""

template4= """ using question4 from OPQRST interview, we get\
information about region of pain.

{input}"""

template5= """ using question5 from OPQRST interview, we get\
information about severity of pain.\
severity is On a scale of 0 to 10, with 0 being no pain or discomfort and 10 being the worst pain imaginable.

{input}"""

template6= """ using question6 from OPQRST interview, we get\
information about duration of pain.\
using above all collected information, genrate a paragraph about diagnosis of possible disease it's causes , risk factors and treatment.
give a informational paragraph. Also give references for the information given

{input}"""





def azure_openai_chat(prompt):
    response = openai.Completion.create(
        engine="symptoms",
        prompt=prompt,
        max_tokens=400,
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
        # Redirect to result page with selected symptoms and diagnosis information
        return render_template('questions.html', selected_symptoms=selected_symptoms)

    return render_template('symptom_checker.html')

@app.route('/diagnosiss', methods=['GET', 'POST'])
def final_diagnosis():
    if request.method == 'POST':
        question = request.form.get('symptoms')
        ques1 = request.form.get('question1')
        ques2 = request.form.get('question2')
        ques3 = request.form.get('question3')
        ques4 = request.form.get('question4')
        ques5 = request.form.get('question5')
        ques6 = request.form.get('question6')

        # Construct prompts for each question
        prompt0 = backpain_template.format(input=question)
        prompt1 = template1.format(input=ques1)
        prompt2 = template2.format(input=ques2)
        prompt3 = template3.format(input=ques3)
        prompt4 = template4.format(input=ques4)
        prompt5 = template5.format(input=ques5)
        prompt6 = template6.format(input=ques6)

        # Combine all prompts into a single prompt
        prompt = prompt0 + prompt1 + prompt2 + prompt3 + prompt4 + prompt5 + prompt6

        diagnosis_info = azure_openai_chat(prompt)

        # Redirect to result page with diagnosis information
        return render_template('result.html', selected_symptoms=question, diagnosis_info=diagnosis_info)

    return render_template('symptom_checker.html')


@app.route('/show-questions', methods=['GET', 'POST'])
def show_questions():
    # Fetch parameters from the URL
    diagnosis_info = request.args.get('diagnosis_info')
    ques1 = request.args.get('question1')
    ques2 = request.args.get('question2')
    ques3 = request.args.get('question3')
    ques4 = request.args.get('question4')
    ques5 = request.args.get('question5')
    ques6 = request.args.get('question6')

    return render_template('result.html', diagnosis_info=diagnosis_info, question1=ques1, question2=ques2, question3=ques3, question4=ques4, question5=ques5, question6=ques6)




@app.route('/checking', methods=['POST'])
def check_selection():
    question = request.form.getlist('question')

    if any(question):
        # At least one checkbox is selected, display the warning message
        return render_template('yes.html')
    else:
        # No checkboxes selected, redirect to a different route
        return render_template('interview.html')

@app.route('/vindicate', methods=['GET', 'POST'])
def vindicate():
    selected_questions = request.form.getlist('interview')
    return render_template('vindicate.html', interview=selected_questions)


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


