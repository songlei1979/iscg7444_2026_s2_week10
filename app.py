import json

from flask import Flask

# Initialize the Flask application
app = Flask(__name__)

# Define the route for the home page
@app.route("/")
def home():
    return json.dumps({})

@app.route("/test")
def test_api():
    return json.dumps({"message": "success"})

# Run the app locally if this file is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")