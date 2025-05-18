import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("large_product_sales_500k.csv")
    df.dropna(inplace=True)
    return df

# Train model
def train_model(df):
    X = df[['ProductType', 'MarketingStrategy', 'InteractionType', 'QuantitySold']]
    y = df['Converted'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Encode categorical features
    encoders = {}
    for col in ['ProductType', 'MarketingStrategy', 'InteractionType']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        encoders[col] = le

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    acc = accuracy_score(y_test, model.predict(X_test))
    return model, encoders, acc

# Predict conversion
def predict_conversion(model, encoders, input_data):
    df_input = pd.DataFrame([input_data])
    for col in ['ProductType', 'MarketingStrategy', 'InteractionType']:
        df_input[col] = encoders[col].transform(df_input[col])
    prediction = model.predict(df_input)[0]
    return 'Yes' if prediction == 1 else 'No'

# Streamlit app
def main():
    st.subheader("🎯 AI Model: Predict Conversion")

    df = load_data()
    model, encoders, accuracy = train_model(df)
    st.success(f"Model trained with accuracy: {accuracy:.2f}")

    with st.form("prediction_form"):
        st.markdown("**Enter Details for Prediction**")
        product_type = st.selectbox("Product Type", df['ProductType'].unique())
        marketing_strategy = st.selectbox("Marketing Strategy", df['MarketingStrategy'].unique())
        interaction_type = st.selectbox("Interaction Type", df['InteractionType'].unique())
        quantity_sold = st.number_input("Quantity Sold", min_value=0, step=1)
        
        submit = st.form_submit_button("Predict")

    if submit:
        input_data = {
            "ProductType": product_type,
            "MarketingStrategy": marketing_strategy,
            "InteractionType": interaction_type,
            "QuantitySold": quantity_sold
        }
        result = predict_conversion(model, encoders, input_data)
        st.success(f"Predicted Conversion: **{result}**")

if __name__ == "__main__":
    main()
