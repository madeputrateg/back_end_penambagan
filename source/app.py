from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import user,model_feature, model,feedback, session, feedback_input_target
from database.db import db
from werkzeug.utils import secure_filename
from helper import modelSwapper,util
from repository.feedback import feedbackRepository
from repository.model import modelRepository
from repository.feedback_input_target import APIrepoFeedbackTarget
from repository.user import APIrepouser
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
ALLOWED_EXTENSIONS = {'py','pkl','txt'}

# --- POSTGRES CONNECTION ---
# Replace 'user', 'password', and 'my_auth_db' with your actual Postgres credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/my_auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#file_upload_path
app.config["UPLOAD_FOLDER"] = "E:\\tugas_uas_penambangan_data\\source\\upload"
db.init_app(app)
with app.app_context():
    try:
        db.create_all()
        print("Database tables initialized successfully!")
    except Exception as e:
        print(f"Error creating database: {e}")
SWAPPER = modelSwapper.modelSwapper(save_route=app.config["UPLOAD_FOLDER"])



login_manager = LoginManager(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return user.Userauth.query.get(int(user_id))

# --- ROUTES ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_pw = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        new_user = user.Userauth(username=request.form['username'], password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return '''<form method="post">User: <input name="username"><br>Pass: <input name="password" type="password"><br><button>Reg</button></form>'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        current_user = user.Userauth.query.filter_by(username=request.form['username']).first()
        if current_user and check_password_hash(current_user.password, request.form['password']):
            login_user(current_user)
            return redirect(url_for('dashboardV2'))
        flash('Invalid credentials')
    return '''<form method="post">User: <input name="username"><br>Pass: <input name="password" type="password"><br><button>Login</button></form>'''

@app.route('/dashboard')
@login_required
def dashboard():
    feedbacks = list(map(lambda x: x.to_dict(),feedbackRepository.get_all_feedback()))
    return render_template(template_name_or_list="uploadModels.jinja",feedbacksResult = feedbacks)

# --- AUTHORIZATION EXAMPLE ---


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('checkHeart'))

@app.route('/upload',methods=['GET','POST'])
@login_required
def upload_model():
    # feedbacks = list(map(lambda x: x.to_dict(),feedbackRepository.get_all_feedback()))
    if request.method == 'POST':
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        print(request.files)
        python_file = request.files['python']
        pickle_file = request.files['pickle']
        class_name = request.form["class"]

        input_name = request.form.getlist('input_name[]')
        data_type = request.form.getlist('data_type[]')
        features = []
        for i in zip(input_name,data_type):
            features.append(i)
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        if not (python_file and allowed_file(python_file.filename)):
            return "error file not accepted"
        if not (pickle_file and allowed_file(python_file.filename)):
            return "error file not accepted"

        err = SWAPPER.initializedModel(class_name,features,pickle_file,python_file)
        if err!="success":
            print(err)
        
            
    return redirect(url_for("dashboardV2"))

@app.route('/checkheart',methods=['GET','POST'])
def checkHeart():
    all_model = SWAPPER.getAllModelAndFeature()
    if request.method == "POST":
        jsonData = request.get_json()
        model = SWAPPER.getLoadedModel(jsonData["model"])
        result = model.predict(jsonData)
        jsonData["pred_target"] = result
        # feedbackRepository.insert_feedback_json(jsonData)
        return jsonify({"result":result})
    return render_template("getprediction.jinja",all_model = all_model)

@app.route("/feedback",methods = ["POST"])
def postFeedback():
    if request.method == "POST":
        jsonData = request.get_json()
        keys = SWAPPER.getModelKeys()
        if not (jsonData["model"] in keys):
            print("model not found")
            return 
        
        model = SWAPPER.getModel(jsonData["model"])
        modelloaded = SWAPPER.getLoadedModel(jsonData["model"])
        print(jsonData)
        filtered_feedback = util.filter_features_by_type(jsonData,model.features)
        target = jsonData["target"]
        pred_target = jsonData["pred_target"]
        input_target = APIrepoFeedbackTarget.insertFeedback_target(target=str(target),pred_target=str(pred_target),model_id=model.model_id)
        feedbackRepository.insert_feedback_json_serial(filtered_feedback,modelloaded.map_features_id,input_target.id)
        return jsonify({"result":"success"})

@app.route("/dashboardv2",methods = ["POST","GET"])
@login_required
def dashboardV2():
    if request.method == "POST":
        pass
    users = APIrepouser.getAllUserDict()
    modelAPI = modelRepository()
    feedbacks = modelAPI.get_all_model_feature_and_feedback()
    return render_template("admin.jinja",feedbacks = feedbacks,users ={"result": users})

@app.route("/adduser",methods = ["POST","GET"])
def adduser():
    jsondata = request.get_json()
    hashed_pw = generate_password_hash(jsondata['password'], method='pbkdf2:sha256')
    new_user = user.Userauth(username=jsondata['username'], password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict())

@app.route("/verifyfeed",methods=["UPDATE"])
def verifyFeedback():
    jsondata = request.get_json()
    APIrepoFeedbackTarget.update_feedback_validation(jsondata["input_id"])
    return jsonify({"result":"success"})

# @app.route('/checkstats',methods=['GET','POST'])
# def checkstats():
#     if request.method == "POST":
#         jsonData = request.get_json()
#         model = SWAPPER.getLoadedModel(jsonData["model"])
#         result = model.predict(jsonData)
#         jsonData["pred_target"] = result
#         # feedbackRepository.insert_feedback_json(jsonData)
#         return jsonify({"result":result})
#     # obj = {}
#     # keys = SWAPPER.getModelKeys()
#     # for key in keys:
#     #     modelAbs = SWAPPER.getModel(key)
#     #     features = list(map(lambda x : {"name":x[0],"type":x[1]},modelAbs.features))
#     #     obj[key] = {
#     #        "features" : features
#     #     }
#     return render_template(template_name_or_list = "tempoaryPred.jinja",features=obj,objstring=json.dumps(obj))


if __name__ == '__main__':

    
    with app.app_context(): 
        SWAPPER.loadSavedModel()
        try:
            # db.drop_all()
            db.create_all()
            print("Database tables initialized successfully!")
        except Exception as e:
            print(f"Error creating database: {e}")
    app.run(debug=True)