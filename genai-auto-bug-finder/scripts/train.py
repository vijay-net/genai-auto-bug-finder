
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib, os
FEATURES = ['loc','avg_line_len','cyclomatic','functions','danger_eval','danger_exec','danger_subprocess_shell','danger_broad_except','danger_mutable_default','danger_innerHTML','danger_document_write','danger_var_usage']

def main():
    df = pd.read_csv('data/training/synthetic_training.csv')
    X = df[FEATURES]; y = df['label']
    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2,random_state=42)
    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(Xtr, ytr)
    print(classification_report(yte, clf.predict(Xte)))
    os.makedirs('models', exist_ok=True)
    joblib.dump(clf, 'models/rf_model.joblib')
    print('Model saved to models/rf_model.joblib')

if __name__=='__main__':
    main()
