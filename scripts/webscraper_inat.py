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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from PIL import Image

# Webdriver for Firefox downloaded with GeckoDriverManager. For other browsers, search for the specific webdriver service
# https://github.com/mozilla/geckodriver/releases
DRIVER_PATH = r'C:\Users\Teo\.wdm\drivers\geckodriver\win64\v0.30.0\geckodriver.exe'


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep:int = 10):
    """Find and store the image urls.
    
    :param query: Species ID to complete the url.
    :type query: str
    :param max_links_to_fetch: Maximum number of urls to download.
    :type max_links_to_fetch: int
    :param wd: Webdriver specific for your browser.
    :type wd: selenium.webdriver
    :param sleep: Number of seconds to wait until next iteration. Defaults to 10 seconds.
    :type sleep: int, optional
    :return: Set of tuples (urls, hrefID_listID)
    """
    
    # Enable infinite scrolling
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep)  
         
    # Build the search query 
    # Only load fotos marked with Research Grade and CC-BY-NC copyright
    page_num = 12 # current page number
    if page_num == 1:
        search_url = f"https://www.inaturalist.org/observations?photo_license=CC-BY-NC&place_id=any&quality_grade=research&subview=table&taxon_id={query}"
    else:
        search_url = f"https://www.inaturalist.org/observations?page={page_num}&photo_license=CC-BY-NC&place_id=any&quality_grade=research&subview=table&taxon_id={query}"
    wd.get(search_url)
    time.sleep(sleep)  
    
    image_urls = set() # will contain tuples of urls along with the hrefID and listID within contribution: (url, hrefID_listID)
    # Note: by storing the href and list IDs, each downloaded image can be retraced exactly on the site
    image_count = 0 
    results_start = 0
    reached_max = False
    
    # Get total number of pages 
    try:
        page_links = WebDriverWait(wd, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='pagination-page ng-scope']/a")))                
        num_pages = int( page_links[-1].get_attribute('text') ) 
    except:
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
                search_url = f"https://www.inaturalist.org/observations?page={page_num}&photo_license=CC-BY-NC&place_id=any&quality_grade=research&subview=table&taxon_id={query}" 
                print('\nLoading next page...\n')
                wd.get(search_url)
                
                results_start = 0 # the new thumbnail list on the next page will be scanned from 0 again
                
                # The list of page links at the bottom can only show 10 pages at once.
                # If there are more than 10 pages, the links to the new ones are only shown as you
                # progress through the links. Therefore, whenever you turn a page, check
                # whether there are actually more pages than initially visible.
                try:
                    page_links = WebDriverWait(wd, 30).until(EC.presence_of_all_elements_located((By.XPATH, "//li[@class='pagination-page ng-scope']/a")))                
                    num_pages = int( page_links[-1].get_attribute('text') )              
                    continue
                
                except Exception as e:
                    print(f"ERROR - Could not find page links on page {page_num}. Returning urls stored until now - {e}")  
                    break
            
            else:
                print('No more images left!')
                break
                     
        # Iterate over (new) images in current thumbnail list
        for img in thumb[results_start : num_results]:
            
            href_att = img.get_attribute('href')
            href_id = href_att[href_att.rfind('/') + 1 : ] # drop string 'observations'
            
            # If no image counter is shown, then there is only one image in the contribution
            # -> Download its url directly from the table
            # If there is a counter visible, the contribution has multiple images
            # -> Click on it and get all available urls
            if img.find_elements(By.CSS_SELECTOR, 'span.ng-hide'):
                
                # URLs are stored as 'background-image' inside the style-attribute
                style_att = img.get_attribute('style')
                 
                # Slice the string down to the url
                ind_start, ind_end = style_att.find('url') + 5, style_att.find(')') - 1
                url = style_att[ind_start : ind_end] 
                image_urls.add( (url, str(href_id) + '_1') ) # for consistency, images in one-element-lists get listID = 1
                 
            else:                
                
                # Open new tab and get all available image urls
                href_urls = get_urls_from_href(href_id, wd)
                
                image_urls.update(href_urls) # Note: use update when adding elements of a set/list to a set                
            
            # Check if maximum number of images was reached
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


def get_urls_from_href(href_id:int, wd:webdriver, sleep:int = 5):
    """Find all image urls from a given observation page index.
    
    :param href_id: Observation page index. Leads to the page containing all images of a single person's contribution.
    :type href_id: int
    :param wd: Webdriver specific for your browser.
    :type wd: selenium.webdriver
    :param sleep: Number of seconds to wait until next iteration. Defaults to 5 seconds.
    :type sleep: int, optional
    :return: Set of tuples (urls, hrefID_listID)
    """
    
    search_url = f"https://www.inaturalist.org/observations/{href_id}"
    wd.execute_script("window.open('" + search_url +"');") # open new tab
    wd.switch_to.window(wd.window_handles[1]) # focus on the new tab
    time.sleep(sleep) 
    
    image_urls = set()    
    img_list = wd.find_elements(By.XPATH, "//div[@class='image-gallery-thumbnail-inner']/img")   
    for i in range(len(img_list)):
        src = img_list[i].get_attribute('src')
        large_url = src.replace('square', 'large') # store the image in original dimensions, not thumbnail dims
        image_urls.add( (large_url, str(href_id) + '_' + str(i+1)) )
        
    wd.execute_script("window.close('" + search_url +"');") # close new tab
    wd.switch_to.window(wd.window_handles[0]) # focus on original tab
    
    return image_urls
    

def persist_image(folder_path:str, url_id:tuple):
    """Save image from url to a specified folder.
    
    :param folder_path: Path to the folder where the images are saved.
    :type folder_path: str
    :param url_id: Address of the image to download and hrefID_listID
    :type url: tuple
    """
    
    url, img_id = url_id
    
    try:
        # Get html code of the image
        headers = {'User-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0)'}
        image_content = requests.get(url, headers=headers).content
        
    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")    
        
    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        
        spec = folder_path.split('\\')[-1]
        file_path = os.path.join(folder_path, spec + '_' + img_id + '.jpg')
                
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
    # Note: On the first run, install driver with GeckoDriverManager().install() instead of DRIVER_PATH
    with webdriver.Firefox(service = Service(DRIVER_PATH)) as wd:
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
    
    ind_spec = [
        #(60579, 'Andrena_fulva'),
        #(62453, 'Anthidium_manicatum'),
        #(453068, 'Bombus_cryptarum'),
        #(121989, 'Bombus_hortorum'),
        #(61803, 'Bombus_hypnorum'),
        #(57619, 'Bombus_lapidarius'),
        #(61856, 'Bombus_lucorum'),
        #(424468, 'Bombus_magnus'),
        #(55637, 'Bombus_pascuorum'),
        #(124910, 'Bombus_pratorum'),
        #(123657, 'Bombus_sylvarum'),
        #(746682, 'Dasypoda_hirtipes'),
        #(415589, 'Halictus_scabiosae'),
        #(207574, 'Osmia_bicolor'),
        #(876599, 'Osmia_bicornis'),
        #(126630, 'Osmia_cornuta'),
        #(154661, 'Sphecodes_albilabris'),
        (124145, 'Xylocopa_violacea')
    ]
    
    for ind, spec in ind_spec:
        
        print('\n******** ' + spec + ' ********\n')
        search_and_download(search_term = str(ind),
                            target_path = 'Z:\data\Bees\\' + spec, 
                            #target_path = 'C:\\Users\Teo\Documents\KInsekten\data\Bees\\' + spec,
                            number_images = 5000)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
     