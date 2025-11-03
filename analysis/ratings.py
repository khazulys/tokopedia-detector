from typing import List, Dict
from collections import Counter
from datetime import datetime
import statistics

class RatingAnalyzer:
    @staticmethod
    def analyze(reviews: List[Dict]) -> Dict:
        rating_analysis = {
            'distribution': {},
            'average': 0,
            'suspicious_pattern': False,
            'all_same_rating': False,
            'sudden_influx': []
        }
        
        ratings = [r['productRating'] for r in reviews if r.get('productRating')]
        
        if ratings:
            rating_counter = Counter(ratings)
            rating_analysis['distribution'] = dict(rating_counter)
            rating_analysis['average'] = statistics.mean(ratings)
            
            if len(set(ratings)) == 1:
                rating_analysis['all_same_rating'] = True
            
            five_star_percentage = rating_counter.get(5, 0) / len(ratings) * 100
            if five_star_percentage > 90:
                rating_analysis['suspicious_pattern'] = True
        
        timestamps_by_day = {}
        for review in reviews:
            timestamp = review.get('reviewCreateTimestamp', 0)
            if timestamp:
                try:
                    timestamp = int(timestamp) if timestamp else 0
                    if timestamp > 0:
                        date = datetime.fromtimestamp(timestamp).date()
                        if date not in timestamps_by_day:
                            timestamps_by_day[date] = 0
                        timestamps_by_day[date] += 1
                except (ValueError, TypeError, OSError):
                    continue
        
        for date, count in timestamps_by_day.items():
            if count > 10:
                rating_analysis['sudden_influx'].append((str(date), count))
        
        return rating_analysis
