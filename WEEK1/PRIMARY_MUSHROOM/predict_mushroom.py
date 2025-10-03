import pickle
import pandas as pd
import os

# Define the path to the training directory
training_dir = 'training'

# Check if all required files exist in the training directory
required_files = ['le_dict.pkl', 'scaler.pkl', 'pca.pkl', 'rf_model.pkl', 'valid_categories.pkl', 'X_columns.pkl']
missing_files = [file for file in required_files if not os.path.exists(os.path.join(training_dir, file))]
if missing_files:
    print(f"Error: The following required files are missing in the training directory: {', '.join(missing_files)}")
    exit(1)

# Load trained objects
try:
    with open(os.path.join(training_dir, 'le_dict.pkl'), 'rb') as f:
        le_dict = pickle.load(f)
    with open(os.path.join(training_dir, 'scaler.pkl'), 'rb') as f:
        scaler = pickle.load(f)
    with open(os.path.join(training_dir, 'pca.pkl'), 'rb') as f:
        pca = pickle.load(f)
    with open(os.path.join(training_dir, 'rf_model.pkl'), 'rb') as f:
        rf_model = pickle.load(f)
    with open(os.path.join(training_dir, 'valid_categories.pkl'), 'rb') as f:
        valid_categories = pickle.load(f)
    with open(os.path.join(training_dir, 'X_columns.pkl'), 'rb') as f:
        X_columns = pickle.load(f)
except pickle.UnpicklingError as e:
    print(f"Error loading required files: {e}. Ensure the files are valid pickle files.")
    exit(1)
except Exception as e:
    print(f"Unexpected error loading files: {e}")
    exit(1)

# Debugging information
print("All required files loaded successfully from the training directory.")
print(f"Feature columns: {X_columns}")

# Take user input
user_input = {}
for feature, categories in valid_categories.items():
    while True:
        val = input(f"Enter value for {feature} {categories}: ").strip()
        if val in categories:
            user_input[feature] = str(val)
            break
        else:
            print(f"Invalid input for {feature}. Allowed: {categories}. Please re-enter.")

# Prepare input DataFrame
try:
    input_df = pd.DataFrame([user_input])
    for col in X_columns:
        if col not in input_df.columns:
            input_df[col] = str(valid_categories[col][0])
    input_df = input_df[X_columns]
    # Strip whitespace from column names in the input DataFrame
    input_df.columns = input_df.columns.str.strip()
    for col in input_df.columns:
        try:
            input_df[col] = le_dict[col].transform([input_df[col].values[0]])[0]
        except ValueError:
            print(f"Error: Invalid value for '{col}'. Allowed: {list(le_dict[col].classes_)}")
            input_df[col] = le_dict[col].transform([valid_categories[col][0]])[0]
except Exception as e:
    print(f"Error preparing input DataFrame: {e}")
    exit(1)

# Debugging information
print("Input DataFrame prepared successfully.")
print(input_df.head())

# Make prediction
try:
    input_pca = pca.transform(scaler.transform(input_df))
    pred = rf_model.predict(input_pca)[0]
    result = 'edible' if pred == 0 else 'poisonous'
    print(f"\nPrediction: The mushroom is {result.upper()}.")
except Exception as e:
    print(f"Error during prediction: {e}")
    exit(1)
