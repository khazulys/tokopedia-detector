from typing import Dict, Optional

class FakeScorer:
    @staticmethod
    def calculate(patterns: Dict, buyers: Dict, ratings: Dict, time_data: Dict, 
                 rating_topics: Optional[Dict] = None, variants: Optional[Dict] = None) -> float:
        score = 0
        max_score = 100
        
        if patterns['generic_reviews'] > 10:
            score += 15
        elif patterns['generic_reviews'] > 5:
            score += 8
        
        if len(patterns['suspiciously_similar']) > 5:
            score += 20
        elif len(patterns['suspiciously_similar']) > 2:
            score += 10
        
        if patterns['keyword_stuffing'] > 5:
            score += 10
        
        if patterns['excessive_praise'] > 8:
            score += 10
        
        if buyers['anonymous_percentage'] > 50:
            score += 15
        elif buyers['anonymous_percentage'] > 30:
            score += 8
        
        if len(buyers['burst_reviewers']) > 3:
            score += 15
        
        if ratings['all_same_rating']:
            score += 20
        elif ratings['suspicious_pattern']:
            score += 15
        
        if len(ratings['sudden_influx']) > 2:
            score += 10
        
        if time_data['night_reviews'] > 30:
            score += 10
        
        if len(time_data['suspicious_hours']) > 2:
            score += 10
        
        if rating_topics and rating_topics.get('rating'):
            rating_data = rating_topics['rating']
            if rating_data.get('detail'):
                five_star = next((d for d in rating_data['detail'] if d.get('rate') == 5), None)
                one_star = next((d for d in rating_data['detail'] if d.get('rate') == 1), None)
                
                if five_star and five_star.get('percentageFloat', 0) > 95:
                    score += 15
                
                if one_star and one_star.get('totalReviews', 0) == 0 and rating_data.get('totalRating', 0) > 100:
                    score += 10
        
        if variants:
            if variants.get('single_variant_dominance'):
                score += 15
        
        if buyers.get('verified_buyers', 0) < 20:
            score += 10
        
        return min(score, max_score)
