# -*- coding: utf-8 -*-
"""Copy_of_Welcome_To_Colab.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QKymGFs7OGX7Cf-gGrKMbs7tKbSDkdUJ
"""

import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv("/content/data.csv")

print("Info")
df.info()
print("Describe")
df.describe()

print("First 10 rows")
df.head()

df.shape

df.isna().sum()

df = df.drop(["Unnamed: 32"],axis=1)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
df['diagnosis'] = le.fit_transform(df.iloc[:,1:2])

df.head()

df.corr()['diagnosis']>0

df = df.drop(['id','fractal_dimension_mean','texture_se','smoothness_se','symmetry_se'],axis=1)

df.sample(1)

from sklearn.model_selection import train_test_split as tts
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, recall_score

lr = LogisticRegression()
rf = RandomForestClassifier()

x = df.iloc[:,1:]
y = df.iloc[:,0:1]

#train test split
x_train, x_test, y_train, y_test = tts(x,y,test_size=0.3,random_state=42)

lr.fit(x_train,y_train)
rf.fit(x_train,y_train)

lr_pred = lr.predict(x_test)
rf_pred = rf.predict(x_test)

#accuracy and confusion matrix
print("Logistic Regression")
acc_lr = accuracy_score(lr_pred,y_test)
con_lr = confusion_matrix(lr_pred,y_test)
print(acc_lr, con_lr, sep="\n")

print("Random Forest")
acc_rf = accuracy_score(rf_pred,y_test)
con_rf = confusion_matrix(rf_pred,y_test)
print(acc_rf, con_rf, sep="\n")

!pip install catboost --quiet

# 2. Imports
import pandas as pd
from catboost import CatBoostClassifier, Pool
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
    classification_report,
    confusion_matrix
)

# 3. Load your data
df = pd.read_csv('/content/data.csv')   # <-- update this
X = df.drop('diagnosis', axis=1)               # <-- replace 'target' with your label column
y = df['diagnosis']

# 4. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 5. Wrap in CatBoost Pools (optional but recommended)
train_pool = Pool(X_train, y_train)
test_pool  = Pool(X_test,  y_test)

# 6. Define & fit a baseline CatBoost model
model = CatBoostClassifier(
    iterations=1000,
    learning_rate=0.1,
    depth=6,
    eval_metric='AUC',
    early_stopping_rounds=50,
    random_seed=42,
    verbose=100
)
model.fit(train_pool, eval_set=test_pool, use_best_model=True)

# 7. Evaluate
y_pred       = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:,1]

print("Accuracy:  ", accuracy_score(y_test, y_pred))
print("ROC AUC:    ", roc_auc_score(y_test, y_pred_proba))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


# 8. (Optional) Hyperparameter tuning with GridSearchCV
param_grid = {
    'depth': [4, 6, 8],
    'learning_rate': [0.01, 0.05, 0.1],
    'iterations': [500, 1000]
}
cb_base = CatBoostClassifier(
    random_seed=42,
    eval_metric='AUC',
    verbose=0
)
grid = GridSearchCV(
    cb_base,
    param_grid,
    cv=3,
    scoring='roc_auc',
    n_jobs=-1
)
grid.fit(X_train, y_train)

print("Best params:", grid.best_params_)
best_model = grid.best_estimator_

# Re-evaluate best_model
y_best_pred       = best_model.predict(X_test)
y_best_pred_proba = best_model.predict_proba(X_test)[:,1]

print("\nTuned Model ROC AUC:", roc_auc_score(y_test, y_best_pred_proba))