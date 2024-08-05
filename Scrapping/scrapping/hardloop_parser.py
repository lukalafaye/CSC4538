from bs4 import BeautifulSoup
import urllib.request
from pprint import pprint


url = "https://www.hardloop.fr/produit/18734-patagonia-better-sweater-1-4-zip-polaire-homme"

def get_info(url_product):
    fp = urllib.request.urlopen(url_product)
    bytes_content = fp.read()
    html_content = bytes_content.decode("utf8")
    soup = BeautifulSoup(html_content, "html.parser")

    product_info = {"brand": None, "name": None, "price": None, "color": None, "description": None, "technical_specs": None}

    brand = soup.find("a", {"class" : "productInfos_manufacturer__jIf80"})
    brand = brand.contents[0]
    product_info["brand"] = brand 

    name = soup.find("h1", {"class": "productInfos_productName__qs2zg"})
    name = name.contents[-1].string
    product_info["name"] = name 

    price = soup.find("span", {"class" : "productInfos_normalPrice__USOo4"})
    price = price.contents[0].get_text(strip=True)
    price = price.replace('€', '').replace(',', '.').strip()
    price = float(price)
    product_info["price"] = price 

    color = soup.find("label", {"class" : "productInfos_colorTitle__9dw_l"})
    color = color.contents[-1].string
    product_info["color"] = color 

    description = soup.find("div", {"class": "productDescription_descContent__UgocM"})
    description = description.contents[0]
    product_info["description"] = description.get_text(strip=True)

    specs_div = soup.find('div', {'class': 'technicalTable_techColumn__zCW_r'})
    specs = specs_div.find_all('div', {'class': 'technicalTable_techElement__F1l9w'})

    technical_specs = {}
    for spec in specs:
        title = spec.find('span', {'class': 'technicalTable_techTitle__g1Isp'}).text.strip()
        value = spec.find_all('span')[1].text.strip()
        technical_specs[title] = value
    
    product_info["technical_specs"] = technical_specs

    return product_info
   

# get_info(url)

def get_product_pages(url):
    fp = urllib.request.urlopen(url)
    bytes_content = fp.read()
    html_content = bytes_content.decode("utf8")
    with open("test.html", "w") as f:
        f.write(html_content)

    soup = BeautifulSoup(html_content, "html.parser")

    product_pages = []
    products_pages_a = soup.find_all("a", {"class": "menuBottomDesktop_catLinks__pCDGv "})
    print(products_pages_a)

    for product_page in products_pages_a:
        product_pages.append(product_page["href"])

    pprint(product_pages)
    return product_pages

# get_product_pages("https://www.hardloop.fr/produit/18734-patagonia-better-sweater-1-4-zip-polaire-homme")

def get_all_product_page(url_page):
    
    soup = BeautifulSoup(html_content, "html.parser")

    products = []

    products_a = soup.find_all("a", {"class": "productCard_itemCard__Jdruu productCard_cardNoBackground__OWx_Y"})

    for product in products_a:
        products.append(product["href"])

    return products

# get_all_product_page("https://www.hardloop.fr/produit/18734-patagonia-better-sweater-1-4-zip-polaire-homme")

def request(url):
    headers = {"User-Agent" : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"}
    req = urllib.request.Request(url, None, headers)
    fp = urllib.request.urlopen(req)
    bytes_content = fp.read()
    html_content = bytes_content.decode("utf8")

    with open("test.html", "w") as f:
        f.write(html_content)

    return html_content

request("https://www.hardloop.fr/produit/18734-patagonia-better-sweater-1-4-zip-polaire-homme")