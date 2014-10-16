from flask import Flask, render_template,url_for,redirect, request
from flask.ext.mongoengine import MongoEngine
app = Flask(__name__)
app.jinja_env.autoescape = False
app.debug = True

# app.config.from_pyfile('the-config.cfg')

import cPickle as pickle

# load models
cv = pickle.load( open( "models//cv.pkl", "rb" )) # vectorizer
nb = pickle.load( open( "models//nb.pkl", "rb" )) # naive bayes
#tree = pickle.load( open( "models//tree.pkl", "rb" ))

@app.route('/')
def root():
	return redirect(url_for('help'))

@app.route('/index/')
def index():
   	content = render_template("hack.html")
   	return render_template("skeleton.html",content=content, type="index")

@app.route('/help/')
def help():
   	content = render_template("help.html")
   	return render_template("skeleton.html",content=content, type="help")

import numpy as np

@app.route('/result/', methods=["POST", "GET"])
def result():
  crazy=False
  form = request.form
  if request.method == 'POST':
    if "hackathon formula" in form["hack_description"].lower():
      crazy = True

    # words only matter
    def replacePunctuation(line):
            line = line.decode("ascii")
            for ch in line:
                    if ch in "~@#$%^&*()_-+=~<>?/,.;:!{}[]|'\"":
                            line = line.replace(ch, " ")
            return line

    vector = cv.transform(np.array([replacePunctuation(form["hack_description"].lower())]))


    success_predictoin=nb.predict(vector)[0]
    probs = dict(zip(nb.classes_, nb.predict_proba(vector)[0]))

    #probs_2 = dict(zip(tree.classes_, tree.predict_proba(vector.todense())[0]))

    print probs[True]
    content = render_template("result.html",success_prob=float(probs[True])*100,success_pred=success_predictoin, hack_name=form["hack_name"], crazy=crazy)
    return render_template("skeleton.html",content=content, type="index")

@app.route('/animation/')
def animation():
   	return render_template("animation.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
