import flask as fl

app = fl.Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for session management

name = "TEMP_USER"

@app.route('/', methods=['GET', 'POST'])
def home():
    #posts
    if fl.request.method == 'POST':

        #redirect to logins
        if 'to_login' in fl.request.form:
            return fl.redirect(fl.url_for('login'))
        
        #test
        elif 'other_button' in fl.request.form:
            print("You clicked the other button!")
        
    #template
    return fl.render_template('home.html', person=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #posts
    if fl.request.method == 'POST':
        #login submit
        if 'submit' in fl.request.form:
            username = fl.request.form.get("username")
            password = fl.request.form.get("password")
            
            print(username, password)
            if username:
                fl.session['username'] = username
                return fl.redirect(fl.url_for('dashboard'))
    #template
    return fl.render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    username = fl.session.get('username', 'TEMP_USER')
    return fl.render_template('dashboard.html', person=username)

@app.route('/create_class', methods=['GET', 'POST'])
def createClass():
    #posts
    
    #template
    return fl.render_template('createClass.html')

if __name__ == '__main__':  
   app.run(debug = True)