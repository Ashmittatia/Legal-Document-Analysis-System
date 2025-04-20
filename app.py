from flask import Flask, render_template, request
import joblib
import spacy
from utils.preprocessing import preprocess_text

model = joblib.load('model/classifier.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    entities = []

    if request.method == 'POST':
        text = request.form['document_text']
        preprocessed = preprocess_text(text)
        vectorized = vectorizer.transform([preprocessed])
        prediction = model.predict(vectorized)[0]

        doc = nlp(text)
        entities = [{'label': ent.label_, 'text': ent.text} for ent in doc.ents]

    return render_template('index.html', prediction=prediction, entities=entities)

if __name__ == '__main__':
    app.run(debug=True)
