import asyncio
import random
from typing import Optional
from playwright.async_api import Browser, async_playwright
from tracker.parsers.base_parser import BaseParser, ParseResult
from tracker.utils.string_utils import StringUtils


class RegardParser(BaseParser):
    """Парсер для regard.ru с защитой бот детекта"""

    def __init__(self, headless: bool = True, timeout = 30):
        super().__init__(timeout)
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.playwright = None
        self._init_lock = asyncio.Lock()

    async def __aenter__(self):
        await self._init_browser()
        return self
    
    async def __aexit__(self):
        await self.close()

    async def _init_browser(self):
        async with self._init_lock:
            if self.browser:
                return
            
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-web-security',
                    '--disable-features=IsolateOrigins,site-per-process',
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--disable-gpu',
                    '--window-size=1920,1080',
                ]
            )

    async def _create_context(self):
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent=random.choice(self.USER_AGENTS),
            locale='ru-RU',
            timezone_id='Europe/Moscow',
            permissions=['geolocation'],
            device_scale_factor=1,
            has_touch=False,
            java_script_enabled=True,
        )
        await context.add_init_script("""
            // cкрытие следов playwright
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            // подмена отпечатков
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ru-RU', 'ru', 'en-US', 'en']
            });
            window.chrome = {
                runtime: {}
            };
        """)
        return context

    async def get_product_name(self, page) -> str:
        try:
            name = await page.locator('h1[class^="Product_title__"]').text_content()
            if name := StringUtils.clean(name):
                return name
            
            title = await page.title()
            separator = ':'
            if title and separator in title:
                name = title.split(separator)[0]
                if name := StringUtils.clean(name):
                    return name
            
            return ''
            
        except Exception as e:
            print(f"Error getting product name: {e}")
            return ''
        
    async def get_product_price(self, page) -> float:
        try:
            price_element = page.locator('span[class^="Price_price__"]').first
            price_text = await price_element.text_content()
            if not price_text:
                return 0
            
            cleaned = StringUtils.clean_price(price_text)
            return float(cleaned) if cleaned else 0
        except Exception as e:
            print(f"Error getting product price: {e}")
            return 0
    
    async def parse(self, url: str) -> ParseResult:
        await self._init_browser()
        
        context = None
        page = None
        try:
            context = await self._create_context()
            page = await context.new_page()

            page.set_default_timeout(self.timeout * 1000)
            await asyncio.sleep(random.uniform(1, 3))

            response = await page.goto(url, wait_until='networkidle')
            if not response or not response.ok:
                return ParseResult(
                    price=0,
                    product_name='',
                    url=url,
                    error=f"HTTP Error: {response.status if response else 'No response'}"
                )

            await asyncio.sleep(random.uniform(0.5, 1.5))
            
            product_name = await self.get_product_name(page)
            product_price = await self.get_product_price(page)
            html = await page.content()

            return ParseResult(
                price=product_price,
                product_name=product_name,
                url=url,
                raw_response=html[:1000]
            )
        except Exception as e:
            return ParseResult(
                price=0,
                product_name='',
                url=url,
                error=str(e)
            )
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
    
    async def close(self):
        if self.browser:
            await self.browser.close()
            self.browser = None
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None