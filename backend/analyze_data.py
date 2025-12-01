import pandas as pd

# Load the dataset
file_path = r'C:/Users/manoj/OneDrive/Desktop/PRATIRAKSHA-Production/data/PRATIRAKSHA_ransomware_dataset.csv'
df = pd.read_csv(file_path)

# 1. Show basic info
def dataset_overview(df):
    print('--- Dataset Overview ---')
    print(df.info())
    print('\nSample rows:')
    print(df.head())
    print('\nMissing values per column:')
    print(df.isnull().sum())
    print('\nClass distribution:')
    print(df['Label'].value_counts())
    print('\n')

# 2. Check for duplicates
def check_duplicates(df):
    num_duplicates = df.duplicated().sum()
    print(f'Duplicated rows: {num_duplicates}')
    if num_duplicates > 0:
        print('Consider removing duplicates for better model accuracy.')
    print('\n')

# 3. Check for constant columns
def check_constant_columns(df):
    constant_cols = [col for col in df.columns if df[col].nunique() == 1]
    if constant_cols:
        print('Constant columns (no variance):', constant_cols)
    else:
        print('No constant columns found.')
    print('\n')

# 4. Check for outliers (simple z-score method)
def check_outliers(df, threshold=4):
    from scipy.stats import zscore
    features = df.select_dtypes(include=['float64', 'int64']).columns
    z_scores = df[features].apply(zscore)
    outlier_rows = (z_scores.abs() > threshold).any(axis=1)
    print(f'Rows with extreme outliers (z > {threshold}): {outlier_rows.sum()}')
    print('\n')

# 5. Show class balance
def show_class_balance(df):
    print('Class balance:')
    print(df['Label'].value_counts(normalize=True))
    print('\n')

if __name__ == '__main__':
    try:
        dataset_overview(df)
        check_duplicates(df)
        check_constant_columns(df)
        check_outliers(df)
        show_class_balance(df)
    except FileNotFoundError:
        print('Dataset file not found. Please check the file path.')
