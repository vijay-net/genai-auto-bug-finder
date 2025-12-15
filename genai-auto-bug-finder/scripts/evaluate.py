
import pandas as pd, joblib
from sklearn.metrics import roc_auc_score, classification_report
FEATURES = ['loc','avg_line_len','cyclomatic','functions','danger_eval','danger_exec','danger_subprocess_shell','danger_broad_except','danger_mutable_default','danger_innerHTML','danger_document_write','danger_var_usage']

def main():
    df = pd.read_csv('data/training/synthetic_training.csv')
    X = df[FEATURES]; y = df['label']
    m = joblib.load('models/rf_model.joblib')
    print('AUC:', roc_auc_score(y, m.predict_proba(X)[:,1]))
    print(classification_report(y, m.predict(X)))

if __name__=='__main__':
    main()
