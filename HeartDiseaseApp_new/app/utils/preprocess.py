def preprocess_data(data):
    # Normalize features for prediction models
    return [
        data["age"] / 100,
        data["cholesterol"] / 300,
        data["blood_pressure"] / 200
    ]
