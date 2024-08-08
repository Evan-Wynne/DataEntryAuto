from flask import Flask, render_template, request
import final  # Ensure final.py contains the process_input function

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['textinput']
        # Call a processing function from final.py
        output = final.process_input(user_input)  # This function should process the input
        return render_template('index.html', user_input=user_input, output=output)
    return render_template('index.html', output=None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)


''''''