from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load("E://Github Projects//OrganTransplantation//MachineLearningModel//organ_transplantation_model_final.pkl")

# Load donor dataset
donors = pd.read_csv('E://Github Projects//OrganTransplantation//Datasets//donors.csv')

def recommend_best_donor(recipient_data):
    """
    Recommend the best donor based on recipient data.
    """
    recipient_df = pd.DataFrame([recipient_data])  # Convert recipient data to DataFrame
    donors_copy = donors.copy()
    
    # Repeat recipient details for all donors
    recipients_repeated = pd.DataFrame([recipient_data] * len(donors_copy))
    combined = pd.concat([recipients_repeated.reset_index(drop=True), donors_copy.reset_index(drop=True)], axis=1)
    
    # Get model predictions
    compatibility_scores = model.predict(combined)
    
    # Add compatibility scores to donors list
    donors_copy['Compatibility_Score'] = compatibility_scores
    best_donor = donors_copy.loc[donors_copy['Compatibility_Score'].idxmax()]
    
    return best_donor.to_dict()

@app.route("/predict", methods=["POST"])
def predict():
    recipient_data = request.json  # Get recipient data from request
    best_match = recommend_best_donor(recipient_data)  # Find best donor
    return jsonify(best_match)  # Return as JSON response

if __name__ == "__main__":
    app.run(debug=True)
