import sys
import os
import pytest
import pandas as pd

# Make sure src folder is in path for terminal run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from data_analysis import clean_ads_data, compute_ad_metrics

@pytest.fixture
def sample_data():
    """Sample raw data with edge cases"""
    data = {
        'user_id': [1, 1, 2, 3, 4, 5, 6, 7],
        'ad_id': [1, 1, 2, 999, 3, 4, 5, 2],
        'impression_ts': [
            pd.Timestamp('2025-12-01 08:00:00'),  # keep
            pd.Timestamp('2025-12-01 08:00:00'),  # duplicate
            pd.Timestamp('2025-12-01 08:05:00'),  # keep
            pd.NaT,                               # missing impression → remove
            pd.Timestamp('2025-12-01 08:10:00'),  # keep
            pd.Timestamp('2025-12-01 08:15:00'),  # keep
            pd.Timestamp('2025-12-01 08:20:00'),  # keep
            pd.Timestamp('2025-12-01 08:25:00')   # purchase without click → remove
        ],
        'click_ts': [
            pd.Timestamp('2025-12-01 08:02:00'),  # ok
            pd.Timestamp('2025-12-01 08:01:00'),  # click before impression → remove
            pd.NaT,                               # no click
            pd.Timestamp('2025-12-01 08:07:00'),  # irrelevant, impression missing
            pd.Timestamp('2025-12-01 08:09:00'),  # ok
            pd.NaT,                               # no click, no purchase → keep
            pd.Timestamp('2025-12-01 08:25:00'),  # ok
            pd.NaT                                # purchase without click → remove
        ],
        'purchase_value': [50, 50, None, 100, -10, None, 200, 100]
    }
    return pd.DataFrame(data)

def test_clean_ads_data(sample_data):
    valid_ad_ids = [1, 2, 3, 4, 5]
    df_cleaned = clean_ads_data(sample_data, valid_ad_ids)

    # Expected cleaned data
    expected_data = {
        'user_id': [1, 2, 5, 6],
        'ad_id': [1, 2, 4, 5],
        'impression_ts': [
            pd.Timestamp('2025-12-01 08:00:00'),  # first row kept
            pd.Timestamp('2025-12-01 08:05:00'),  # row with no click
            pd.Timestamp('2025-12-01 08:15:00'),  # no click/purchase → ok
            pd.Timestamp('2025-12-01 08:20:00')   # ok
        ],
        'click_ts': [
            pd.Timestamp('2025-12-01 08:02:00'),
            pd.NaT,
            pd.NaT,
            pd.Timestamp('2025-12-01 08:25:00')
        ],
        'purchase_value': [50, None, None, 200],
        'click': [1, 0, 0, 1],
        'purchase': [1, 0, 0, 1]
    }
    df_expected = pd.DataFrame(expected_data).reset_index(drop=True)

    pd.testing.assert_frame_equal(
        df_cleaned.sort_index(axis=1),
        df_expected.sort_index(axis=1),
        check_dtype=False
    )

def test_compute_ad_metrics(sample_data):
    valid_ad_ids = [1, 2, 3, 4, 5]
    df_cleaned = clean_ads_data(sample_data, valid_ad_ids)
    ad_metrics = compute_ad_metrics(df_cleaned)

    # Expected aggregated metrics
    expected_metrics_data = {
        'ad_id': [1, 2, 4, 5],
        'impressions': [1, 1, 1, 1],
        'clicks': [1, 0, 0, 1],
        'purchases': [1, 0, 0, 1],
        'ctr': [1.0, 0.0, 0.0, 1.0],
        'conversion_rate': [1.0, 0.0, 0.0, 1.0],
        'avg_purchase_value': [50.0, 0.0, 0.0, 200.0]
    }
    df_expected_metrics = pd.DataFrame(expected_metrics_data)

    pd.testing.assert_frame_equal(
        ad_metrics.sort_index(axis=1),
        df_expected_metrics.sort_index(axis=1),
        check_dtype=False
    )
