from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from system_design import ClickFeatureStore


def test_click_feature_store():
    store = ClickFeatureStore(window_days=30)
    now = datetime(2025, 12, 13)
    
    # No clicks yet
    assert store.get_feature("user1", now) == 0
    
    # Record one click
    store.record_click("user1", now - timedelta(days=1))
    assert store.get_feature("user1", now) == 1
    
    # Record another click outside window
    store.record_click("user1", now - timedelta(days=31))
    assert store.get_feature("user1", now) == 1  # old click ignored
    
    # Record multiple clicks
    for i in range(5):
        store.record_click("user2", now - timedelta(days=i))
    assert store.get_feature("user2", now) == 5
