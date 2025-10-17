import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.neighbors import LocalOutlierFactor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
 
class EnhancedAnomalyDetector:
    def __init__(self, contamination=0.05, random_state=42):
        self.contamination = contamination
        self.random_state = random_state
        self.scaler = None
        self.models = {}
        self.results = {}
       
    def load_and_preprocess_data(self, file_path):
        """Load data and perform comprehensive preprocessing"""
        print("Loading and preprocessing data...")
        df = pd.read_csv(file_path)
       
        numeric_cols = [
            'Repair Order Number', 'Customer Number', 'Vehicle Model Year',
            'Service Advisor ID', 'Odometer In', 'Odometer Out',
            'Total Repair Order Price', 'Total Labor Price', 'Total Parts Price',
            'Total Miscellaneous Price', 'Total Sublet Price', 'Repair Order Line Number',
            'Operation Labor Price', 'Operation Actual Billed Labor Hours',
            'Operation Miscellaneious Price', 'Operation Part Price',
            'Operation Actual Labor Hours', 'Part Quantity', 'Part Total Cost',
            'Part Total Price', 'Service Technician Employee Number',
            'Service Technician Labor Rate Amount'
        ]
       
        # Filter existing columns
        existing_cols = [col for col in numeric_cols if col in df.columns]
        print(f"Using {len(existing_cols)} out of {len(numeric_cols)} specified columns")
       
        # Handle missing values more intelligently
        data_num = df[existing_cols].copy()
       
        # Fill missing values based on column characteristics
        for col in existing_cols:
            if 'Price' in col or 'Cost' in col:
                data_num[col] = data_num[col].fillna(0)  # Prices can be 0
            elif 'Number' in col or 'ID' in col:
                data_num[col] = data_num[col].fillna(data_num[col].mode()[0] if not data_num[col].mode().empty else 0)
            else:
                data_num[col] = data_num[col].fillna(data_num[col].median())
       
        # Remove extreme outliers for better scaling
        for col in existing_cols:
            if data_num[col].std() > 0: 
                z_scores = np.abs(stats.zscore(data_num[col]))
                data_num.loc[z_scores > 3, col] = data_num[col].median()

        anomaly_results = {}
        for col in existing_cols:
            try:
                scaler = RobustScaler()
                col_scaled = scaler.fit_transform(data_num[[col]])

                model = IsolationForest(contamination=self.contamination, random_state=self.random_state)
                preds = model.fit_predict(col_scaled)
                scores = model.decision_function(col_scaled)

                anomaly_results[col] = {
                    "predictions": preds,
                    "scores": scores,
                    "anomaly_rate": (preds == -1).mean() * 100
                }
                print(f"Processed feature: {col}, anomalies detected: {(preds == -1).sum()}")

            except Exception as e:
                print(f" Error processing {col}: {str(e)}")

        return df, data_num, existing_cols, anomaly_results
   
    def prepare_features(self, data_num):
        """Return original features without any engineering"""
        print("Using original features only...")
        return data_num.copy()
   
    def split_and_scale_data(self, features):
        """Split data and apply robust scaling"""
        print("Splitting and scaling data...")
       
        # Split data
        train_data, temp_data = train_test_split(features, test_size=0.4, random_state=self.random_state)
        val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=self.random_state)
       
        print(f"Train size: {len(train_data)}, Validation size: {len(val_data)}, Test size: {len(test_data)}")
       
        # Use RobustScaler (less sensitive to outliers than StandardScaler)
        self.scaler = RobustScaler()
        train_scaled = self.scaler.fit_transform(train_data)
        val_scaled = self.scaler.transform(val_data)
        test_scaled = self.scaler.transform(test_data)
       
        return train_scaled, val_scaled, test_scaled, train_data.index, val_data.index, test_data.index
   
    def optimize_hyperparameters(self, train_data, val_data):
        """Optimize hyperparameters using validation set"""
        print("Optimizing hyperparameters...")
       
        # Isolation Forest hyperparameter tuning
        best_if_score = -np.inf
        best_if_params = {}
       
        for n_est in [50, 100, 200]:
            for cont in [0.03, 0.05, 0.07, 0.1]:
                model = IsolationForest(n_estimators=n_est, contamination=cont, random_state=self.random_state)
                model.fit(train_data)
                val_scores = model.decision_function(val_data)
                score = np.mean(val_scores)
               
                if score > best_if_score:
                    best_if_score = score
                    best_if_params = {'n_estimators': n_est, 'contamination': cont}
       
        # One-Class SVM hyperparameter tuning
        best_svm_score = -np.inf
        best_svm_params = {}
       
        for nu in [0.03, 0.05, 0.07, 0.1]:
            for gamma in ['scale', 'auto', 0.001, 0.01, 0.1]:
                try:
                    model = OneClassSVM(kernel="rbf", gamma=gamma, nu=nu)
                    model.fit(train_data)
                    val_scores = model.decision_function(val_data)
                    score = np.mean(val_scores)
                   
                    if score > best_svm_score:
                        best_svm_score = score
                        best_svm_params = {'nu': nu, 'gamma': gamma}
                except:
                    continue
       
        # LOF hyperparameter tuning
        best_lof_score = -np.inf
        best_lof_params = {}
       
        for n_neighbors in [10, 20, 30, 50]:
            for cont in [0.03, 0.05, 0.07, 0.1]:
                model = LocalOutlierFactor(n_neighbors=n_neighbors, contamination=cont)
                val_preds = model.fit_predict(val_data)
                # Use negative outlier factor as score
                score = np.mean(model.negative_outlier_factor_)
               
                if score > best_lof_score:
                    best_lof_score = score
                    best_lof_params = {'n_neighbors': n_neighbors, 'contamination': cont}
       
        return best_if_params, best_svm_params, best_lof_params
   
    def train_models(self, train_data, val_data):
        """Train optimized models"""
        print("Training optimized models...")
       
        # Get best hyperparameters
        best_if, best_svm, best_lof = self.optimize_hyperparameters(train_data, val_data)
       
        print(f"Best IF params: {best_if}")
        print(f"Best SVM params: {best_svm}")
        print(f"Best LOF params: {best_lof}")
       
        # Train Isolation Forest
        self.models['isolation_forest'] = IsolationForest(
            random_state=self.random_state,
            **best_if
        )
        self.models['isolation_forest'].fit(train_data)
       
        # Train One-Class SVM
        self.models['one_class_svm'] = OneClassSVM(
            kernel="rbf",
            **best_svm
        )
        self.models['one_class_svm'].fit(train_data)
       
        # Store LOF params for later use
        self.lof_params = best_lof
       
    def predict_anomalies(self, test_data):
        """Generate predictions on test data"""
        print("Generating predictions...")
       
        results = pd.DataFrame(index=range(len(test_data)))
       
        # Isolation Forest
        results['IF_anomaly'] = self.models['isolation_forest'].predict(test_data)
        results['IF_score'] = self.models['isolation_forest'].decision_function(test_data)
       
        # One-Class SVM
        results['OCSVM_anomaly'] = self.models['one_class_svm'].predict(test_data)
        results['OCSVM_score'] = self.models['one_class_svm'].decision_function(test_data)
       
        # LOF (fit on test data with optimized parameters)
        lof_model = LocalOutlierFactor(**self.lof_params)
        results['LOF_anomaly'] = lof_model.fit_predict(test_data)
        results['LOF_score'] = lof_model.negative_outlier_factor_
       
        # Ensemble prediction (majority voting)
        anomaly_votes = (results[['IF_anomaly', 'OCSVM_anomaly', 'LOF_anomaly']] == -1).sum(axis=1)
        results['Ensemble_anomaly'] = np.where(anomaly_votes >= 2, -1, 1)
       
        # Ensemble score (average of normalized scores)
        normalized_scores = pd.DataFrame()
        for col in ['IF_score', 'OCSVM_score', 'LOF_score']:
            normalized_scores[col] = (results[col] - results[col].min()) / (results[col].max() - results[col].min())
        results['Ensemble_score'] = normalized_scores.mean(axis=1)
       
        return results
   
    def analyze_results(self, results, feature_names):
        """Analyze and summarize results"""
        print("\n" + "="*50)
        print("ANOMALY DETECTION RESULTS")
        print("="*50)
       
        methods = ['IF', 'OCSVM', 'LOF', 'Ensemble']
       
        for method in methods:
            anomaly_count = (results[f'{method}_anomaly'] == -1).sum()
            anomaly_rate = anomaly_count / len(results) * 100
            print(f"\n{method} Results:")
            print(f"  Anomalies detected: {anomaly_count} ({anomaly_rate:.2f}%)")
           
            if f'{method}_score' in results.columns:
                scores = results[f'{method}_score']
                print(f"  Score range: [{scores.min():.4f}, {scores.max():.4f}]")
                print(f"  Mean score: {scores.mean():.4f}")
       
        # Agreement between methods
        print(f"\nMethod Agreement:")
        methods_binary = ['IF_anomaly', 'OCSVM_anomaly', 'LOF_anomaly']
        correlation_matrix = results[methods_binary].corr()
        print(correlation_matrix)
       
        return results
   
    def save_results(self, original_df, results, test_indices, output_path="enhanced_anomaly_results.csv"):
        """Save comprehensive results"""
        print(f"\nSaving results to {output_path}")
       
        # Create output dataframe with original data + predictions
        output_df = original_df.loc[test_indices].copy()
       
        # Add all prediction results
        for col in results.columns:
            output_df[col] = results[col].values
       
        # Add risk categories
        output_df['Risk_Level'] = 'Low'
        ensemble_anomalies = results['Ensemble_anomaly'] == -1
        output_df.loc[test_indices[ensemble_anomalies], 'Risk_Level'] = 'High'
       
        # Save results
        output_df.to_csv(output_path, index=False)
       
        return output_df
 
