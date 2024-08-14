import os
import requests
import bs4

# Define constants
base_url = 'https://www.kaleva.fi'
start_page = base_url + '/sarjakuvat/fingerpori/6313167'
max_iterations = 500  # Set a limit to avoid infinite loop
images_dir = 'images'

def create_images_directory():
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)

def download_image(url):
    print('Downloading ' + url)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        # Extract the filename from the URL
        filename = os.path.join(images_dir, url.split('/')[-1])

        # filename = url.split('/')[-1]
        print('Filename: ' + filename)
        with open(filename, 'wb') as f:
            for chunk in res.iter_content():
                f.write(chunk)
    else:
        print('Failed to download image, status code:', res.status_code)

def fetch_comic_page(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.text

def parse_comic_image_url(page_content):
    soup = bs4.BeautifulSoup(page_content, "html.parser")
    cart = soup.select('div.cartoon-strip__image > img')
    if cart:
        return cart[0]['src']
    else:
        print('No comic image found')
        return None

def find_previous_comic_url(page_content):
    soup = bs4.BeautifulSoup(page_content, "html.parser")
    prev_link = soup.select('a.cartoon-strip__change-date')  # Adjust the selector based on the actual HTML structure
    if prev_link:
        return base_url + prev_link[0]['href']
    else:
        print('No previous comic link found')
        return None

def main():
    comic_page_url = start_page
    iterations = 0

    create_images_directory()

    while comic_page_url and iterations < max_iterations:
        page_content = fetch_comic_page(comic_page_url)
        comic_image_url = parse_comic_image_url(page_content)
        
        if comic_image_url:
            print('Comic image URL:', comic_image_url)
            download_image(comic_image_url)
            print("Image downloaded successfully.")
        else:
            print("Failed to find comic image URL.")
            break
        
        print('----------------------------------------')
        comic_page_url = find_previous_comic_url(page_content)
        iterations += 1

if __name__ == "__main__":
    main()
