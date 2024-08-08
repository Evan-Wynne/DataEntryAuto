from flask import Flask, request, jsonify  # Import necessary modules
import subprocess  # Import subprocess module for running external commands
import os  # Import os module for file operations

app = Flask(__name__)  # Create a Flask application

@app.route('/run', methods=['POST'])  # Define a route for POST requests to '/run'
def run_code():
    data = request.get_json()
    code = data['code']
    
    # Path to the final.py file
    script_path = 'final.py'
    
    # Write the input code to final.py
    with open(script_path, 'w') as file:
        file.write(code)
    
    try:
        # Run the Python code using subprocess
        result = subprocess.run(['python', script_path], capture_output=True, text=True, check=True)
        output = result.stdout
    except subprocess.CalledProcessError as e:
        output = e.stderr
    
    return jsonify({ 'output': output })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Run the Flask application

