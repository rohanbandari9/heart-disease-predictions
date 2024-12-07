import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Step 1: Fetch Dataset from API
def fetch_dataset():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
    columns = [
        "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
        "thalach", "exang", "oldpeak", "slope", "ca", "thal", "target"
    ]
    df = pd.read_csv(url, header=None, names=columns, na_values="?")
    return df

# Step 2: Preprocess the Data
def preprocess_data(df):
    # Drop rows with missing values
    df.dropna(inplace=True)

    # Separate features and target
    X = df.drop("target", axis=1)
    y = df["target"]

    # Convert target into binary classification
    y = y.apply(lambda x: 1 if x > 0 else 0)  # 1 for heart disease, 0 otherwise

    return train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Train Models
def train_models():
    # Fetch and preprocess the dataset
    df = fetch_dataset()
    X_train, X_test, y_train, y_test = preprocess_data(df)

    # Ensure the models directory exists
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    os.makedirs(MODELS_DIR, exist_ok=True)

    # Train KNN Model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train, y_train)
    knn_preds = knn.predict(X_test)
    knn_acc = accuracy_score(y_test, knn_preds)
    print(f"KNN Accuracy: {knn_acc * 100:.2f}%")

    # Save KNN model
    with open(os.path.join(MODELS_DIR, "knn_model.pkl"), "wb") as f:
        pickle.dump(knn, f)

    # Train Random Forest Model
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_preds)
    print(f"Random Forest Accuracy: {rf_acc * 100:.2f}%")

    # Save Random Forest model
    with open(os.path.join(MODELS_DIR, "random_forest_model.pkl"), "wb") as f:
        pickle.dump(rf, f)

# Step 4: Main Function
if __name__ == "__main__":
    train_models()
