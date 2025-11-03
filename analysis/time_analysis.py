from typing import List, Dict
from collections import Counter
from datetime import datetime

class TimeAnalyzer:
    @staticmethod
    def analyze(reviews: List[Dict]) -> Dict:
        time_analysis = {
            'reviews_per_hour': {},
            'suspicious_hours': [],
            'weekend_ratio': 0,
            'night_reviews': 0
        }
        
        hour_counter = Counter()
        weekend_count = 0
        night_count = 0
        
        for review in reviews:
            timestamp = review.get('reviewCreateTimestamp', 0)
            if timestamp:
                try:
                    timestamp = int(timestamp) if timestamp else 0
                    if timestamp > 0:
                        dt = datetime.fromtimestamp(timestamp)
                        hour = dt.hour
                        hour_counter[hour] += 1
                        
                        if dt.weekday() >= 5:
                            weekend_count += 1
                        
                        if hour >= 0 and hour < 6:
                            night_count += 1
                except (ValueError, TypeError, OSError):
                    continue
        
        time_analysis['reviews_per_hour'] = dict(hour_counter)
        
        for hour, count in hour_counter.items():
            if 2 <= hour <= 5 and count > 5:
                time_analysis['suspicious_hours'].append(hour)
        
        total_reviews = len(reviews)
        if total_reviews > 0:
            time_analysis['weekend_ratio'] = (weekend_count / total_reviews) * 100
            time_analysis['night_reviews'] = (night_count / total_reviews) * 100
        
        return time_analysis
