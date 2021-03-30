from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium import webdriver

package_page_link_list = []
github_link_list = []
lib_link_list = []
dart_file_link_list = []
dart_file_raw_text_list = []


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

for i in range(1, 11):
    browser.get(f'https://pub.dev/packages?sort=popularity&page={i}')
    for package in browser.find_elements_by_css_selector(".packages-title a"):
        package_page_link_list.append(package.get_attribute("href"))

for package_page in package_page_link_list:
    browser.get(package_page)
    try:
        github_link = browser.find_element_by_link_text("Repository (GitHub)").get_attribute("href")
        github_link_list.append(github_link)
    except NoSuchElementException:
        pass

for github_page in github_link_list:
    browser.get(github_page)
    try:
        lib_link_list.append(browser.find_element_by_link_text("lib").get_attribute("href"))
    except (NoSuchElementException, StaleElementReferenceException):
        pass

for lib_link in lib_link_list:
    github_folder_traverse(lib_link)

for file_link in dart_file_link_list:
    browser.get(file_link)
    dart_file_raw_text_list.append(browser.find_element_by_id("raw-url").get_attribute("href"))

with open("source_code.txt", "a") as file:
    for source_code_link in dart_file_raw_text_list:
        browser.get(source_code_link)
        file.write(browser.find_element_by_tag_name("pre").text)
        file.write("\n")

browser.close()
