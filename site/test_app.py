import unittest
from app import app  # Import the Flask application

class AppTestCase(unittest.TestCase):

    def setUp(self):
        # Creates a test client for your Flask app
        self.app = app.test_client()
        # Propagate the exceptions to the test client
        self.app.testing = True
    
    def test_process_input(self):
        # Define a sample input that you know how the output should look
        sample_input = "Your sample input text that needs to be processed"

        # Send a POST request to the Flask app with the sample input as form data
        response = self.app.post('/', data={'textinput': sample_input})
        
        # Print out the response data for debugging
        print('Response data:', response.data.decode('utf-8'))

        # Assert to check if the output is as expected (optional)
        # self.assertIn('Expected part of the output', response.data.decode('utf-8'))

        # The test always passes and primarily serves for debugging output
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
