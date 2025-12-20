from collections import deque
from datetime import datetime, timedelta

class ClickFeatureStore:
    def __init__(self, window_days=30):
        self.window = timedelta(days=window_days)
        self.store = {}  # user_id -> deque of timestamps
    
    def record_click(self, user_id: str, ts: datetime):
        """Record a click event"""
        if user_id not in self.store:
            self.store[user_id] = deque()
        self.store[user_id].append(ts)
        self._evict_old(user_id, ts)
    
    def get_feature(self, user_id: str, current_ts: datetime) -> int:
        """Return click count in last window_days"""
        if user_id not in self.store:
            return 0
        self._evict_old(user_id, current_ts)
        return len(self.store[user_id])
    
    def _evict_old(self, user_id: str, current_ts: datetime):
        """Remove clicks older than window"""
        dq = self.store[user_id]
        while dq and dq[0] < current_ts - self.window:
            dq.popleft()
