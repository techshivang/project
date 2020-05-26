from flask import Flask,render_template,url_for,flash,redirect,jsonify,request,session
from flask_sqlalchemy import SQLAlchemy
import os
import numpy as np 
import math 
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

db_path=os.path.join(os.path.dirname(__file__))
db_uri='sqlite:///'+os.path.join(db_path,'dbfile.sqlite')


app=Flask(__name__)
model=pickle.load(open('taxi.pkl','rb'))
model1 = pickle.load(open('breast.pkl', 'rb'))
model2=pickle.load(open('student_pickle','rb'))
model3=pickle.load(open('house.pkl','rb'))

app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI']=db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80))
    email=db.Column(db.String(80))
    password=db.Column(db.String(80))
    confirm_password=db.Column(db.String(80))
    mobile_number=db.Column(db.String(10))
    country=db.Column(db.String(80))

db.create_all()

@app.route('/')
def homes():
    return render_template('home.html')


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/add',methods=['GET','POST'])
def add():
    if request.method=='POST':
        name=request.form.get('user')
        email=request.form.get('email')
        password=request.form.get('pass')
        confirm_password=request.form.get('conpass')
        mobile_number=request.form.get('mobile')
        country=request.form.get('country')
        
        user = User.query.filter_by(name=name).first()
        if user:
            return render_template('sign.html')
        else:
            entry=User(name=name,email=email,password=password,confirm_password=confirm_password,mobile_number=mobile_number,country=country)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('start'))

    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/log', methods=['GET','POST'])
def log():
    if request.method=='POST':             
        name = request.form.get('user')
        password = request.form.get('pass')
        user_name=User.query.filter_by(name=name).first()
        user_found=User.query.filter_by(password=password).first()
        if (user_found) and (user_name):
            return redirect(url_for('start'))
        else:
            if user_name:
                return render_template('log.html')
            else:
                return render_template('false.html')
    return render_template('login.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/check',methods=['GET','POST'])
def check():
    if request.method=='POST':
        email=request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('forgot'))
        else:
            return render_template('false.html')
    return render_template('update.html')


@app.route('/forgot')
def forgot():
    return render_template('forgot_password.html')

@app.route('/reset',methods=['GET','POST'])
def reset():
    if request.method=='POST':
        name=request.form.get('user')
        password = request.form.get('pass')
        confirm_password=request.form.get('conpass')

        user_found=User.query.filter_by(name=name).first()
        user_id=user_found.id
        user_information=User.query.get(user_id)

        if user_found:
            user_information.password=password
            user_information.confirm_password=confirm_password
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('false.html')
    return render_template('forgot_password.html')
        

    

    #     user_found=User.query.filter_by(name=name).first()
    #     if user_found:
    #         entry=User()
    #         db.session.add(entry)
    #         db.session.commit()
    #         return redirect(url_for('login'))
    #     else:
    #         return render_template('log.html')
    # return render_template('forgot.html')


        

    #     password = request.form.get('pass')
    #     confirm_password=request.form.get('conpass')

    #     user_pass=User.query.filter_by(password=password).first()
    #     user_con_pass=User.query.filter_by(confirm_password=confirm_password).first()

    #     entry=User(password=password,confirm_password=confirm_password)
    #     db.session.add(entry)
    #     db.session.commit()
    #     return redirect(url_for('login'))
    # return render_template('forgot_password.html')




@app.route('/view')
def view():
    users=User.query.all()
    return render_template('view.html',users=users)

@app.route('/start')
def start():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('aboutus.html')

@app.route('/home')
def home():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    int_features  = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    output = round(prediction[0],2)
    return render_template('index1.html',prediction_text="Number of Weekly Rides Should be {}".format(math.floor(output)))

@app.route('/health')
def health():
    return render_template('index2.html')

@app.route('/predict1',methods=['POST'])
def predict1():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    
    features_name = ['mean radius', 'mean texture', 'mean perimeter', 'mean area',
       'mean smoothness', 'mean compactness', 'mean concavity',
       'mean concave points', 'mean symmetry', 'mean fractal dimension',
       'radius error', 'texture error', 'perimeter error', 'area error',
       'smoothness error', 'compactness error', 'concavity error',
       'concave points error', 'symmetry error', 'fractal dimension error',
       'worst radius', 'worst texture', 'worst perimeter', 'worst area',
       'worst smoothness', 'worst compactness', 'worst concavity',
       'worst concave points', 'worst symmetry', 'worst fractal dimension']
    
    df = pd.DataFrame(features_value, columns=features_name)
    output = model1.predict(df)
        
    if output == 0:
        res_val = "** breast cancer **"
    else:
        res_val = "no breast cancer"
        

    return render_template('index2.html', prediction_text1='Patient has {}'.format(res_val)) 

@app.route('/corona')
def hello_world():
    return render_template('index3.html')

@app.route('/predict2', methods=['POST'])
def predict2():
    
    if request.method =='POST':
        
        #pickle_in = open("corona.pkl","rb")
        
        #
        
        age = request.form['age']
        fever = request.form['fever']
        breath = request.form['breath']
        cold = request.form['cold']
        body = request.form['body']
       

        #print('#-------------------------------data is here-------------------------------------#')
        #print(age,body,fever,cold,breath)
        
        clf = pickle.load(open("corona.pkl", "rb"))
        #columns  -- Age,	Fever,	BodyPains,	RunnyNose,	Difficulty_in_Breath
        data = [[int(age),int(fever),int(body),int(cold),int(breath)]]
        predict = clf.predict(data)[0]
        proba_score = clf.predict_proba([[60,100,0,1,0]])[0][0]
        
        if predict==1:
            prediction='Positive'
        else:
            prediction = 'Negative'
        
        return render_template('index3.html',prediction=prediction,proba_score=round(proba_score*100,2))
    else:
        
        return render_template('index3.html',message='Something missed, Please follow the instructions..!')


#model = pickle.load(open('student_pickle','rb'))
# print(model.predict([[15,20,20,20,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,1]]))

@app.route('/students')
def students():
    return render_template('index4.html')

@app.route('/student_performance',methods=['POST'])
def student_performance():
    input_features = [int(x) for x in request.form.values()]
    features_value = [np.array(input_features)]

    output = model2.predict(features_value)

    if output == 0:
        res_val = "** Marks Between 60 to 70% **"
    elif output==1:
        res_val = "** Marks Between 75 to 85% **"
    else:
        res_val="** Marks Between 90 to 98% **"

    
    return render_template('index4.html', prediction_text2='Student has Secure {} in These Particular subjects'.format(res_val))

@app.route('/boston')
def boston():
    return render_template('index5.html')

@app.route('/houseprice', methods=['POST'])
def houseprice():
    int_features  = [float(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model3.predict(final_features)
    output = round(prediction[0],2)
    return render_template('index5.html',prediction_text3="Price of the House for following features Should be {}".format(math.floor(output)))

@app.route('/help')
def help():
    return render_template('help.html')

if __name__=="__main__":
    app.run(debug=True)