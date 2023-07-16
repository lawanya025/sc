from flask import Flask, render_template, request

app = Flask(__name__)

import os
import openai
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_base = "https://openairedflags.openai.azure.com/"
openai.api_key = "41d6760e6a674dae891eef613eae5b69"


backpain_template = """ using symptoms from symptoms checker genrate a paragraph including information about symptom, possible diagnosis,causes,risk factors and treatment.
give a informational paragraph.

{input}"""

redflag_template = """generate a list of red flags (in medical terms) based on symptoms from the symptom checker and put '.' after each line.\
make sure 2 '.' are never together.\

Here is a question:
{input}"""

opqrst_template = """for a particular type of symptom\
generate OPQRST questions to answer and put '?' after each question of the acronym.\
make sure 2 '?' are never together.\

Here is a question:
{input}"""

vindicate_template = """for a particular type of symptom\
generate VINDICATE questions to answer and put '?' after each question of the acronym.\
make sure 2 '?' are never together.\

Here is a question:
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

@app.route('/redflag', methods=['GET', 'POST'])
def redflag():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        prompt = redflag_template.format(input=input_text)
        red_quest = azure_openai_chat(prompt)

        questions = []
        for line in red_quest.split("\n"):
            if "." in line:
                line = line.replace(".", "")
                if line.strip():
                    questions.append(line.strip() + ".")
            else:
                questions.append(line)

        # Redirect to redflag page with selected symptoms and redflag questions
        return render_template('redflag.html', selected_symptoms=selected_symptoms, red_quest=questions)

    return render_template('results.html')


@app.route('/opqrst', methods=['GET', 'POST'])
def opqrst():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        prompt = opqrst_template.format(input=input_text)
        interview_quest = azure_openai_chat(prompt)

        questions = []
        for line in interview_quest.split("\n"):
            if "?" in line:
                questions.append(line[:line.find("?") + 1])
            else:
                questions.append(line)

        # Redirect to OPQRST page with selected symptoms and interview questions
        return render_template('opqrst.html', selected_symptoms=selected_symptoms, interview_quest=questions)

    return render_template('results.html')

@app.route('/vindicate', methods=['GET', 'POST'])
def vindicate():
    if request.method == 'POST':
        selected_symptoms = request.form.get('symptoms')
        input_text = selected_symptoms
        prompt = vindicate_template.format(input=input_text)
        vind_quest = azure_openai_chat(prompt)

        questions = []
        for line in vind_quest.split("\n"):
            if "?" in line:
                questions.append(line[:line.find("?") + 1])
            else:
                questions.append(line)

        # Redirect to VINDICATE page with selected symptoms and VINDICATE questions
        return render_template('vindicate.html', selected_symptoms=selected_symptoms, vind_quest=questions)

    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True)
