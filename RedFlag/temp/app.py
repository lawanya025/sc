from flask import Flask, render_template, request

app = Flask(__name__)

symptoms = {
    "Cough": ["Fever", "Sore throat", "Chest pain"],
    "Headache": ["Nausea", "Sensitivity to light", "Stiff neck"],
    "Abdominal pain": ["Nausea", "Vomiting", "Bloody tool"],
    "Back pain": ["Numbness or tingling in the legs", "Muscle weakness", "Difficulty walking"],

}

@app.route('/', methods=['GET', 'POST'])
def symptom_checker():
    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        related_symptoms = []
        for symptom in selected_symptoms:
            if symptom in symptoms:
                related_symptoms.extend(symptoms[symptom])
        return render_template('result.html', selected_symptoms=selected_symptoms, related_symptoms=related_symptoms)
    else:
        return render_template('symptom_checker.html', symptoms=symptoms)

if __name__ == '__main__':
    app.run(debug=True)
