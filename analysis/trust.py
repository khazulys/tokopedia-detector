from typing import Dict, Optional
import time

class TrustAnalyzer:
    @staticmethod
    def analyze(shop_info: Dict, shop_rating: Optional[Dict] = None) -> Dict:
        trust_score = 0
        max_score = 100
        trust_analysis = {
            'trust_score': 0,
            'badges': [],
            'shop_age': None,
            'shop_score': 0,
            'shop_rating': 0,
            'total_reviews': 0,
            'total_favorites': 0,
            'is_official': False,
            'is_gold': False,
            'reasons': []
        }
        
        if not shop_info:
            return trust_analysis
        
        if shop_info.get('goldOS'):
            goldos = shop_info['goldOS']
            trust_analysis['is_official'] = goldos.get('isOfficial', False)
            trust_analysis['is_gold'] = goldos.get('isGold', False)
            trust_analysis['badges'].append(goldos.get('badge', ''))
            
            if trust_analysis['is_official']:
                trust_score += 30
                trust_analysis['reasons'].append("Official Store (+30)")
            
            if trust_analysis['is_gold']:
                trust_score += 20
                trust_analysis['reasons'].append("Gold Merchant (+20)")
        
        if shop_info.get('shopCore'):
            shop_core = shop_info['shopCore']
            shop_score = shop_core.get('shopScore', 0)
            trust_analysis['shop_score'] = shop_score
            
            if shop_score >= 95:
                trust_score += 25
                trust_analysis['reasons'].append(f"Excellent shop score {shop_score}% (+25)")
            elif shop_score >= 90:
                trust_score += 20
                trust_analysis['reasons'].append(f"Very good shop score {shop_score}% (+20)")
            elif shop_score >= 85:
                trust_score += 15
                trust_analysis['reasons'].append(f"Good shop score {shop_score}% (+15)")
            elif shop_score >= 80:
                trust_score += 10
                trust_analysis['reasons'].append(f"Fair shop score {shop_score}% (+10)")
        
        if shop_info.get('createInfo'):
            create_info = shop_info['createInfo']
            open_since = create_info.get('openSince', '')
            trust_analysis['shop_age'] = open_since
            
            try:
                shop_created = create_info.get('epochShopCreated', 0)
                if shop_created:
                    shop_age_days = (time.time() - shop_created) / 86400
                    if shop_age_days > 1095:
                        trust_score += 15
                        trust_analysis['reasons'].append("Store open > 3 years (+15)")
                    elif shop_age_days > 730:
                        trust_score += 12
                        trust_analysis['reasons'].append("Store open > 2 years (+12)")
                    elif shop_age_days > 365:
                        trust_score += 10
                        trust_analysis['reasons'].append("Store open > 1 year (+10)")
                    elif shop_age_days > 180:
                        trust_score += 5
                        trust_analysis['reasons'].append("Store open > 6 months (+5)")
            except:
                pass
        
        if shop_info.get('favoriteData'):
            total_fav = shop_info['favoriteData'].get('totalFavorite', 0)
            trust_analysis['total_favorites'] = total_fav
            
            if total_fav > 10000:
                trust_score += 10
                trust_analysis['reasons'].append(f"{total_fav:,} favorites (+10)")
            elif total_fav > 5000:
                trust_score += 8
                trust_analysis['reasons'].append(f"{total_fav:,} favorites (+8)")
            elif total_fav > 1000:
                trust_score += 5
                trust_analysis['reasons'].append(f"{total_fav:,} favorites (+5)")
        
        if shop_rating:
            rating_score = shop_rating.get('ratingScore', 0)
            try:
                rating_score = float(rating_score) if rating_score else 0.0
            except:
                rating_score = 0.0
            
            trust_analysis['shop_rating'] = rating_score
            trust_analysis['total_reviews'] = shop_rating.get('totalRating', 0)
            
            if rating_score >= 4.8:
                trust_score += 15
                trust_analysis['reasons'].append(f"Excellent rating {rating_score:.1f}/5.0 (+15)")
            elif rating_score >= 4.5:
                trust_score += 12
                trust_analysis['reasons'].append(f"Very good rating {rating_score:.1f}/5.0 (+12)")
            elif rating_score >= 4.0:
                trust_score += 8
                trust_analysis['reasons'].append(f"Good rating {rating_score:.1f}/5.0 (+8)")
            
            total_reviews = shop_rating.get('totalRating', 0)
            if total_reviews > 10000:
                trust_score += 10
                trust_analysis['reasons'].append(f"{total_reviews:,} shop reviews (+10)")
            elif total_reviews > 5000:
                trust_score += 8
                trust_analysis['reasons'].append(f"{total_reviews:,} shop reviews (+8)")
            elif total_reviews > 1000:
                trust_score += 5
                trust_analysis['reasons'].append(f"{total_reviews:,} shop reviews (+5)")
        
        trust_analysis['trust_score'] = min(trust_score, max_score)
        return trust_analysis
