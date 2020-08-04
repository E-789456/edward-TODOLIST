from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify

)
import requests
from base64 import *
from io import BytesIO
from pprint import pprint


class User:
    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='tsatsu', email='edwardakorlie73@gmail.com', password='sensitive'))
users.append(User(id=2, username='Becca', email='040917125@live.gtuc.edu.gh' , password='secret'))
users.append(User(id=3, username='Carlos', email='edtsatsu@gmail.com' , password='bace'))


app = Flask(__name__)
app.secret_key = 'tsatsu'


@app.route('/')
def index():
    return redirect('/login')
    
@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        return redirect(url_for('login'))

    return render_template('login.html')

def get_base64(files):
    if len(files) > 0:
        b64file = b64encode(files['image'].read()).decode("utf-8")
        return b64file
    return ""



@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method =="POST":
        api_key = 'T_72876c28-a773-4ac8-b650-4b0d27a6489b'
        headers = {'x-authorization': 'Basic edwardakorlie73@gmail.com:{api_key}'.format(api_key= api_key),'Content-Type': 'application/json'}
        data = request.form
        print(data)
        print(request.files)
        b64file = get_base64(request.files)
        payload = {"gallery":"project_1db","identifier":data["email"],"image":b64file}
        print(headers)
        r = requests.post('https://api.bacegroup.com/v2/enroll', headers=headers, data=payload)
    
        print(r.text) 
       # print(r.json)

    return render_template("signup.html")



@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')



if __name__ == "__main__":
    app.debug =True
    app.run()