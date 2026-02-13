import re


class StringUtils:
    
    @staticmethod
    def clean(text: str | None) -> str | None:
        if not text:
            return None
        cleaned = text.strip()
        return cleaned if cleaned else None
    
    @staticmethod
    def clean_price(price_text: str) -> str:
        if not price_text:
            return ''
        return re.sub(r'[^\d.]', '', price_text.replace(',', '.'))