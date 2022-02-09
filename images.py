from selenium import webdriver # automate browser
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# chrome webdriver local path
PATH = "C:\\Users\\Joyce\\Documents\\Clustering images\\chromedriver.exe"
wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

    # link to google product images
	url = "https://www.google.com/search?q=product+images&rlz=1C1CHBF_enRW948RW948&sxsrf=APq-WBtYR3GxbRE5o3CkOAurJJJpYltrhA:1643962525926&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjTw4bTzeX1AhVOt6QKHXybBL0Q_AUoAXoECAEQAw&biw=1536&bih=754&dpr=1.25"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

        # find all elements with classname ...
		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue
            
            # find specific image with classname ...
			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 20)

for i, url in enumerate(urls):
	download_image("images/", url, str(i) + ".jpg")

wd.quit()

