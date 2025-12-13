import pandas as pd

def clean_ads_data(df: pd.DataFrame, valid_ad_ids: list) -> pd.DataFrame:
    """
    Comprehensive data cleanup for ads dataset.
    
    Parameters:
        df (pd.DataFrame): Raw ads dataset
        valid_ad_ids (list): List of allowed ad_id values

    Steps:
    1. Drop duplicates based on user_id, ad_id, impression_ts
    2. Remove rows where click_ts is before impression_ts
    3. Handle negative purchase_value (set to 0)
    4. Drop rows with missing impression_ts (critical for CTR/metrics)
    5. Remove rows where purchase exists but click is missing
    6. Remove rows with invalid ad_ids
    7. Recreate indicators: click and purchase

    Returns:
        Cleaned DataFrame
    """
    # Start with a copy
    df_cleaned = df.copy()

    # 1. Drop duplicates
    df_cleaned = df_cleaned.drop_duplicates(subset=['user_id', 'ad_id', 'impression_ts'])

    # 2. Remove rows where click_ts is before impression_ts
    df_cleaned = df_cleaned[~(
        (df_cleaned['click_ts'].notna()) &
        (df_cleaned['impression_ts'].notna()) &
        (df_cleaned['click_ts'] < df_cleaned['impression_ts'])
    )]

    # 3. Handle negative purchase_value
    df_cleaned.loc[df_cleaned['purchase_value'] < 0, 'purchase_value'] = 0

    # 4. Drop rows with missing impression_ts
    df_cleaned = df_cleaned.dropna(subset=['impression_ts'])

    # 5. Remove rows where purchase exists but click is missing
    df_cleaned = df_cleaned[~(
        (df_cleaned['purchase_value'].notna()) &
        (df_cleaned['click_ts'].isna())
    )]

    # 6. Remove invalid ad_ids
    df_cleaned = df_cleaned[df_cleaned['ad_id'].isin(valid_ad_ids)]

    # 7. Recreate indicators
    df_cleaned['click'] = df_cleaned['click_ts'].notna().astype(int)
    df_cleaned['purchase'] = df_cleaned['purchase_value'].notna().astype(int)

    # Reset index
    df_cleaned = df_cleaned.reset_index(drop=True)

    return df_cleaned

def compute_ad_metrics(df_cleaned: pd.DataFrame) -> pd.DataFrame:
    """
    Compute aggregated ad metrics after cleaning.

    Output columns:
    - ad_id
    - impressions
    - clicks
    - ctr
    - purchases
    - conversion_rate
    - avg_purchase_value
    """
    # Aggregate by ad_id
    ad_metrics = df_cleaned.groupby('ad_id').agg(
        impressions=('impression_ts', 'count'),
        clicks=('click', 'sum'),
        purchases=('purchase', 'sum'),
        total_purchase_value=('purchase_value', 'sum')
    ).reset_index()

    # CTR: clicks / impressions
    ad_metrics['ctr'] = ad_metrics['clicks'] / ad_metrics['impressions']

    # Conversion rate: purchases / clicks
    ad_metrics['conversion_rate'] = ad_metrics.apply(
        lambda row: row['purchases'] / row['clicks'] if row['clicks'] > 0 else 0,
        axis=1
    )

    # Avg purchase value per click
    ad_metrics['avg_purchase_value'] = ad_metrics.apply(
        lambda row: row['total_purchase_value'] / row['clicks'] if row['clicks'] > 0 else 0,
        axis=1
    )

    # Round metrics
    ad_metrics['ctr'] = ad_metrics['ctr'].round(4)
    ad_metrics['conversion_rate'] = ad_metrics['conversion_rate'].round(4)
    ad_metrics['avg_purchase_value'] = ad_metrics['avg_purchase_value'].round(2)

    # Drop total_purchase_value column
    ad_metrics = ad_metrics.drop(columns=['total_purchase_value'])

    return ad_metrics

