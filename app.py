# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 20:51:25 2022

@author: Lahiru
"""
import pyrebase
import streamlit as st
from datetime import datetime
import joblib
import requests
from streamlit_lottie import st_lottie


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottieMain = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fmgfy8rq.json")
lottieSetting = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_qchvuplk.json")
lottieDiab = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_mvdqkcvo.json")

def main():
    # Configuration Key
    
    firebaseConfig = {
        'apiKey': "AIzaSyCn5VQUOW6Q9p5QJLsZVEOTK9Spn13AdxY",
        'authDomain': "test-bf7ae.firebaseapp.com",
        'projectId': "test-bf7ae",
        'databaseURL':"https://test-bf7ae-default-rtdb.firebaseio.com/",
        'storageBucket': "test-bf7ae.appspot.com",
        'messagingSenderId': "756143492496",
        'appId': "1:756143492496:web:0c77d5ab880196f2abb715",
        'measurementId': "G-BKNZRG2QWJ"
      }
    
    # Firebase Authentication
    
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    
    # Database
    
    db = firebase.database()
    storage = firebase.storage()
    
    #side bar logo
    
    st.sidebar.image("logos/Dr BigBot-logos.jpg", width=300)
    
    # Authentication
    
    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign Up'])
    
    email = st.sidebar.text_input('Please input your email')
    password = st.sidebar.text_input('Please enter your password', type = 'password')
    
    # App
    
    # Sign up Block
    
    if choice == 'Sign Up':
        handle = st.sidebar.text_input('Please input your app handle name', value= 'Default')
        submit = st.sidebar.button('Create my account')
        
        if submit:
            user = auth.create_user_with_email_and_password(email, password)
            st.success('Your account is created sucsessfully')
            st.balloons()
            #sign in
            user = auth.sign_in_with_email_and_password(email, password)
            db.child(user['localId']).child("Handle").set(handle)
            db.child(user['localId']).child("ID").set(user['localId'])
            st.title('Welcome ' + handle)
            st.info('login via login drop down selection')
    
    # Login Block
            
    if choice == 'Login':
        login = st.sidebar.checkbox('Login')
        if login:
            user = auth.sign_in_with_email_and_password(email, password)
            st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
            
            bio = st.radio('Jump to', ['Home', 'Recomandation', 'Settings'])
            
            # SETTINGS PAGE 
            if bio == 'Settings':  
                # CHECK FOR IMAGE
                nImage = db.child(user['localId']).child("Image").get().val()  
                
                # IMAGE FOUND     
                if nImage is not None:
                    # We plan to store all our image under the child image
                    Image = db.child(user['localId']).child("Image").get()
                    for img in Image.each():
                        img_choice = img.val()
                        #st.write(img_choice)
                    st.image(img_choice, width=100)
                    
                    exp1 = st.expander('Change profile Image')  
                    # User plan to change profile picture  
                    with exp1:
                        newImgPath = st.text_input('Enter full path of your profile image')
                        upload_new = st.button('Upload')
                        if upload_new:
                            uid = user['localId']
                            fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                            a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
                            db.child(user['localId']).child("Image").push(a_imgdata_url)
                            st.success('Success!')    
                            
                # IF THERE IS NO IMAGE
                else:    
                    st.info("No profile picture yet")
                    newImgPath = st.text_input('Enter full path of your profile image')
                    upload_new = st.button('Upload')
                    if upload_new:
                        uid = user['localId']
                        # Stored Initated Bucket in Firebase
                        fireb_upload = storage.child(uid).put(newImgPath,user['idToken'])
                        # Get the url for easy access
                        a_imgdata_url = storage.child(uid).get_url(fireb_upload['downloadTokens']) 
                        # Put it in our real time database
                        db.child(user['localId']).child("Image").push(a_imgdata_url)             
                   
                exp2 = st.expander('Input/Change Bio details')
                with exp2:   
                        s1=st.selectbox("Sex",("Male","Female"))
                        if s1=="Male":
                            p1=2
                        else:
                            p1=1
                            
                        p2 =st.number_input("Enter Your body temperature")
                        
                        #p3 =st.number_input("Enter Your body puls rate")
                        p3 = st.slider("Enter Your body puls rate",0,200)
                        
                        p4 = st.slider("Enter Your Respiration",0,50)
                        
                        #p5 =st.number_input("Enter Your body systolic blood pressure")
                        p5 = st.slider("Enter Your body systolic blood pressure",0,200)
                        
                        #p6 =st.number_input("Enter Your body diastolic blood pressure")
                        p6 = st.slider("Enter Your body diastolic blood pressure",0,200)
                        
                        p7 =st.number_input("Enter Your body weight (kg)")
                        
                        p8 = st.slider("Enter Your body height (cm)", 1,300)
                      
                        #p9 =st.number_input("Enter Your BMI Value")
                        bmi = (p7/p8**2)*10000
                        p9 = format(bmi, '.2f')
                        st.metric(label="your BMI:", value=p9, delta_color="red")
    
                        
                        p10 = st.slider("Enter Your Age catogory",0,10)
                        
                        s2=st.selectbox("Do you have Myocardial infarction",("Yes","No"))
                        if s2=="Yes":
                            p11=1
                        else:
                            p11=0        
                            
                        save_bio = st.button('Save')
                        
                        #send user static bio to DataBase
                        if save_bio:
                            sex = db.child(user['localId']).child("p1").push(p1)
                            body_temp = db.child(user['localId']).child("p2").push(p2)
                            puls_rate = db.child(user['localId']).child("p3").push(p3)
                            respiration = db.child(user['localId']).child("p4").push(p4)
                            sbp = db.child(user['localId']).child("p5").push(p5)
                            dbp = db.child(user['localId']).child("p6").push(p6)
                            weight = db.child(user['localId']).child("p7").push(p7)
                            height = db.child(user['localId']).child("p8").push(p8)
                            bmi = db.child(user['localId']).child("p9").push(p9)
                            agecat = db.child(user['localId']).child("p10").push(p10)
                            mi = db.child(user['localId']).child("p11").push(p11)
                            
               # st_lottie(lottieSetting, height=300, key= "setting")            
                            
                        
     # HOME PAGE
            elif bio == 'Home':
                
                st_lottie(lottieMain, height=300, key= "main")
                        
                # HF 2 models are run here
                exp1 = st.expander('Heart Failure')  
                 
                with exp1:       
                    
                    st.write("\nPrediction:")
                    #in progress
                    
                    
                    st.write("\nNYHA Severity Type:")
                    # load the model
                    model = joblib.load('model_HF_level')
                    
                    if st.button('Predict'):
                        
                       #calling db user bio data 
                       
                       db_sex = db.child(user['localId']).child("p1").get().val()         
                       if db_sex is not None:
                           val = db.child(user['localId']).child("p1").get()
                           for child_val in val.each():
                               p1_get = child_val.val()   
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
     
                       db_body_temp = db.child(user['localId']).child("p2").get().val()
                       if db_body_temp is not None:
                           val = db.child(user['localId']).child("p2").get()
                           for child_val in val.each():
                               p2_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                       
                       db_puls_rate = db.child(user['localId']).child("p3").get().val()
                       if db_puls_rate is not None:
                           val = db.child(user['localId']).child("p3").get()
                           for child_val in val.each():
                               p3_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                       
                       db_respiration = db.child(user['localId']).child("p4").get().val()
                       if db_respiration is not None:
                           val = db.child(user['localId']).child("p4").get()
                           for child_val in val.each():
                               p4_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                       db_sbp = db.child(user['localId']).child("p5").get().val()
                       if db_sbp is not None:
                           val = db.child(user['localId']).child("p5").get()
                           for child_val in val.each():
                               p5_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                       
                       db_dbp = db.child(user['localId']).child("p6").get().val()
                       if db_dbp is not None:
                           val = db.child(user['localId']).child("p6").get()
                           for child_val in val.each():
                               p6_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                       
                       db_weight = db.child(user['localId']).child("p7").get().val()
                       if db_weight is not None:
                           val = db.child(user['localId']).child("p7").get()
                           for child_val in val.each():
                               p7_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
         
                       db_height = db.child(user['localId']).child("p8").get().val()
                       if  db_height is not None:
                           val = db.child(user['localId']).child("p8").get()
                           for child_val in val.each():
                               p8_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
                         
                       db_bmi = db.child(user['localId']).child("p9").get().val()
                       if  db_bmi is not None:
                           val = db.child(user['localId']).child("p9").get()
                           for child_val in val.each():
                               p9_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
          
                       db_agecat = db.child(user['localId']).child("p10").get().val()
                       if  db_agecat is not None:
                           val = db.child(user['localId']).child("p10").get()
                           for child_val in val.each():
                               p10_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!")
          
                       db_mi = db.child(user['localId']).child("p11").get().val()
                       if  db_mi is not None:
                           val = db.child(user['localId']).child("p11").get()
                           for child_val in val.each():
                               p11_get = child_val.val()
                       else:
                           st.info("No bio data shown yet. Go to setting and provide bio data!") 
                       
                       #run HF type model
                       prediction = model.predict([[p1_get,p2_get,p3_get,p4_get,p5_get,p6_get,p7_get,p8_get,p9_get,p10_get,p11_get]])
                       
                       st.success('HF Type: {} '.format(prediction[0]))
                       
                
                # Diabites 2 models are run here
                exp2 = st.expander('Diabetes Prediction')     
                
                with exp2:                       
                    # load the model
                    st_lottie(lottieDiab, height=300, key= "dia") 
if __name__ == '__main__':
    main()                   
                    