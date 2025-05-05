from sklearn.ensemble import RandomForestClassifier
import joblib

X = [[0, 1], [1, 0], [0, 0], [1, 1]]
y = [0, 1, 0, 1]  # 1 = Fraud, 0 = Not fraud

model = RandomForestClassifier().fit(X, y)
joblib.dump(model, 'fraud_model.pkl')