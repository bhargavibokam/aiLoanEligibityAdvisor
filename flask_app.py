from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import pickle
import numpy as np
from chatflask import chat_response  # Import Gemini chatbot logic


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key
# Load your trained ML model
model = pickle.load(open("C:/Users/srava/OneDrive/Desktop/Projects/aiLoanEligibityAdvisor/model.pkl", 'rb'))

USERS = {
    "user@example.com": "password123"  # You can replace with real DB logic later
}
@app.context_processor
def inject_first_name():
    user_email = session.get('user')
    first_name = user_email.split('@')[0] if user_email else None
    return dict(first_name=first_name)


@app.route('/')
def home():
    user_email = session.get('user')
    if user_email:
        first_name = user_email.split('@')[0]  # Extract first part before '@'
    else:
        first_name = None
    return render_template('index.html', first_name=first_name)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/chatbot_response', methods=['POST'])
def chatbot_api():
    try:
        answers = request.get_json()
        bot_reply = chat_response(answers)
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Error in chatbot_api: {e}")
        return jsonify({"reply": "Error processing your request."})

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
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

        credit_flag = 1 if 800 <= credit <= 1000 else 0

        features = [credit_flag, ApplicantIncomeLog, LoanAmountLog, Loan_Amount_Termlog, totalincomelog,
                    male, married_yes, dependents_1, dependents_2, dependents_3,
                    not_graduate, employed_yes, semiurban, urban]

        try:
            prediction = model.predict([features])[0]
            prediction_label = "Approved" if prediction == "Y" else "Rejected"
            return render_template('prediction.html', prediction_text=f"Loan Status: {prediction_label}")
        except Exception as e:
            print(f"Prediction error: {e}")
            return render_template('prediction.html', prediction_text="Error occurred during prediction. Please try again.")

    return render_template('prediction.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        if email in USERS and USERS[email] == password:
            session['user'] = email
            return redirect(url_for('home'))
        else:
            error = "Invalid email or password."
    return render_template('login.html', error=error)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not email or not password or not confirm_password:
            error = "All fields are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif email in USERS:
            error = "User already exists."
        else:
            USERS[email] = password  # Add user (replace with DB logic)
            success = "Signup successful! Please login."
            # You can redirect to login page here if preferred:
            # return redirect(url_for('login'))

    return render_template('signup.html', error=error, success=success)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
