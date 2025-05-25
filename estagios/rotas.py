from estagios import app

@app.route('/')
def homepage():
    return "Home Page"