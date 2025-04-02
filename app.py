from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html file

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
