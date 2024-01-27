from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__, template_folder='templates')

# Eğitilmiş modeli yükle
model = joblib.load('../preprocessing/randomForest_model.pkl')

# Ana sayfa
@app.route('/')
def index():
    return render_template('index.html')

# Tahminleri al ve sonucu göster
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Formdan gelen verileri al
            oda_sayisi = int(request.form['oda_sayisi'])
            kat = int(request.form['kat'])
            metrekare = int(request.form['metrekare'])
            konum = int(request.form['konum'])

            # Verileri modele uygun formatta düzenle
            new_data = pd.DataFrame({'Oda Sayısı': [oda_sayisi],
                                     'Kat': [kat],
                                     'Metrekare': [metrekare],
                                     'Konum': [konum]})

            # Tahmin yap
            prediction = model.predict(new_data)[0]

            return render_template('result.html', prediction=prediction)

        except:
            return 'Tahmin yapılamadı. Lütfen geçerli bir değer girin.'

if __name__ == '__main__':
    app.run(debug=True)
