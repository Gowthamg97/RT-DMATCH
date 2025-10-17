import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import RobustScaler
from scipy import stats

class AnomalyModule:
    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state

    def preprocess_numeric(self, df):
        """Auto-detect numeric cols, fill missing, handle outliers"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        data_num = df[numeric_cols].copy()

        # Fill missing values
        for col in numeric_cols:
            if 'Price' in col or 'Cost' in col:
                data_num[col] = data_num[col].fillna(0)
            elif 'Number' in col or 'ID' in col:
                data_num[col] = data_num[col].fillna(
                    data_num[col].mode()[0] if not data_num[col].mode().empty else 0
                )
            else:
                data_num[col] = data_num[col].fillna(data_num[col].median())

            # Remove extreme outliers
            if data_num[col].std() > 0:
                z_scores = np.abs(stats.zscore(data_num[col]))
                data_num.loc[z_scores > 3, col] = data_num[col].median()

        return data_num, numeric_cols

    def detect_per_feature(self, data_num, numeric_cols):
        """Run per-feature anomaly detection dynamically"""
        results = {}

        for col in numeric_cols:
            try:
                scaler = RobustScaler()
                col_scaled = scaler.fit_transform(data_num[[col]])

                model = IsolationForest(
                    contamination=self.contamination,
                    random_state=self.random_state
                )
                preds = model.fit_predict(col_scaled)
                scores = model.decision_function(col_scaled)

                results[col] = {
                    "predictions": preds,
                    "scores": scores,
                    "anomaly_rate": (preds == -1).mean() * 100
                }

                print(f" {col}: {results[col]['anomaly_rate']:.2f}% anomalies")

            except Exception as e:
                print(f" Error processing {col}: {str(e)}")

        return results
