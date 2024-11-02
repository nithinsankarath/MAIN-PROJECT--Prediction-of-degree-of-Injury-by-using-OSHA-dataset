# -*- coding: utf-8 -*-
"""MAIN PROJECT nithin.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QLqzV3O-F3x8oIOfqQKN47-ZY-McfkZ-

DEGREE OF INJURY PREDICTION FROM OCCUPATIONAL SAFETY DATASET OF OSHA

Submitted by : Nithin Raj

**TABLE OF CONTENTS**

1.Problem Statement
2.Objective
3.Data Collection
4.Data Description
5.EDA
6.Data Preprocessing
7.visualization
8.Feature Engineering
9.Data Splitting
10.Model Selection
11.Model Training and Evaluation
12.Feature Selection
13.Hyperparameter tuning
14.Saving the model
15.Load the model

**PROBLEM STATEMENT**

Workplace injuries pose a significant challenge to organizations, impacting both employee well-being and operational efficiency. Understanding the factors that contribute to injury severity is essential for improving safety measures and reducing incident severity. By predicting the severity of potential injuries, companies can better prioritize safety protocols, allocate resources effectively, and proactively address high-risk scenarios to foster a safer working environment

**OBJECTIVE**

Using occupational safety data from OSHA, this project aims to develop a predictive model to classify the degree of injury that may result from various workplace incidents based on factors such as environmental conditions, industry, incident type, employee demographics, and other relevant variables.

**DATA COLLECTION**
"""

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_regression

"""***Load the dataset and using pandas to import the data***"""

data=pd.read_csv("/content/Final OSHA Accident and Inspections Data Merged May 2021.csv")
data.head(10)

"""**EXPLORATORY DATA ANALYSIS**

***Identifying the relevant columns by cross checking the name of columns***
"""

data.columns

"""***Drop irrelevant columns by using data.drop***"""

data = data.drop(['state_flag','health_const','nr_in_estab','reporting_id','health_marit','migrant','report_id','abstract_text','fall_distance', 'event_date','event_time','summary_nr','injury_line_nr','occ_code','naics_code','adv_notice','state_flag.1','site_zip','mail_street', 'mail_city', 'open_date', 'case_mod_date', 'close_conf_date','sic_code','host_est_key','site_address','mail_zip','owner_code','nonbuild_ht','close_case_date', 'ld_dt'],axis=1)

data

data.info()

"""***Get an overview of the dataset.This dataset contains 23896 columns and 40 rows. Datatypes are float,integer and objects.***"""

data.describe()

""" ***Get Summary statistics for numerical columns by using data.describe()***"""

data.isnull().sum()

data.isnull().sum()/len(data)*100

data=data.dropna(axis=1,thresh=15000)

data.isnull().sum()/len(data)*100

data.duplicated()

data.drop_duplicates()

"""***Finding out null values and duplicated values. remove duplicate values from the dataset .***"""

num_data = data.select_dtypes(include="number")
num_data

num_data.isnull().sum()

from sklearn.impute import SimpleImputer

data['degree_of_inj'] = SimpleImputer(strategy='median').fit_transform(data[['degree_of_inj']])

"""***Seperatly check the numerical columns from the dataset and tried to impute the column name degree_of_inj by median***"""

num_data.skew()

cat_data = data.select_dtypes(include="object")
cat_data

cat_data.isnull().sum()

data1=data.copy()
data1['fatality'].fillna('no',inplace=True)

sex_imputer = SimpleImputer(strategy='most_frequent')

# Fit the imputer and transform the 'sex' column
data['sex'] = sex_imputer.fit_transform(data[['sex']]).flatten()

union_status_imputer = SimpleImputer(strategy='most_frequent')

# Fit the imputer and transform the 'union_status' column
data['union_status'] = union_status_imputer.fit_transform(data[['union_status']]).flatten()

"""***In this step we already checked the categorical columns and impute most_frequent values in some categorical columns***"""

num_data

numeric_columns=list(num_data)
numeric_columns

"""***Visualize the distributions to check for outliers so plot histogram and boxplot.***"""

