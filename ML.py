import pandas as pd
import security
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.datasets import make_classification
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.feature_selection import SelectKBest, chi2
from imblearn.over_sampling import SMOTE

from sklearn.metrics import classification_report

df = pd.read_csv('save.csv')
x = df.drop("case", axis=1)
y = df["case"]
df.isnull().sum()

# Handle class imbalance with SMOTE 
rus = SMOTE(sampling_strategy={0:8974 , 1:8974 })
X_res, y_res = rus.fit_resample(x, y)

# Split data 
X_train, X_test, y_train, y_test = train_test_split(X_res, y_res, test_size=0.1, random_state=1000)

# Feature selection pipeline
fea_sel = SelectKBest(chi2, k=10)

# Model selection pipeline 
clf = Pipeline([('feature_selection', fea_sel),
                ('classification', XGBClassifier(objective='binary:logistic', 
                               n_estimators=500, max_depth=8))])

# Hyperparameter tuning
parameters = { 'feature_selection__k': list(range(1,4)),

              'classification__max_depth': [3,5,7],
              'classification__n_estimators': [100,300,500]}



cv = StratifiedKFold(n_splits=5)
grid = GridSearchCV(clf, parameters, cv=cv, n_jobs=-1, verbose=1)

# Fit the model  
grid.fit(X_train, y_train)

# Evaluate on test set
y_pred = grid.predict(X_test)
print(classification_report(y_test, y_pred))
print(f'Accuracy on test set: {grid.score(X_test, y_test):.4f}')

# Import the entire module

security.call()
