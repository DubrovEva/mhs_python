import asyncio
import aiohttp
import argparse
from pathlib import Path
import sys


async def download_image(session, image_id, output_dir):
    url = f"https://picsum.photos/800/600?random={image_id}"
    filename = output_dir / f"image_{image_id:03d}.jpg"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                with open(filename, 'wb') as f:
                    f.write(content)
                print(f"Downloaded: {filename.name}")
                return str(filename)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
    return None


async def download_images(count, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, i, output_dir) for i in range(1, count + 1)]
        results = await asyncio.gather(*tasks)
    
    successful = [r for r in results if r]
    print(f"\nDownloaded {len(successful)}/{count} images")
    return successful


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('count', type=int)
    parser.add_argument('--output', '-o', default='artifacts/images')
    args = parser.parse_args()
    
    if args.count < 1:
        print("Error: count must be >= 1", file=sys.stderr)
        sys.exit(1)
    
    asyncio.run(download_images(args.count, Path(args.output)))