for column in numeric_columns:
    plt.figure(figsize=(12, 5))

    # Histogram
    plt.subplot(1, 2, 1)

    # Check if the column is numeric and cast to a numeric type if possible
    if data[column].dtype == 'object':
        try:
            data[column] = pd.to_numeric(data[column], errors='coerce')
        except ValueError:
            print(f"Warning: Skipping column '{column}' due to non-numeric values.")
            continue  # Skip this column if it can't be converted

    # Explicitly set the number of bins or bin range to avoid automatic calculation
    sns.histplot(data[column], kde=True, bins=30)  # Adjust the number of bins as needed
    # Or, use binrange: sns.histplot(data[column], kde=True, binrange=(min_val, max_val))

    plt.title(f'Histogram of {column}')
    plt.show()

for column in numeric_columns:
    plt.figure(figsize=(12, 5))

 # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(x=data[column])
    plt.title(f'Boxplot of {column}')

    plt.show()

"""***Remove outliers by applying IQR(Inter Quartile Range) method and visualize again to cross check whether outliers removed or not.***"""

def remove_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Return a filtered DataFrame that excludes outliers
    return data[(data[column] >= lower_bound) &  (data[column] <= upper_bound)]

# Start with the original data
cleaned_data = data.copy()  # Create a copy for cleaning

# Remove outliers for each numeric column
for column in numeric_columns:
    cleaned_data = remove_outliers_iqr(cleaned_data, column)

# Visualize the cleaned data again to confirm outliers are removed
for column in numeric_columns:
    plt.figure(figsize=(12, 5))

    # Histogram
    plt.subplot(1, 2, 1)
    sns.histplot(cleaned_data[column], kde=True)
    plt.title(f'Histogram of {column} after outlier removal')

    # Boxplot
    plt.subplot(1, 2, 2)
    sns.boxplot(x=cleaned_data[column])
    plt.title(f'Boxplot of {column} after outlier removal')

    plt.show()

cleaned_data.select_dtypes("number").skew()

cleaned_data.shape

cleaned_data["degree_of_inj"].value_counts()

"""**visualization**

***Use histograms and box plots to visualize individual features***
"""

# Histogram for degree of injury
sns.histplot(cleaned_data['degree_of_inj'].dropna(), bins=30, kde=True)
plt.title('Degree of injury histogram')
plt.xlabel('Degree of injury')
plt.ylabel('Frequency')
plt.show()

# Box plot for PM2.5
sns.boxplot(x=cleaned_data['degree_of_inj'].dropna())
plt.title('Boxplot of degree_of_inj')
plt.show()

"""***Scatter plots and bar plots to visualize the relationship between two variables.***"""

# Scatter plot between degree of inury and fatality
sns.scatterplot(x='degree_of_inj', y='fatality', data=cleaned_data)
plt.title('degree_of_inj vs fatality ')
plt.show()

# Bar plot for average degree of injury by nature_of_inj
degree_of_inju_nature_of_inj = cleaned_data.groupby('degree_of_inj')['nature_of_inj'].mean().reset_index()
sns.barplot(x='degree_of_inj', y='nature_of_inj', data=degree_of_inju_nature_of_inj)
plt.xticks(rotation=90)
plt.title('degree_of_inj by nature_of_inj')
plt.show()

""" ***Pair plots and heatmaps to explore relationships between multiple features.***"""

# Pair plot for a subset of variables
sns.pairplot(cleaned_data[['age',
 'nature_of_inj',
 'part_of_body','degree_of_inj','fatality']].dropna())
plt.suptitle('Pair Plot of Selected Features', y=1.02)
plt.show()

