import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

log_file = 'google_play_sdk_index_guidance_links_' +\
           f'{datetime.now().strftime("%B").lower()}_{datetime.now().day}.csv'
with open(log_file, 'w') as f:
    f.write('')

category_base = 'https://play.google.com/sdks/categories/'
target_urls = {
    'advertising_and_monetization': category_base+'ads',
    'analytics': category_base+'analytics',
    'data_management': category_base+'data-management',
    'location': category_base+'location',
    'merketing_and_engagement': category_base+'marketing-and-engagement',
    'payments': category_base+'payments',
    'social': category_base+'social',
    'user_authentication': category_base+'user-authentication',
    'user_support': category_base+'user-support',
}

def init_driver():
    # return webdriver.Firefox(executable_path='./geckodriver', log_path='./geckodriver.log', firefox_profile=webdriver.FirefoxProfile())
    driver = webdriver.Firefox(executable_path='./geckodriver')
    # driver.set_window_size(1600, 1000)
    return driver

def get_app_buttons_in_category_page(driver):
    elements = driver.find_elements(By.XPATH,
                                    "//*[text()='arrow_right_alt']")
    assert len(elements) % 2 == 0
    return [ elements[i*2+1] for i in range(int(len(elements)/2)) ]

def get_app_name_in_app_page(driver):
    element = driver.find_element(By.XPATH,
                                  # "/html/body/div[1]/root/console-chrome/div/div/div/div/div[1]/page-router-outlet/page-wrapper/div/sdk-details-page/console-page-header/div/div/div/console-header/div/div[2]/div[1]/div[1]/div/div/simple-html/span")
                                  "/html/body/div[1]/root/console-chrome/div/div/div/div/div[1]/page-router-outlet/page-wrapper/div/sdk-details-page/console-page-header/div/div/div/console-header/div/div[2]/div[1]/div[1]/div[1]/div/div/simple-html/span")
    return element.text

def detect_guidance_in_app_page(driver):
    try:
        element = driver.find_element(By.XPATH,
                                      "//*[text()='View guidance']")
        print(f'guidance: {element}')
        guidance_url = element.get_attribute("href")
        print(f'{guidance_url = }')
        return guidance_url
    except NoSuchElementException:
        print('guidance not found')
        return ''

# def get_maven_id_in_app_page(driver):
#     elements = driver.find_elements(By.XPATH,
#                                     "//*[@debug-id='label-container']/following-sibling::div")
#     return elements[0].text
# 
# def get_maven_repository_in_app_page(driver):
#     elements = driver.find_elements(By.XPATH,
#                                     "//*[@debug-id='label-container']/following-sibling::div")
#     return elements[1].text

def get_maven_info_in_app_page(driver):
    try:
        element = driver.find_element(By.XPATH,
                                      "//*[text()='View more']")
        print(f'view more: {element}')
        element.click()
        time.sleep(2)
    except NoSuchElementException:
        pass

    element = driver.find_element(By.XPATH,
                                  "//sdk-maven-information-card")
    # print(f'maven info = {element.text}')

    maven_id = []
    maven_repository = []
    current = None
    for line in element.text.split('\n'):
        if (line in ['Maven ID', 'Maven IDs']):
            current = maven_id
        elif (line == 'Maven repository'):
            current = maven_repository
        elif (line == 'Data safety section guidance'):
            break
        elif (current is not None and
              line not in ['Hide', 'expand_less']
             ):
            current.append(line)
    return f'"{",".join(maven_id)}"', f'"{",".join(maven_repository)}"'

def crawl_one_category(driver, category_name, category_url):
    driver.get(category_url)
    time.sleep(3)

    app_buttons = get_app_buttons_in_category_page(driver)
    print(f'{len(app_buttons) = }')

    app_num = len(app_buttons)
    app_with_guidance_num = 0
    results = ''

    for i in range(app_num):
        print(f'{i+1} / {app_num}')
        app_buttons = get_app_buttons_in_category_page(driver)
        app_buttons[i].click()
        time.sleep(3)
        # App Name
        app_name = get_app_name_in_app_page(driver)
        print(f'{app_name = }')
        # Guidance URL
        guidance_url = detect_guidance_in_app_page(driver)
        if (guidance_url): app_with_guidance_num += 1
        # # Maven ID
        # maven_id = get_maven_id_in_app_page(driver)
        # print(f'{maven_id = }')
        # # Maven Repository
        # maven_repository = get_maven_repository_in_app_page(driver)
        # print(f'{maven_repository = }')
        # Maven Info
        maven_id, maven_repository = get_maven_info_in_app_page(driver)
        print(f'{maven_id = }')
        print(f'{maven_repository = }')

        results += f'{category_name},{app_name},{guidance_url},{maven_id},{maven_repository}\n'

        driver.execute_script('window.history.go(-1)')

        time.sleep(3)

    # Write result to the file
    with open(log_file, 'a') as f:
        f.write(f'{category_name},{app_num},{app_with_guidance_num},,\n')
        f.write(results)
        f.write('\n')


if __name__ == '__main__':
    print('Starting')
    driver = init_driver()

    for i, (category_name, category_url) in enumerate(target_urls.items()):
        print(f'{i+1} / {len(target_urls.keys())} {category_name}')
        print(f'{category_url = }')

        crawl_one_category(driver, category_name, category_url)

    input('Hit Enter to continue')

    print('Done')
