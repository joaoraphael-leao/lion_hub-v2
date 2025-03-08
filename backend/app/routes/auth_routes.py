from flask import Flask, render_template

app = Flask(__name__, static_folder="static", template_folder="../../../frontend")

@app.route("/carregamento")
def carregamento():
    return render_template("/src/routes/login.svelte")

if __name__ == "__main__":
    app.run(debug=True)