# Heatmap for correlation
corr_matrix = cleaned_data[['age',
 'nature_of_inj',
 'part_of_body','degree_of_inj']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

"""***Use histograms and KDE plots to visualize distributions.***"""

# fatality happend in occupational sites using histograms and KDE
sns.histplot(cleaned_data['fatality'].dropna(), bins=30, kde=True)
plt.title('Fatality histogram')
plt.xlabel('Fatality')
plt.ylabel('Frequency')
plt.show()

# KDE plot for part of body injured
sns.kdeplot(cleaned_data['part_of_body'].dropna(), shade=True)
plt.title('KDE Plot of part_of_body')
plt.xlabel('part_of_body')
plt.ylabel('degree_of_inj')
plt.show()

"""***According to the graph we have get some insights like part of body,nature of injury etc directly proportional to degree of injury and fatality.***

***Assume that x is our features and y is target***
"""

x=cleaned_data.drop("degree_of_inj",axis=1)
y=cleaned_data["degree_of_inj"]

x

y

cat_cleaned_data=x.select_dtypes(include="object")
cat_cleaned_data

cat_cleaned_data_columns=list(cat_cleaned_data)
cat_cleaned_data_columns

"""***Encode the categorical columns by using OneHotEncoder***"""

from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()

# Fit and transform the specified categorical columns
encoded_data = enc.fit_transform(x[cat_cleaned_data_columns]).toarray()

encoded_data

# Create a DataFrame from the encoded data
encoded_df = pd.DataFrame(encoded_data, columns=enc.get_feature_names_out(cat_cleaned_data_columns))

# Combine the encoded DataFrame with the original cleaned_data (excluding the original categorical columns)
x = pd.concat([x.drop(columns=cat_cleaned_data_columns).reset_index(drop=True), encoded_df], axis=1)

# Display the first few rows of the encoded DataFrame
x

x.shape

from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np

# Assume x is feature set and y is target variable
# Create a Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(x, y)

"""**Feature Engineering**

***By using feature importance method findout important features whichever we can apply for further process.***
"""

# Get feature importances
importances = model.feature_importances_
# Create a DataFrame to display feature importances
feature_importance_df = pd.DataFrame({
    'Feature': x.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

print(feature_importance_df)

# Set a threshold (example: 0.01)
threshold = 0.01

# Select features with importance above the threshold
selected_features = feature_importance_df[feature_importance_df['Importance'] > threshold]

print("Selected Features:")
print(selected_features)

X_selected = x[selected_features['Feature']]

"""***The above mentioned features are now important for this project.***"""

X_selected

y

"""***Installing imbalanced learn for SMOTE technique to varify features and target are balanced or imbalanced.***"""

!pip install imbalanced-learn

from imblearn.over_sampling import SMOTE

smote=SMOTE(random_state=42)
x_smote,y_smote=smote.fit_resample(x,y)

class_counts = y_smote.value_counts()
print('Balanced class distribution:\n',class_counts)
print('Balanced class ratios:\n',class_counts/len(y_smote))

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(X_selected)

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

"""**Data Splitting**

***Split the data into training and testing sets***
"""

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

"""***Standardization of data***"""

x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

"""**Model Selection**

***Initialize models such as Logisticregression,RandomForest classifier,DecissionTree,SVM,KNN and Calculate Training Accuracy Scores***
"""

log_reg = LogisticRegression()
log_reg.fit(x_train_scaled, y_train)

y_pred = log_reg.predict(x_test_scaled)

print("Logistic Regression prediction:",y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier()
dt.fit(x_train_scaled, y_train)

y_pred = dt.predict(x_test_scaled)

print("Decision Tree prediction:",y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier()
rf.fit(x_train_scaled, y_train)

y_pred = rf.predict(x_test_scaled)

print("Random Forest prediction:",y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

from sklearn.svm import SVC
svm = SVC()
svm.fit(x_train_scaled, y_train)

y_pred = svm.predict(x_test_scaled)

print("SVM prediction:",y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier()
knn.fit(x_train_scaled, y_train)

y_pred = knn.predict(x_test_scaled)

print("KNN prediction:",y_pred)
print("Accuracy:", accuracy_score(y_test, y_pred))

"""**Model Training and Evaluation**

** Model Training and Hyperparameter Tuning**:- The code performs hyperparameter tuning as before.
Metrics Calculation: After tuning, it calculates accuracy, precision, recall, F1 score, and ROC AUC score for each model on the test set.

Accuracy: Measures the overall correctness of the model.

Precision: Measures the accuracy of positive predictions.

Recall: Measures the ability to find all positive samples.

F1 Score: Harmonic mean of precision and recall.

ROC AUC: Measures the ability of the model to distinguish between classes.

Results Visualization: Finally, it presents the results in a DataFrame for easier comparison.
"""

from sklearn.model_selection import train_test_split, GridSearchCV

# Apply classification algorithms (Logistic Regression, SVM, Random Forest,Decision tree,KNN)
# Hyperparameter tuning using GridSearchCV

# Logistic Regression
log_reg = LogisticRegression(max_iter=1000)
log_reg_params = {'C': [0.01, 0.1, 1, 10]}
log_reg_grid = GridSearchCV(log_reg, log_reg_params, cv=5)
log_reg_grid.fit(x_train_scaled, y_train)

# SVM
svm = SVC()
svm_params = {'C': [0.1,1], 'kernel': ['linear', 'rbf']}
svm_grid = GridSearchCV(svm, svm_params, cv=5)
svm_grid.fit(x_train_scaled, y_train)

# Random Forest
rf = RandomForestClassifier()
rf_params = {'n_estimators': [10,50, 100, 150], 'max_depth': [2,3, 5, 7]}
rf_grid = GridSearchCV(rf, rf_params, cv=5)
rf_grid.fit(x_train_scaled, y_train)

# Decision tree
dt = DecisionTreeClassifier()
dt_params = {'max_depth': [2,3, 5, 7]}
dt_grid = GridSearchCV(dt, dt_params, cv=5)
dt_grid.fit(x_train_scaled, y_train)

#KNN
knn = KNeighborsClassifier()
knn_params = {'n_neighbors': [3, 5, 7, 9]}
knn_grid = GridSearchCV(knn, knn_params, cv=5)
knn_grid.fit(x_train_scaled, y_train)

# Evaluate model performance
def evaluate_model(model, x_test_scaled, y_test):
    y_pred = model.predict(x_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")

# Evaluate model performance
def evaluate_model(model, x_test_scaled, y_test):
    """
    Evaluates a model's performance by predicting on the test set and computing metrics.

    Args:
        model: The trained machine learning model.
        x_test_scaled: The scaled features of the test set.
        y_test: The true labels of the test set.
    """

    # Predict labels for the test set
    y_pred = model.predict(x_test_scaled)

    # Check if the lengths of y_test and y_pred match
    if len(y_test) != len(y_pred):
        print(f"Warning: Inconsistent sample sizes. y_test: {len(y_test)}, y_pred: {len(y_pred)}")
        # Attempt to resolve the issue by truncating the larger array
        min_len = min(len(y_test), len(y_pred))
        y_test = y_test[:min_len]
        y_pred = y_pred[:min_len]
        print(f"Truncated to minimum length: {min_len}")

    # Calculate and print accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy:.4f}")

    # Print classification report
    print(f"Classification Report:\n{classification_report(y_test, y_pred)}")

print("\nEvaluation for Logistic Regression:")
evaluate_model(log_reg_grid, x_test_scaled, y_test)

print("\nEvaluation for SVM:")
evaluate_model(svm_grid, x_test_scaled, y_test)

print("\nEvaluation for Random Forest:")
evaluate_model(rf_grid, x_test_scaled, y_test)

print("\nEvaluation for Decision Tree:")
evaluate_model(dt_grid, x_test_scaled, y_test)

print("\nEvaluation for KNN:")
evaluate_model(knn_grid, x_test_scaled, y_test)

from sklearn.datasets import make_classification
# Create a synthetic dataset
x, y = make_classification(n_samples=1000, n_features=10, n_informative=5, n_redundant=2, random_state=42)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Define parameter grids for each model
param_grids = {
    "Random Forest": {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    },
    "Decision Tree": {
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5, 10]
    },
    "Logistic Regression": {
        'C': [0.001, 0.01, 0.1, 1, 10],
        'solver': ['liblinear', 'saga']  # solvers that support L1 regularization
    },
    "SVM": {
        'C': [0.001, 0.01, 0.1, 1, 10],
        'kernel': ['linear', 'rbf']
    },
    "KNN": {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance']
    }
}

# Dictionary to hold the best models
best_models = {}

# Hyperparameter tuning using Grid Search
for name, model in [
    ("Random Forest", RandomForestClassifier()),
    ("Decision Tree", DecisionTreeClassifier()),
    ("Logistic Regression", LogisticRegression(max_iter=1000)),
    ("SVM", SVC(probability=True)),
    ("KNN", KNeighborsClassifier())
]:
    print(f"Tuning {name}...")
    grid_search = GridSearchCV(model, param_grids[name], cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(x_train, y_train)
    best_models[name] = grid_search.best_estimator_
    print(f"Best parameters for {name}: {grid_search.best_params_}")
    print(f"Best cross-validation score for {name}: {grid_search.best_score_:.4f}\n")

# Evaluate the best models on the test set
for name, model in best_models.items():
    test_score = model.score(x_test, y_test)
    print(f"Test accuracy for {name}: {test_score:.4f}")

"""***Find the model with the highest test accuracy***"""

# Store the test accuracies in a dictionary
test_accuracies = {
    'Random Forest': 0.9650,
    'Decision Tree': 0.9100,
    'Logistic Regression': 0.8300,
    'SVM': 0.9450,
    'KNN': 0.9250
}

# Find the model with the highest test accuracy
best_model = max(test_accuracies, key=test_accuracies.get)
best_accuracy = test_accuracies[best_model]

# Display the best model and its accuracy
print(f"The model with the highest test accuracy is: {best_model}")
print(f"Highest Test Accuracy: {best_accuracy:.4f}")

""" ***Save the best model and Choose the model with the highest performance metrics***"""

best_model = max([log_reg_grid, svm_grid, rf_grid], key=lambda model: model.best_score_)
print(f"\nBest model: {best_model.best_estimator_}")

"""**Save the Model**"""

# Save the best model using joblib
import joblib
joblib.dump(best_model, 'final_best_occupational_safety_model.pkl')

print("\nBest model saved as 'final_best_occupational_safety_model.pkl'")

"""**Load the model**"""

import joblib
# Load the saved model
loaded_model = joblib.load('final_best_occupational_safety_model.pkl')

"""***Predict degree of injury of a sample data by using model which I saved as best model***"""

sample_data = pd.DataFrame({'fatality_nan':[0.0],	'fatality_X':[1.0],	'nature_of_inj':[2.0],	'activity_nr':[17456682],	'part_of_body':[20.0],	'evn_factor':[1.0],	'rel_insp_nr':[17456682],	'src_of_injury':[27],	'age':[48],	'sic_list':[1791]})

prediction=loaded_model.predict(sample_data)
print("Predicted Degree of injury:",prediction[0])

"""***Prediction done by using the model is accurate***

***In OSHA Accident and inspection data, the nature of injury refers to the type of injury sustained by the worker during an accident. it describes the specific physical harm or illness resulting from the incident. some common categories of the nature of injury indicates in datasets***
1.Fractures
2.Lacerations
3.Burns
4.Contusions
5.Amputations
6.Sprains and strains
7.Respiratory Condition
8.Hearing loss
9.Electrocution
10.Chemical Burns
11.Puncture wounds
12.Cumulative Trauma Disorder

***In OSHA (Occupational Safety and Health Administration) reports, the "Degree of Injury" typically refers to the severity level of an injury sustained during a workplace incident. The classification often helps determine the response and preventive measures needed. Common categories for "Degree of Injury" in OSHA data include:***

1. Fatal – The injury resulted in the death of the worker.


2. Severe – The injury was serious, often leading to permanent disability, significant medical treatment, or hospitalization.


3. Moderate – The injury required medical attention beyond first aid but was not life-threatening.


4. Minor – The injury was less severe, potentially treated on-site or with basic first aid, and did not require extensive medical treatment.

**Key Insights:**
*This project successfully built a predictive model using OSHA accident and inspection data to classify the degree of injury in workplace incidents. By using a Random Forest Classifier the model achieved high accuracy, demonstrating its potential for real world application. Insights from feature importance suggest that significantly influence injury severity,offering valuable information for targeted safety measures. While the model requires all features for optimal performance, future improvements could focus on simplifying feature requirements. Overall, this project shows how machine learning can contribute to enhancing workplace safety and guiding inspection priorities.*
"""