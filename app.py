import os
import numpy as np
import flask
import pickle
from flask import Flask, redirect, url_for, request, render_template


# creating instance of the class
app = Flask(__name__, template_folder='templates')

# to tell flask what url should trigger the function index()


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html')


# prediction function
# Memprediksi input dari form user
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 2)
    loaded_model = pickle.load(
        open("./model/model.pkl", "rb"))  # load the model
    # predict the values using loded model
    result = loaded_model.predict(to_predict)
    return result


@app.route('/result', methods=['POST'])
def result():
    if request.method == 'POST':
        name = request.form['name']
        attack_score = request.form['attack_score']
        defend_score = request.form['defend_score']

        to_predict_list = list(map(int, [attack_score, defend_score]))
        result = ValuePredictor(to_predict_list)

        if int(result) == 0:
            prediction = 'Anda Menemukan Pokemon Tipe Bertahan'
        elif int(result) == 1:
            prediction = 'Anda Menemukan Pokemon Tipe Penyerang'
        elif int(result) == 2:
            prediction = 'Anda Menemukan Pokemon Sampah'
        elif int(result) == 3:
            prediction = 'Anda Menemukan Pokemon Yang Kuat'
        elif int(result) == 4:
            prediction = 'Anda Menemukan Pokemon yang Normal'

        return render_template("result.html", prediction=prediction, name=name)


if __name__ == "__main__":
    app.run(debug=False)  # use debug = False for jupyter notebook
