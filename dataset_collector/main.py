from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium import webdriver

base_url = 'https://pub.dev/'
package_page_link_list = []
github_link_list = []
lib_link_list = []
dart_file_link_list = []


def github_folder_traverse(page_link):
    browser.get(page_link)
    links = browser.find_elements_by_css_selector(
        '.Details .css-truncate.css-truncate-target.d-block.width-fit a.Link--primary')
    temp_links = []

    for link in links:
        url = link.get_attribute("href")
        if url.endswith('.dart'):
            dart_file_link_list.append(url)
        else:
            temp_links.append(url)

    for link in temp_links:
        github_folder_traverse(link)

    return


browser = webdriver.Chrome(executable_path='./chromedriver')

for i in range(1, 2):  # TODO: Change back to 11
    browser.get(f'{base_url}packages?sort=popularity&page={i}')
    for package in browser.find_elements_by_css_selector(".packages-title a"):
        package_page_link_list.append(package.get_attribute("href"))

for package_page in package_page_link_list:
    browser.get(package_page)
    github_link_list.append(browser.find_element_by_link_text("Repository (GitHub)").get_attribute("href"))

for github_page in github_link_list:
    browser.get(github_page)
    try:
        lib_link_list.append(browser.find_element_by_link_text("lib").get_attribute("href"))
    except (NoSuchElementException, StaleElementReferenceException):
        pass

for lib_link in lib_link_list:
    github_folder_traverse(lib_link)

print(dart_file_link_list)
#TODO: Access URL, then download .dart file and store as .txt, also rename it with url name directly before blob/master

browser.close()
