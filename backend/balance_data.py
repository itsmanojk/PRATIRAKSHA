import pandas as pd
from imblearn.over_sampling import SMOTE

# Load the dataset
file_path = r'C:/Users/manoj/OneDrive/Desktop/PRATIRAKSHA-Production/data/PRATIRAKSHA_ransomware_dataset.csv'
df = pd.read_csv(file_path)

# Separate features and label
X = df.drop('Label', axis=1)
y = df['Label']

# Apply SMOTE to balance classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Combine back to a DataFrame
balanced_df = pd.DataFrame(X_resampled, columns=X.columns)
balanced_df['Label'] = y_resampled

# Save the balanced dataset
balanced_path = r'C:/Users/manoj/OneDrive/Desktop/PRATIRAKSHA-Production/data/PRATIRAKSHA_ransomware_dataset_balanced.csv'
balanced_df.to_csv(balanced_path, index=False)

print('Balanced dataset saved to:', balanced_path)
print('Class distribution after balancing:')
print(balanced_df['Label'].value_counts())
