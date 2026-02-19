import httpx
from bs4 import BeautifulSoup
from tracker.parsers.base_parser import BaseParser, ParseResult
from tracker.utils.string_utils import StringUtils


class ExtraFurnituraParser(BaseParser):
    async def parse(self, url: str) -> ParseResult:
        try:
            headers = self._get_headers()
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url, headers=headers)
                if not response.status_code == 200:
                    return ParseResult(
                        price=0,
                        product_name='',
                        url=url,
                        error=f"HTTP {response.status_code}"
                    )

                soup = BeautifulSoup(response.text, "html.parser")

                name = self._get_product_name(soup)
                price = self._get_product_price(soup)

                return ParseResult(
                    price=price,
                    product_name=name,
                    url=url
                )
        except Exception as e:
            return ParseResult(
                price=0,
                product_name='',
                url=url,
                error=str(e)
            )

    def _get_product_name(self, soup: BeautifulSoup) -> str:
        el = soup.select_one("div.preview_text.dotdot")
        return StringUtils.clean(el.get_text(strip=True)) if el else ''

    def _get_product_price(self, soup: BeautifulSoup) -> float:
        price_group = soup.select_one(".price_matrix_block .price_group")
        if not price_group:
            return 0
        price_el = price_group.select_one(".price_value")
        if not price_el:
            return 0
        price_text = StringUtils.clean_price(price_el.get_text(strip=True))
        return float(price_text) if price_text else 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
