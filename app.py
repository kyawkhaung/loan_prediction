from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

model = pickle.load(open('logistic_regression_model.pkl', 'rb'))
                         
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():

    if request.method == 'POST':
        Gender = int(request.form['Gender'])
        Married =int(request.form['Married'])
        Dependents = int(request.form['Dependents'])
        Education = int(request.form['Education'])
        Self_Employed = int(request.form['Self_Employment'])
        Property_Area = int(request.form['Property_Area'])
        Credit_History = int(request.form['Credit_History'])
        Loan_Amount_Term = int(request.form['Loan_amt_term'])
        
        str_loan_amt = str(request.form['loan_amt'])
        if str_loan_amt:
            LoanAmount = float(str_loan_amt)
        else:
            LoanAmount = 0
        
        str_applicant_income = request.form['ApplicantIncome']
        if str_applicant_income:
            ApplicantIncome = float(str_applicant_income)
        else:
            ApplicantIncome = 0
            
        str_co_applicant_income = request.form['CoApplicantIncome']
        if str_co_applicant_income:
            CoapplicantIncome = float(str_co_applicant_income)
        else:
            CoapplicantIncome = 0
                
        #LoanAmount = float(request.form['loan_amt'])
       # LoanAmount = request.form.get('loan_amt', type=float)#500 # float(request.form['loan_amount'])
       # ApplicantIncome = float(request.form['ApplicantIncome'])
       # CoapplicantIncome = float(request.form['CoApplicantIncome'])
        print(LoanAmount)
 
        prediction = model.predict([[Gender, Married, Dependents, Education,Self_Employed, 
                                     ApplicantIncome, CoapplicantIncome, LoanAmount,Loan_Amount_Term, 
                                     Credit_History, Property_Area]])
        output=round(prediction[0],2)
        
        if LoanAmount == 0 or ApplicantIncome == 0:
            return render_template('index.html',prediction_text="Sorry, can't determine your loan request. Enter valid income/loan amount!")
        
        else:
            if output <= 0:
                return render_template('index.html',prediction_text="Sorry you cannot get this loan. Actual predicted value is " + str(output))
            else:
                return render_template('index.html', prediction_text="Congratulation, decisiont to get loan is Approved! Actual predicted value is" + str(output))
           # return render_template('index.html',prediction_text="Decision to get loan is {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

