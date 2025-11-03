import random
from typing import Dict, Optional

class HeaderGenerator:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        ]
    
    def generate(self, referer_url: Optional[str] = None) -> Dict[str, str]:
        user_agent = random.choice(self.user_agents)
        headers = {
            'User-Agent': user_agent,
            'Content-Type': "application/json",
            'sec-ch-ua': '"Chromium";v="137", "Not/A)Brand";v="24"',
            'x-version': f"2fcafb{random.randint(1,9)}",
            'sec-ch-ua-mobile': "?1" if "Android" in user_agent or "iPhone" in user_agent else "?0",
            'x-source': "tokopedia-lite",
            'bd-device-id': str(random.randint(7000000000000000000, 7999999999999999999)),
            'x-price-center': "true",
            'x-tkpd-lite-service': "phoenix",
            'sec-ch-ua-platform': '"Android"' if "Android" in user_agent else '"Windows"' if "Windows" in user_agent else '"iOS"',
            'origin': "https://www.tokopedia.com",
            'sec-fetch-site': "same-site",
            'sec-fetch-mode': "cors",
            'sec-fetch-dest': "empty",
            'accept-language': "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        if referer_url:
            headers['referer'] = referer_url
        return headers
