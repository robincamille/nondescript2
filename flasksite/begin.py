from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello(name='Robin'):
    name = name.lower()
    return render_template('hello.html', name=name)

@app.route('/features', methods = ['POST'])
def features():
    text = "Amazing grace how sweet the sound"
    textlength = len(text)
    return render_template('features.html', name = textlength, msg = text)


@app.route('/textr', methods = ['GET', 'POST'])
def my_form():
    return render_template("my-form.html")

@app.route('/textr', methods = ['POST'])
def my_form_post():

    text = request.form['text']
    processed_text = text.upper()
    return processed_text


if __name__ == '__main__':
    app.debug = True
    app.run()
