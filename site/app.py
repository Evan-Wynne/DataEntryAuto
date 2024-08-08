from flask import Flask, render_template, request
from process import process_input  # Ensure this import works

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    user_input = None
    output = None
    if request.method == 'POST':
        user_input = request.form['textinput']
        print("Received input:", user_input)  # Debug statement to check input

        # Try to process the input and catch potential errors
        try:
            output = process_input(user_input)
            print("Processed output:", output)  # Debug statement to check output
        except Exception as e:
            output = f"Error processing input: {str(e)}"
            print(output)  # Log the error

    return render_template('index.html', user_input=user_input, output=output)

if __name__ == '__main__':
    app.run(debug=True)
