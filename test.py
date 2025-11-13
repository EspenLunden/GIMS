import flask as fl
import json
import os

app = fl.Flask(__name__)
app.secret_key = "dev-secret-key"  # needed for session management
userClasses = {}
classPath = "user_classes.json"

name = "TEMP_USER"

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

@app.route('/', methods=['GET', 'POST'])
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
                userClasses[className] = {"fields": []}
                
                # Parse dynamic fields from form data
                # Fields are named as fields[0][name], fields[0][type], fields[1][name], etc.
                field_indices = set()
                for key in fl.request.form:
                    if key.startswith("fields["):
                        # Extract the index from keys like "fields[0][name]"
                        index_str = key.split("[")[1].split("]")[0]
                        field_indices.add(int(index_str))
                
                # Build fields array in order
                for i in sorted(field_indices):
                    field_name_key = f"fields[{i}][name]"
                    field_type_key = f"fields[{i}][type]"

                    # Add default ID field
                    field = {
                            "name": "ID",
                            "type": "number"
                        }
                    userClasses[className]["fields"].append(field)
                    
                    # Add user-defined fields
                    if field_name_key in fl.request.form and field_type_key in fl.request.form:
                        field = {
                            "name": fl.request.form.get(field_name_key),
                            "type": fl.request.form.get(field_type_key)
                        }
                        userClasses[className]["fields"].append(field)
                    
                json.dump(userClasses, file, indent=4)
                print(f"Successfully created class '{className}' with {len(userClasses[className]['fields'])} fields")
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