from flask import Flask, render_template, request
from process import process_input

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    output = None
    if request.method == 'POST':
        user_input = request.form['textinput']
        print("Received input in Flask app:", user_input[:500])  # Debug print for received input
        try:
            output = process_input(user_input)
            print("Processed output in Flask app:", output)  # Debug print for processed output
        except Exception as e:
            print(f"Error during processing: {e}")
            output = f"Error during processing: {e}"
    return render_template('index.html', user_input=user_input, output=output)


@app.route('/other')
def test():
    return render_template('other.html')


if __name__ == '__main__':
    app.run(debug=True)
