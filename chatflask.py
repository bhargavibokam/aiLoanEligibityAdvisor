import pickle
import numpy as np
import google.generativeai as genai

# Configure your Google GenAI API key here
genai.configure(api_key="AIzaSyCpQTry2c4ABXJXVnb_5C4I57YhA05Y9FQ")

# Load trained model once at module load
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

def preprocess_data(gender, married, dependents, education, employed, credit, area,
                    ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term):

    male = 1 if str(gender).lower() == "male" else 0
    married_yes = 1 if str(married).lower() == "yes" else 0

    dependents_1, dependents_2, dependents_3 = 0, 0, 0
    if dependents == '1':
        dependents_1 = 1
    elif dependents == '2':
        dependents_2 = 1
    elif dependents == "3+":
        dependents_3 = 1

    not_graduate = 1 if str(education).lower() == "not graduate" else 0
    employed_yes = 1 if str(employed).lower() == "yes" else 0
    semiurban = 1 if str(area).lower() == "semiurban" else 0
    urban = 1 if str(area).lower() == "urban" else 0

    # Safe log transform (avoid math domain error)
    ApplicantIncome = float(ApplicantIncome)
    CoapplicantIncome = float(CoapplicantIncome)
    LoanAmount = float(LoanAmount)
    Loan_Amount_Term = float(Loan_Amount_Term)
    credit = float(credit)

    ApplicantIncomelog = np.log(ApplicantIncome) if ApplicantIncome > 0 else 0
    totalincomelog = np.log(ApplicantIncome + CoapplicantIncome) if (ApplicantIncome + CoapplicantIncome) > 0 else 0
    LoanAmountlog = np.log(LoanAmount) if LoanAmount > 0 else 0
    Loan_Amount_Termlog = np.log(Loan_Amount_Term) if Loan_Amount_Term > 0 else 0

    # Credit encoding aligned to form input range 300-850: treat >=750 as good credit
    credit_flag = 1 if 750 <= credit <= 850 else 0

    return [
        credit_flag, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Termlog, totalincomelog,
        male, married_yes, dependents_1, dependents_2, dependents_3,
        not_graduate, employed_yes, semiurban, urban
    ]


def generate_gemini_explanation(user_data, prediction_status):
    prompt = f"""
User Provided Data: {user_data}
Loan Prediction Result: {prediction_status}

Please provide a clear and detailed explanation of why the loan was {prediction_status}. 
If rejected, suggest actionable steps for improving eligibility, focusing on credit score, income, and financial stability.
If approved, provide congratulations and outline next steps in the loan process.
"""
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    chat = model.start_chat()
    response = chat.send_message(prompt)
    return response.text


def chat_response(data):
    """Takes a dictionary of user input and returns a model prediction with explanation."""
    try:
        features = preprocess_data(
            data['gender'], data['married'], data['dependents'], data['education'],
            data['employed'], data['credit'], data['area'], data['ApplicantIncome'],
            data['CoapplicantIncome'], data['LoanAmount'], data['Loan_Amount_Term']
        )
        prediction = model.predict([features])[0]
        status_msg = "Eligible for loan" if prediction == 'Y' else "Not eligible for loan"

        explanation = generate_gemini_explanation(data, status_msg)

        return f" {status_msg}.\n\n{explanation}"
    except Exception as e:
        return f"Error processing data: {str(e)}"
