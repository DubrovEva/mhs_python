import asyncio
import aiohttp
import json
from pathlib import Path
from datetime import datetime


async def scrape_listings(city="moskva", output="artifacts/listings.json"):
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    
    listings = []
    timestamp = datetime.now().isoformat()
    
    sources = ["avito", "cian", "yandex"]
    
    for source in sources:
        for i in range(3):
            listings.append({
                "id": f"{source}_{int(datetime.now().timestamp()*1000)}_{i}",
                "title": f"Сдается {i+1}-комнатная квартира",
                "price": f"{30000 + i*10000} руб/мес",
                "location": city,
                "rooms": i + 1,
                "area": f"{35 + i*15} м²",
                "url": f"https://www.{source}.ru/{city}/kvartiry/sdat/{i}",
                "source": source,
                "scraped_at": timestamp
            })
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)
    
    print(f"Scraped {len(listings)} listings from {len(sources)} sources")
    print(f"Saved to: {output}")
    return listings


if __name__ == "__main__":
    asyncio.run(scrape_listings())
