class StringUtils:
    
    @staticmethod
    def clean(text: str | None) -> str | None:
        if not text:
            return None
        cleaned = text.strip()
        return cleaned if cleaned else None