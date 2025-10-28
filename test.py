import flask as fl

app = fl.Flask(__name__)

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
            
            print(fl.request.form["username"], fl.request.form["password"])
    
    #template
    return fl.render_template('login.html')