from estagios import app

@app.route('/')
def homepage():
    return "Home Page"

@app.route('/nova')
def nova():
    return "Nova paggina"