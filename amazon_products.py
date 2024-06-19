import time

import requests
from scrapy import Selector
import pandas as pd

# Your proxies and headers are correctly defined here
proxy_list = [
    'http://customer-sakshipandey-cc-bd:mP_5GeK7RtM92a5@pr.oxylabs.io:7777'
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT": "1",
    "Connection": "close",
    "Upgrade-Insecure-Requests": "1"
}

data = []
for page in range(1, 21):
    try:
        print(page)
        index = page % len(proxy_list)
        proxies = {
            'http': proxy_list[index],
            'https': proxy_list[index]
        }
        url = f"https://www.amazon.co.uk/s?k=headphones&page={page}&adgrpid=119029923498&hvadid=498455637770&hvdev=m&hvlocint=9044911&hvlocphy=9040241&hvnetw=g&hvqmt=e&hvrand=9168423748744710586&hvtargid=kwd-11647051&hydadcr=7590_1724963&qid=1707463674"

        # Use requests.get with proxies and headers
        response = requests.get(url, proxies=proxies, headers=headers)
        time.sleep(1)
        if response.status_code == 200:  # Check if the response is successful
            response1 = Selector(text=response.text)
            for div in response1.css('div.s-result-list > div.s-result-item.s-asin'):
                rating = str(div.css("i.a-icon-star-small > span::text").get(''))
                data.append(
                    {
                        "Product Title": div.css('span.a-size-medium.a-color-base.a-text-normal::text').get().strip(),
                        "Price": div.css("span.a-size-base.s-underline-text::text").get('').strip(),
                        "Rating": rating.split()[0] if len(rating.split()) > 0 else None,
                        "Review count": div.css("span.a-size-base.s-underline-text::text").get('').strip(),
                        "Product URL": f"https://www.amazon.co.uk{div.css('h2 > a.s-underline-link-text::attr(href)').get('')}"
                    }
                )
    except Exception as e:
        print(e)

df = pd.DataFrame(data)

df.to_csv(r'Products.csv', index=True)
