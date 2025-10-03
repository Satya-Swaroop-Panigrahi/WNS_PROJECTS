# Mushroom Classification Project

## Project Background

This project is a Python-based application that classifies mushrooms as either edible or poisonous based on their features. The project demonstrates a complete machine learning workflow, including data preprocessing, model training, evaluation, and deployment. The trained model is used in a separate script to make predictions based on user input.

### Features
- **Data Preprocessing:** Handles missing values, encodes categorical features, and removes outliers.
- **Dimensionality Reduction:** Uses PCA to reduce the feature space for better model performance.
- **Model Training:** Trains multiple models (e.g., Decision Tree, Random Forest, Logistic Regression, SVM) with cross-validation to reduce overfitting.
- **Prediction Script:** A user-friendly script (`predict_mushroom.py`) allows users to input mushroom features and get predictions.

## How to Run the Code

### Prerequisites
- Python 3.x
- Required Python libraries:
  - pandas
  - numpy
  - scikit-learn
  - matplotlib
  - seaborn

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YourUsername/MushroomClassifier.git
   cd MushroomClassifier
   ```

2. **Install Required Packages:**
   Install the required Python libraries using pip:
   ```bash
   pip install pandas numpy scikit-learn matplotlib seaborn
   ```

3. **Prepare the Dataset:**
   Place the dataset file (`Mushroom-Dataset(Data).csv`) in the `data` folder.

4. **Run the Notebook:**
   Open the `mushroom_classifier.ipynb` notebook in Jupyter Notebook or VS Code and run all cells to train the model and save the required `.pkl` files.

5. **Run the Prediction Script:**
   Use the `predict_mushroom.py` script to make predictions:
   ```bash
   python predict_mushroom.py
   ```

## Usage

1. **Train the Model:**
   - Open the notebook and execute all cells to preprocess the data, train the model, and save the necessary files.

2. **Make Predictions:**
   - Run the `predict_mushroom.py` script.
   - Enter the required mushroom features when prompted.
   - The script will output whether the mushroom is edible or poisonous.

## Code Overview

### 1. Notebook (`mushroom_classifier.ipynb`)
- **Data Preprocessing:**
  - Handles missing values and encodes categorical features using `LabelEncoder`.
  - Removes outliers using the IQR method.
- **Dimensionality Reduction:**
  - Uses PCA to reduce the feature space to 5 components.
- **Model Training:**
  - Trains multiple models with cross-validation to evaluate performance.
  - Saves the best model and preprocessing objects as `.pkl` files.

### 2. Prediction Script (`predict_mushroom.py`)
- **Loads Pretrained Objects:**
  - Loads the trained model, `LabelEncoder` objects, scaler, PCA, and valid categories from `.pkl` files.
- **Takes User Input:**
  - Prompts the user to enter mushroom features.
- **Makes Predictions:**
  - Preprocesses the input, applies PCA, and uses the trained model to predict whether the mushroom is edible or poisonous.

## Example Workflow

1. **Train the Model:**
   - Run the notebook to preprocess the data, train the model, and save the `.pkl` files.

2. **Make Predictions:**
   - Run the `predict_mushroom.py` script.
   - Example input:
     ```
     Enter value for cap-shape ['b', 'c', 'x', 'f', 'k', 's']: x
     Enter value for cap-surface ['f', 'g', 'y', 's']: y
     ...
     ```
   - Example output:
     ```
     Prediction: The mushroom is POISONOUS.
     ```

## Dataset Description

The dataset used in this project contains information about various mushroom species, including their physical characteristics and whether they are edible or poisonous. Each row in the dataset represents a mushroom, and the columns represent its features.

### Key Features
- **cap-shape, cap-surface, cap-color:** Characteristics of the mushroom cap.
- **bruises?:** Indicates whether the mushroom has bruises.
- **odor:** The smell of the mushroom.
- **gill-attachment, gill-spacing, gill-size, gill-color:** Details about the gills of the mushroom.
- **stalk-shape, stalk-root, stalk-surface, stalk-color:** Information about the stalk of the mushroom.
- **veil-type, veil-color:** Characteristics of the mushroom's veil.
- **ring-number, ring-type:** Details about the ring on the mushroom's stalk.
- **spore-print-color:** The color of the spore print.
- **population:** The population density where the mushroom is found.
- **habitat:** The type of habitat where the mushroom grows.

### Target Variable
- **Type:** The target variable indicates whether the mushroom is edible (`e`) or poisonous (`p`).

### Dataset Insights
- The dataset is entirely categorical, with no missing values.
- Some features have a large number of unique categories, making encoding an essential preprocessing step.
- The dataset is imbalanced, with more edible mushrooms than poisonous ones, requiring careful handling during model training.

### Source
The dataset is publicly available and commonly used for classification tasks in machine learning. It provides an excellent opportunity to practice preprocessing, feature engineering, and model evaluation.

## Project Structure
```
MushroomClassifier/
│
├── data/
│   ├── Mushroom-Dataset(Data).csv
│   ├── Mushroom-Dataset(Description).csv
│
├── training/
│   ├── mushroom_classifier.ipynb
│   ├── le_dict.pkl
│   ├── scaler.pkl
│   ├── pca.pkl
│   ├── rf_model.pkl
│   ├── valid_categories.pkl
│   ├── X_columns.pkl
│
├── predict_mushroom.py
├── README.md
```

## Important Notes
1. **Dataset:** Ensure the dataset is placed in the `data` folder before running the notebook.
2. **Environment:** Use a virtual environment to manage dependencies.
3. **Performance:** The script is optimized for small datasets. For larger datasets, consider using more advanced preprocessing techniques.

## Conclusion
This project provides a complete pipeline for mushroom classification, from data preprocessing to model deployment. It is a valuable tool for demonstrating machine learning workflows and can be extended to other classification tasks.
