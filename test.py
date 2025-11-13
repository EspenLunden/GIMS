import flask as fl
import json
import os

app = fl.Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for session management
userClasses = {}
classPath = "user_classes.json"

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
    # posts
    if fl.request.method == 'POST':
        # create class submit, check if class name already exists
        if 'submit' in fl.request.form and fl.request.form.get("class_name") not in userClasses:
            print("Creating class...")
            print(fl.request.form)

            # write to json
            with open(classPath, 'w') as file:
                className = fl.request.form.get("class_name")
                userClasses[className] = {}
                for key in fl.request.form:
                    if key == "fields[][name]":
                        userClasses[className]["fields"] = []
                        for i in range(len(fl.request.form.getlist(key))):
                            field = {}
                            field["name"] = fl.request.form.getlist(key)[i]
                            field["type"] = fl.request.form.getlist("fields[][type]")[i]
                            userClasses[className]["fields"].append(field)
                    if key != "class_name" and key != "submit":
                        userClasses[className][key] = fl.request.form.get(key)
                json.dump(userClasses, file, indent=4)
        else:
            print("Class name already exists or no name provided.")
    
    #template
    return fl.render_template('create_class.html')

if __name__ == '__main__':
   # load user classes if file exists
    if os.path.exists(classPath) and os.path.getsize(classPath) > 0:
        with open(classPath, 'r') as file:
           userClasses = json.load(file)
    else:
        userClasses = {}

    # run app
    app.run(debug = True)