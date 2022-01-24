"""Webscraper iNaturalist"""

"""
Downloads n images for a given species. The user only needs to provide the species id in the url 
and a target folder where the images should be downloaded.

Code inspired by:
    https://medium.com/swlh/web-scraping-stock-images-using-google-selenium-and-python-8b825ba649b9
    https://medium.com/geekculture/scraping-images-using-selenium-f35fab26b122
"""

# Import libraries
import time
import requests
import io, os
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image



def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int = 5):
    """Find and store the image urls.
    
    :param query: Species ID to complete the url.
    :type query: str
    :param max_links_to_fetch: Maximum number of urls to download.
    :type max_links_to_fetch: int
    :param wd: Webdriver specific for your browser.
    :type wd: selenium.webdriver
    :param sleep_between_interactions: Number of seconds to wait until next iteration. Defaults to 5 seconds.
    :type sleep_between_interactions: int, optional
    :return: Set of urls
    """
    
    # Enable infinite scrolling
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)  
         
    # Build the search query
    search_url = f"https://www.inaturalist.org/observations?place_id=any&subview=table&taxon_id={query}" # load the page
    wd.get(search_url)
    time.sleep(sleep_between_interactions)  
    
    # Define empty set for urls and image counter
    image_urls = set()
    image_count = 0
    results_start = 0
    reached_max = False
    page_num = 1 # current page number
    
    # Get total number of pages 
    last_page_link = wd.find_elements(By.XPATH, "//li[@class='pagination-page ng-scope']/a")[-1]
    if last_page_link:
        num_pages = int( last_page_link.get_attribute('text') )
    else:
        num_pages = 1 # only one page, no links to new pages

    # View all results on page
    while image_count < max_links_to_fetch:
        
        scroll_to_end(wd)
        thumb = wd.find_elements(By.CSS_SELECTOR, 'a.img') # after each scrolling, the list increases
        num_results = len(thumb)
        
        # If the new thumbnail list is as long as before, you have reached the end of the page
        # Load next page (in case there is one)
        if num_results == results_start:
            
            if page_num < num_pages:
                page_num += 1
                search_url = f"https://www.inaturalist.org/observations?page={page_num}&place_id=any&subview=table&taxon_id={query}"
                print('\nLoading next page...\n')
                wd.get(search_url)
                time.sleep(sleep_between_interactions)  
                
                results_start = 0 # the new thumbnail list from next page will be searched from 0 again
                
                # The list of page links at the bottom can only show 10 pages at once.
                # If there are more than 10 pages, the links to the new ones are only shown as you
                # progress through the links. Therefore, whenever you turn a page, check
                # whether there are actually more pages than initially visible
                last_page_link = wd.find_elements(By.XPATH, "//li[@class='pagination-page ng-scope']/a")[-1]
                num_pages = int( last_page_link.get_attribute('text') )
                
                continue
            
            else:
                print('No more images left!')
                break
                     
        # Iterate over (new) images in current thumbnail list
        for img in thumb[results_start : num_results]:
            
            # URLs are stored as 'background-image' inside style-attribute
            style_att = img.get_attribute('style')
            
            # Slice the string down to the url
            ind_start, ind_end = style_att.find('url') + 5, style_att.find(')') - 1
            url = style_att[ind_start : ind_end] 
            print(url)
            
            image_urls.add(url)                   
            image_count = len(image_urls)
            if image_count >= max_links_to_fetch:
                reached_max = True
                break
        
        if not reached_max:
            print(f"Found: {image_count} image links. Looking for more...\n")       
            # Move the result startpoint further down
            results_start = num_results
        
    print(f"Found: {image_count} image links, done!\n")
    return image_urls


def persist_image(folder_path:str, url:str):
    """Save image from url to a specified folder.
    
    :param folder_path: Path to the folder where the images are saved.
    :type folder_path: str
    :param url: Address of the image to download.
    :type url: str
    """
    
    try:
        # Get html code of the image
        headers = {'User-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0)'}
        image_content = requests.get(url, headers=headers).content
        
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")    
        
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path, hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality = 95)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")
        
        
def search_and_download(search_term:str, target_path = './', number_images = 10):
    """Launch query, store urls and download images.
    
    :param search_term: Image ID used as query in the url.
    :type search_term: str
    :param target_path: Path to the folder where the images should be downloaded. Defaults to current folder.
    :type target_path: str, optional
    :param number_images: Number of images to be downloaded. Defaults to 10.
    :type number_images: int, optional
    """
    
    # Create downloading path, if not already existant
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # Store image urls
    with webdriver.Firefox(service = Service(GeckoDriverManager().install())) as wd:
        res = fetch_image_urls(search_term, number_images, wd = wd)
        
    # Download images
    for elem in res:
        persist_image(target_path, elem)
        
        
  
if __name__ == '__main__':
    
    # Test server: a browser window should open and close immediately
    # from selenium.webdriver.firefox.service import Service
    # service = Service(DRIVER_PATH)
    # service.start()
    # wd = webdriver.Remote(service.service_url)
    # wd.quit()
    
    search_and_download(search_term = '355696',
                        target_path = 'Z:\data\Bees\Andrena_vaga', number_images = 10000)
    
    
     