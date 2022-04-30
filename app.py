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
import base64

# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="SmartCare", page_icon=":elephant:", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#lottieMain = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_fmgfy8rq.json")
lottieMain = load_lottieurl("https://assets2.lottiefiles.com/private_files/lf30_xverp39j.json")
lottieSetting = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_qchvuplk.json")
lottieDiab = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_mvdqkcvo.json")

@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
      background-image: url("data:image/png;base64,%s");
      background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

def main():
    
    set_png_as_page_bg('microsoft-surface-duo-2-2560x1440-windows-11-se-microsoft-4k-23875.png')
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
    
    st.sidebar.title('SmartCare System')
    #st.sidebar.image("logos/Dr BigBot-logos.jpg", width=300)
    
    st_lottie(lottieMain, height=400, key= "main")
    
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
                    
                        #HF Level inputs    
                    
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
                        
                        p7 = st.number_input("Enter Your body weight (kg)")
                        
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
                            
                        #Diabetes Types inputs
                        
                        k1 =st.number_input("Enter Your fasting blood sugar level")
                        
                        k2 =st.number_input("Enter Your bs pp level")
                        
                        k3 =st.number_input("Enter Your Plasma F")
                        
                        k4 =st.number_input("Enter Your HbA1c")
                        
                            
                            
                        save_bio = st.button('Save')
                        
                        #send user static bio to DataBase
                        if save_bio:
                            
                            #sending HF Type user data to DB
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
                            
                            
                            #sending Diabetes types user data to DB
                            
                            bs_fast = db.child(user['localId']).child("k1").push(p1)
                            bs_pp = db.child(user['localId']).child("k2").push(p1)
                            plasmaf = db.child(user['localId']).child("k3").push(p1)
                            hba1c = db.child(user['localId']).child("k4").push(p1)
                            
                            
               # st_lottie(lottieSetting, height=300, key= "setting")            
                            
                        
     # HOME PAGE
            elif bio == 'Home':
                
                #st_lottie(lottieMain, height=400, key= "main")
                
                with st.container():
                    
                    st.write("---")
                    left_column, right_column = st.columns(2)
                    
                    with left_column:
                        
                        st.header("Heart Failure")
                        
                        st.subheader("\nProbability of having Heart Failure:")
                        
                        #in progress
                        # load the model
                        model1 = joblib.load('model_HF_level')
                        
                        if st.button('Predict', key = "5ed028cf-f86c-4aae-a5b2-5b5c365aeb13"):
                            
                           #calling db user bio data 
                           
                           db_bs_fast = db.child(user['localId']).child("k1").get().val()         
                           if db_bs_fast is not None:
                               val = db.child(user['localId']).child("k1").get()
                               for child_val in val.each():
                                   k1_get = child_val.val()   
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
         
                           db_bs_pp = db.child(user['localId']).child("k2").get().val()
                           if db_bs_pp is not None:
                               val = db.child(user['localId']).child("k2").get()
                               for child_val in val.each():
                                   k2_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_plasmaf = db.child(user['localId']).child("k3").get().val()
                           if db_plasmaf is not None:
                               val = db.child(user['localId']).child("k3").get()
                               for child_val in val.each():
                                   k3_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_hba1c = db.child(user['localId']).child("k4").get().val()
                           if db_hba1c is not None:
                               val = db.child(user['localId']).child("k4").get()
                               for child_val in val.each():
                                   k4_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           #run diabetes type model
                           prediction1 = model1.predict([[k1_get,k2_get,k3_get,k4_get]])
                           
                           st.success('Diabetes Type is: {} '.format(prediction1[0]))
                        
                        st.subheader("\nNYHA Severity Type:")
                        
                        # load the model
                        model2 = joblib.load('model_HF_level')
                        
                        if st.button('Predict', key = "b0c49ce4-be53-4e65-8eaf-9e51ed513462"):
                            
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
                           prediction2 = model2.predict([[p1_get,p2_get,p3_get,p4_get,p5_get,p6_get,p7_get,p8_get,p9_get,p10_get,p11_get]])
                           
                           st.success('HF Type: {} '.format(prediction2[0]))
                        
                        with right_column:
                            
                            
                            
                            st.write("")
                            st.write("")
                            st.write("")
                            st.write("")
                            
                with st.container():
                    
                    st.write("---")
                    left_column, right_column = st.columns(2)
                    
                    with left_column:
                        
                        st.header("Diabetes")
                        
                        st.subheader("\nProbability of having Diabetes:")
                        
                        # load the model
                        model3 = joblib.load('model_HF_level')
                        
                        if st.button('Predict', key = "a5300157-6999-43bf-a34c-0c419a0582ea"):
                            
                           #calling db user bio data 
                           
                           db_bs_fast = db.child(user['localId']).child("k1").get().val()         
                           if db_bs_fast is not None:
                               val = db.child(user['localId']).child("k1").get()
                               for child_val in val.each():
                                   k1_get = child_val.val()   
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
         
                           db_bs_pp = db.child(user['localId']).child("k2").get().val()
                           if db_bs_pp is not None:
                               val = db.child(user['localId']).child("k2").get()
                               for child_val in val.each():
                                   k2_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_plasmaf = db.child(user['localId']).child("k3").get().val()
                           if db_plasmaf is not None:
                               val = db.child(user['localId']).child("k3").get()
                               for child_val in val.each():
                                   k3_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_hba1c = db.child(user['localId']).child("k4").get().val()
                           if db_hba1c is not None:
                               val = db.child(user['localId']).child("k4").get()
                               for child_val in val.each():
                                   k4_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           #run diabetes type model
                           prediction3 = model3.predict([[k1_get,k2_get,k3_get,k4_get]])
                           
                           st.success('Diabetes Type is: {} '.format(prediction3[0]))
                           
                           
                        st.subheader("\nType:")
                        
                        # load the model
                        model4 = joblib.load('model_HF_level')
                        
                        if st.button('Predict', key = "783b046e-7a62-47a7-a64a-c01e8529c03d"):
                            
                           #calling db user bio data 
                           
                           db_bs_fast = db.child(user['localId']).child("k1").get().val()         
                           if db_bs_fast is not None:
                               val = db.child(user['localId']).child("k1").get()
                               for child_val in val.each():
                                   k1_get = child_val.val()   
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
         
                           db_bs_pp = db.child(user['localId']).child("k2").get().val()
                           if db_bs_pp is not None:
                               val = db.child(user['localId']).child("k2").get()
                               for child_val in val.each():
                                   k2_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_plasmaf = db.child(user['localId']).child("k3").get().val()
                           if db_plasmaf is not None:
                               val = db.child(user['localId']).child("k3").get()
                               for child_val in val.each():
                                   k3_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           db_hba1c = db.child(user['localId']).child("k4").get().val()
                           if db_hba1c is not None:
                               val = db.child(user['localId']).child("k4").get()
                               for child_val in val.each():
                                   k4_get = child_val.val()
                           else:
                               st.info("No bio data shown yet. Go to setting and provide bio data!")
                           
                           #run diabetes type model
                           prediction4 = model4.predict([[k1_get,k2_get,k3_get,k4_get]])
                           
                           st.success('Diabetes Type is: {} '.format(prediction4[0]))
                        
                    with right_column:
                        
                        # load the model
                        #st_lottie(lottieMain, height=400, key= "main")
                        st.write("")
                        st.write("")
                        st.write("")
                        st.write("")

if __name__ == '__main__':
    main()                   
                    