from flask import Flask, render_template, request
import final  # This should have the processing functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textinput']
        output = final.process_input(user_input)  # Make sure this function exists and does what you expect
        return render_template('index.html', user_input=user_input, output=output)
    else:
        return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
