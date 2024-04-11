import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox import service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

guidance_urls = open('guidance_page_urls_october_4.txt', 'r').read().rstrip('\n').split('\n')
result_dir = 'guidance_pages_annotated/'
SKIP_URLS = [ ]

def init_driver():
    # return webdriver.Firefox(executable_path='./geckodriver', log_path='./geckodriver.log', firefox_profile=webdriver.FirefoxProfile())
    firefox_service = service.Service(executable_path='./geckodriver')
    driver = webdriver.Firefox(service=firefox_service)
    return driver

def get_body_text(driver):
    element = driver.find_element(By.XPATH,
                                  "/html/body")
    print(f'{len(element.text) = }')

    return element.text

def get_source(driver):
    html = driver.page_source
    print(f'{len(html) = }')

    return html

def print_page(driver, output_path):
    driver.save_full_page_screenshot(output_path)

def crawl_one_url(driver, guidance_id, guidance_url):
    driver.get(guidance_url)
    time.sleep(6)

    guidance_text = get_body_text(driver)
    guidance_source = get_source(driver)
    with open(f'{result_dir}{guidance_id}.txt', 'w') as f:
        f.write(guidance_text)
    with open(f'{result_dir}{guidance_id}.html', 'w') as f:
        f.write(guidance_source)

    print_page(driver, f'{result_dir}{guidance_id}.png')

    time.sleep(1)

if __name__ == '__main__':
    print('Starting')
    driver = init_driver()

    for i in range(1, len(guidance_urls)+1):
        if (i in SKIP_URLS): continue

        guidance_url = guidance_urls[i-1]

        print(f'{i} / {len(guidance_urls)} {guidance_url}')

        crawl_one_url(driver, i, guidance_url)

    input('Hit Enter to continue')

    print('Done')
