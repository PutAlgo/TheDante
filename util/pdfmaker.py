from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from weasyprint import HTML
from selenium.webdriver.chrome.service import Service


def make_pdf(urls,meta):
    num = 0
    service = Service(executable_path=r'/usr/bin/chromedriver')
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)

    #names = []
    print(urls)
    html_content = ""
    for url1 in urls:
        #print(url)
        url = url1[0]
        driver.get(url)
        driver.implicitly_wait(10) # wait for the page to load
        driver.refresh()
        html_content += driver.page_source
        num +=1
        if meta['form'] == '10-K':
            meta['form'] = '10k'
        elif meta['form'] == '10-Q':
            meta['form'] = '10Q'
        elif meta['form'] == '8-K':
            meta['form'] = '8K'

        #HTML(string=html_content).write_pdf(f"{meta['tick']}-{url1[1]}-{meta['form']}.pdf")

    HTML(string=html_content).write_pdf(f"{meta['tick']}-{meta['form']}.pdf")
    name = f"{meta['tick']}-{meta['form']}.pdf"

    driver.quit()
    return name
