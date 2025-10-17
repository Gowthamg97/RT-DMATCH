from sklearn.svm import OneClassSVM

class AnomalyModule:
    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state

    def preprocess_numeric(self, df):
        """Auto-detect numeric cols, fill missing, handle outliers"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        data_num = df[numeric_cols].copy()

        # Fill missing values and handle outliers
        for col in numeric_cols:
            if 'Price' in col or 'Cost' in col:
                data_num[col] = data_num[col].fillna(0)
            elif 'Number' in col or 'ID' in col:
                data_num[col] = data_num[col].fillna(
                    data_num[col].mode()[0] if not data_num[col].mode().empty else 0
                )
            else:
                data_num[col] = data_num[col].fillna(data_num[col].median())

            # Remove extreme outliers (z-score > 3 replaced by median)
            if data_num[col].std() > 0:
                z_scores = np.abs(stats.zscore(data_num[col]))
                data_num.loc[z_scores > 3, col] = data_num[col].median()

        return data_num, numeric_cols

    def detect_per_feature_with_models(self, data_num, numeric_cols, model_name="IsolationForest"):
        """Run per-feature anomaly detection with multiple models"""
        results = {}

        for col in numeric_cols:
            try:
                # Scale data for each feature separately
                scaler = RobustScaler()
                col_scaled = scaler.fit_transform(data_num[[col]])

                if model_name == "IsolationForest":
                    model = IsolationForest(contamination=self.contamination,
                                            random_state=self.random_state)
                    preds = model.fit_predict(col_scaled)
                    scores = model.decision_function(col_scaled)

                elif model_name == "OneClassSVM":
                    model = OneClassSVM(kernel="rbf", gamma="scale", nu=self.contamination)
                    preds = model.fit_predict(col_scaled)
                    # decision_function returns raw score, higher means more normal
                    scores = model.decision_function(col_scaled)

                elif model_name == "LOF":
                    model = LocalOutlierFactor(contamination=self.contamination,
                                               novelty=True)  # novelty=True to allow predict on same data
                    model.fit(col_scaled)
                    preds = model.predict(col_scaled)
                    # negative_outlier_factor_ attribute (negative LOF scores)
                    # For consistency, convert to positive score as inverse
                    scores = -model.negative_outlier_factor_

                else:
                    raise ValueError(f"Unsupported model name: {model_name}")

                results[col] = {
                    "predictions": preds,
                    "scores": scores,
                    "anomaly_rate": (preds == -1).mean() * 100
                }
                print(f"{col}: {results[col]['anomaly_rate']:.2f}% anomalies detected using {model_name}")

            except Exception as e:
                print(f"Error processing {col}: {str(e)}")

        return results
