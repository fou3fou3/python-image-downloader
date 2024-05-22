import aiohttp, asyncio, aiofiles, time, re, os
from urllib.parse import urlparse


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5672.126 Safari/537.36"

async def download_image(session: aiohttp.ClientSession, image_url: str, download_folder: str) -> None:
	try:
		if not os.path.exists(download_folder):
			os.makedirs(download_folder)

		image_name = urlparse(image_url).path.split('/')[-1]
		image_file = f'{download_folder}/{image_name}'

		if os.path.isfile(image_file) and os.path.getsize(image_file) > 10:  # bigger than 10b >:
				print(f'Image already exsits at: {image_file}')

		else:
			start = time.time()

			async with session.get(image_url, headers={'User-Agent': USER_AGENT}) as response:
				response.raise_for_status()
				async with aiofiles.open(image_file, 'wb') as image:
					await image.write(await response.read())
			end = time.time()
			print(f"Downloaded image from: {image_url} to: {image_file}, operation took: {abs((end - start))} seconds.")

	except aiohttp.ClientResponseError:
		await asyncio.sleep(5)
		await download_image(session, image_url, download_folder)

	except Exception as e:
		print(e)


async def download_images(images: list, download_folder: str = 'downloaded_images/') -> None:
	start = time.time()
	print(f'Downloading the list of images ...')

	async with aiohttp.ClientSession() as session:
		tasks = [download_image(session, image_url, download_folder) for image_url in images]
		await asyncio.gather(*tasks)

	end = time.time()
	print(f'Succesfuly downloaded {len(images)} images in: {abs((end - start))}s')
 
async def main(images_links_file: str = 'images.txt'):
	with open(images_links_file, 'r') as file:
		images = [line.strip() for line in file]
	
	await download_images(images)
  
if __name__ == "__main__":
	asyncio.run(main())