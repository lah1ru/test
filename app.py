# -*- coding: utf-8 -*-
"""
Created on Sun Dec 26 21:00:34 2021

@author: Lahiru
"""
import streamlit as st
import joblib

def main():
    html_temp = """
    <div style="background-color:lightblue;padding:16px">
    <h2 style="color:black";text-align:center> Dr.BigBot 🐘</h2>
    </div>
    
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    
    # load the model
    model = joblib.load('model_HF_level')
    
    s1=st.selectbox("Sex",("Male","Female"))
    if s1=="Male":
        p1=2
    else:
        p1=1
        
    p2 =st.number_input("Enter Your body temperature")
    
    p3 =st.number_input("Enter Your body puls rate")
    #p3 = st.slider("Enter Your body puls rate",0,200)
    
    #p4 = st.slider("Enter Your Respiration",0,50)
    p4 = st.number_input("Enter Your Respiration")
    
    p5 =st.number_input("Enter Your body systolic blood pressure")
    #p5 = st.slider("Enter Your body systolic blood pressure",0,200)
    
    p6 =st.number_input("Enter Your body diastolic blood pressure")
    #p6 = st.slider("Enter Your body diastolic blood pressure",0,200)
    
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
         
    
    if st.button('Predict'):
       prediction = model.predict([[p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11]])
       
       st.success('HF Type: {} '.format(prediction[0]))   
        
        
if __name__ == '__main__':
    main()
