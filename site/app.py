from flask import Flask, render_template, request
import final  # Ensure final.py contains the processing functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textinput']
        print(f"Form input: {user_input}")  # Debug print to confirm input received
        try:
            output = final.process_input(user_input)  # Use process_input from final.py
            print(f"Processed output: {output}")  # Debug print to confirm processing
        except Exception as e:
            output = f"An error occurred: {e}"
            print(e)  # Log to console for debugging
        return render_template('index.html', user_input=user_input, output=output)
    else:
        return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
