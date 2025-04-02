from flask import Flask, render_template

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
