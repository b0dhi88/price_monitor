from urllib.parse import urlparse
from typing import Optional

PARSER_REGISTRY = {
    'regard.ru': 'RegardParser',
    'extra-furnitura.ru': 'ExtraFurnituraParser',
}


def get_parser_for_url(url: str) -> Optional[str]:
    """
    Возвращает имя парсера для URL или None, если парсер не найден.
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        if domain.startswith('www.'):
            domain = domain[4:]
        return PARSER_REGISTRY.get(domain)
    except Exception:
        return None


def validate_url_has_parser(url: str) -> tuple[bool, Optional[str]]:
    """
    Проверяет, есть ли парсер для URL.
    Возвращает (is_valid, error_message).
    """
    parser_name = get_parser_for_url(url)
    if not parser_name:
        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith('www.'):
                domain = domain[4:]
        except Exception:
            domain = 'unknown'
        return False, f'Нет парсера для домена: {domain}'
    return True, None
