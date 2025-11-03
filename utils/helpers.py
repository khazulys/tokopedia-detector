def calculate_similarity(text1: str, text2: str) -> float:
    if not text1 or not text2:
        return 0.0
    
    text1 = text1.lower()
    text2 = text2.lower()
    
    if text1 == text2:
        return 1.0
    
    words1 = set(text1.split())
    words2 = set(text2.split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0
