from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello! 👋 This is my Flask demo app.</h1><p>Deployed on Render.</p>"

@app.route("/about")
def about():
    return "<h2>About</h2><p>This is a sample route you can edit.</p>"

if __name__ == "__main__":
    app.run(debug=True)