def main():
    """Main execution function"""
    # Initialize detector
    detector = EnhancedAnomalyDetector(contamination=0.05, random_state=42)
   
    # File path
    file_path = r"C:\Users\Dell\Documents\dmatch\ro_ge\synthetic_dealer_repair_data_full_level2.csv"
   
    try:
        # Load and preprocess data
        df, data_num, feature_names = detector.load_and_preprocess_data(file_path)
       
        # Use original features without engineering
        features = detector.prepare_features(data_num)
       
        # Split and scale data
        train_scaled, val_scaled, test_scaled, train_idx, val_idx, test_idx = detector.split_and_scale_data(features)
       
        # Train models with hyperparameter optimization
        detector.train_models(train_scaled, val_scaled)
       
        # Generate predictions
        results = detector.predict_anomalies(test_scaled)
       
        # Analyze results
        results = detector.analyze_results(results, features.columns)
       
        # Save comprehensive results
        output_df = detector.save_results(df, results, test_idx)
       
        print(f"\n✅ Analysis complete! Results saved with {len(results)} test samples")
        print(f"📊 Enhanced features: {len(features.columns)} total features")
        print(f"🎯 Ensemble method provides most robust anomaly detection")
       
    except FileNotFoundError:
        print(f"❌ Error: Could not find file at {file_path}")
        print("Please check the file path and try again.")
    except Exception as e:
        print(f"❌ Error during execution: {str(e)}")
 
if __name__ == "__main__":
    main()
 
