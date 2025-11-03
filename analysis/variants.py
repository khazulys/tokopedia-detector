from typing import List, Dict
from collections import Counter

class VariantAnalyzer:
    @staticmethod
    def analyze(reviews: List[Dict]) -> Dict:
        variant_analysis = {
            'variant_distribution': {},
            'no_variant_percentage': 0,
            'single_variant_dominance': False,
            'variant_count': 0
        }
        
        variant_counter = Counter()
        no_variant_count = 0
        
        for review in reviews:
            variant_name = review.get('variantName', '')
            if variant_name:
                variant_counter[variant_name] += 1
            else:
                no_variant_count += 1
        
        variant_analysis['variant_distribution'] = dict(variant_counter)
        variant_analysis['variant_count'] = len(variant_counter)
        
        total_reviews = len(reviews)
        if total_reviews > 0:
            variant_analysis['no_variant_percentage'] = (no_variant_count / total_reviews) * 100
            
            if variant_counter:
                most_common_variant = variant_counter.most_common(1)[0]
                if most_common_variant[1] / total_reviews > 0.8:
                    variant_analysis['single_variant_dominance'] = True
        
        return variant_analysis
