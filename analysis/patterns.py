from typing import List, Dict
from collections import Counter
from ..utils import calculate_similarity

class PatternAnalyzer:
    @staticmethod
    def analyze(reviews: List[Dict]) -> Dict:
        patterns = {
            'duplicate_phrases': [],
            'generic_reviews': 0,
            'suspiciously_similar': [],
            'excessive_praise': 0,
            'keyword_stuffing': 0
        }
        
        generic_phrases = [
            'bagus', 'mantap', 'oke', 'recommended', 'puas', 'sesuai',
            'cepat', 'original', 'terima kasih', 'makasih', 'thanks'
        ]
        
        messages = [r['message'] for r in reviews if r.get('message')]
        
        for i, msg1 in enumerate(messages):
            if not msg1:
                continue
                
            msg1_lower = msg1.lower()
            
            if len(msg1_lower.split()) < 5:
                patterns['generic_reviews'] += 1
            
            if msg1_lower.count('bagus') > 2 or msg1_lower.count('mantap') > 2:
                patterns['keyword_stuffing'] += 1
            
            if any(phrase in msg1_lower for phrase in ['terbaik', 'sempurna', 'luar biasa', 'sangat bagus sekali']):
                patterns['excessive_praise'] += 1
            
            for j, msg2 in enumerate(messages[i+1:], i+1):
                if not msg2:
                    continue
                similarity = calculate_similarity(msg1, msg2)
                if similarity > 0.8:
                    patterns['suspiciously_similar'].append((i, j, similarity))
        
        phrase_counter = Counter()
        for msg in messages:
            if msg:
                words = msg.lower().split()
                for i in range(len(words) - 2):
                    phrase = ' '.join(words[i:i+3])
                    phrase_counter[phrase] += 1
        
        patterns['duplicate_phrases'] = [(phrase, count) for phrase, count in phrase_counter.items() if count > 3]
        
        return patterns
