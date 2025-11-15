from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
from chatflask import chat_response  # Import Gemini chatbot logic

app = Flask(__name__)

# Load trained ML model
model = pickle.load(open("C:/Users/srava/OneDrive/Desktop/Projects/aiLoanEligibityAdvisor/model.pkl", 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

# Corrected chatbot POST endpoint URL to match frontend fetch
@app.route('/chatbot_response', methods=['POST'])
def chatbot_api():
    try:
        answers = request.get_json()
        # Assuming chat_response can handle the answers dictionary appropriately
        bot_reply = chat_response(answers)
        return jsonify({"reply": bot_reply})
    except Exception as e:
        # Log error for debugging
        print(f"Error in chatbot_api: {e}")
        return jsonify({"reply": "Error processing your request."})

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get form inputs exactly as strings/numbers from form
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # Preprocessing same as streamlit with safe log and binary credit flag
        male = 1 if gender == "Male" else 0
        married_yes = 1 if married == "Yes" else 0
        dependents_1 = 1 if dependents == '1' else 0
        dependents_2 = 1 if dependents == '2' else 0
        dependents_3 = 1 if dependents == '3+' else 0
        not_graduate = 1 if education == "Not Graduate" else 0
        employed_yes = 1 if employed == "Yes" else 0
        semiurban = 1 if area == "Semiurban" else 0
        urban = 1 if area == "Urban" else 0

        ApplicantIncomeLog = np.log(ApplicantIncome) if ApplicantIncome > 0 else 0
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome) if (ApplicantIncome + CoapplicantIncome) > 0 else 0
        LoanAmountLog = np.log(LoanAmount) if LoanAmount > 0 else 0
        Loan_Amount_Termlog = np.log(Loan_Amount_Term) if Loan_Amount_Term > 0 else 0

        credit_flag = 1 if 800 <= credit <= 1000 else 0  # Keep same threshold as Streamlit

        features = [credit_flag, ApplicantIncomeLog, LoanAmountLog, Loan_Amount_Termlog, totalincomelog,
                    male, married_yes, dependents_1, dependents_2, dependents_3,
                    not_graduate, employed_yes, semiurban, urban]

        try:
            prediction = model.predict([features])[0]
            prediction_label = "Approved" if prediction == "Y" else "Rejected"
            return render_template('prediction.html', prediction_text=f"Loan Status: {prediction_label}")
        except Exception as e:
            # Log error but don’t crash; show friendly error page or message
            print(f"Prediction error: {e}")
            return render_template('prediction.html', prediction_text="Error occurred during prediction. Please try again.")

    return render_template('prediction.html')



if __name__ == "__main__":
    app.run(debug=True)
