from typing import List, Dict
from collections import Counter

class BuyerAnalyzer:
    @staticmethod
    def analyze(reviews: List[Dict]) -> Dict:
        buyer_analysis = {
            'anonymous_percentage': 0,
            'new_accounts': 0,
            'single_review_accounts': [],
            'burst_reviewers': [],
            'verified_buyers': 0,
            'labeled_users': {}
        }
        
        total_reviews = len(reviews)
        anonymous_count = sum(1 for r in reviews if r.get('isAnonymous', False))
        
        if total_reviews > 0:
            buyer_analysis['anonymous_percentage'] = (anonymous_count / total_reviews) * 100
        
        user_review_times = {}
        label_counter = Counter()
        
        for review in reviews:
            if review.get('user') and review['user'].get('userID'):
                user_id = review['user']['userID']
                timestamp = review.get('reviewCreateTimestamp', 0)
                try:
                    timestamp = int(timestamp) if timestamp else 0
                except (ValueError, TypeError):
                    timestamp = 0
                
                if user_id not in user_review_times:
                    user_review_times[user_id] = []
                user_review_times[user_id].append(timestamp)
                
                if review['user'].get('label'):
                    label_counter[review['user']['label']] += 1
        
        buyer_analysis['labeled_users'] = dict(label_counter)
        
        if 'Verified Buyer' in label_counter:
            buyer_analysis['verified_buyers'] = (label_counter['Verified Buyer'] / total_reviews * 100) if total_reviews > 0 else 0
        
        for user_id, timestamps in user_review_times.items():
            if len(timestamps) > 1:
                timestamps.sort()
                time_diffs = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
                
                if any(diff < 300 for diff in time_diffs):
                    buyer_analysis['burst_reviewers'].append(user_id)
        
        return buyer_analysis
