import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlencode

service = Service(ChromeDriverManager().install())

async def ext_page_source(
    url,
    driver_params=None,
    driver_headers=None,
    driver_url=False,
    driver_pic_name=False,
    driver_source=True,
    driver_sleep=8,
):
    try:
        if driver_params:
            url = f"{url}?{urlencode(driver_params)}"

        default_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        }

        if driver_headers:
            default_headers.update(driver_headers)

        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")

        for key, value in default_headers.items():
            options.add_argument(f"--header={key}:{value}")

        driver = webdriver.Chrome(service=service, options=options)
        driver.get(url)
        await asyncio.sleep(driver_sleep)  # Use asyncio.sleep for async
        all = []
        cookies = ""
        if cookies:
            cookies = [{"name": "ndus", "value": "lol"}]
            for cookie in cookies:
                driver.add_cookie(cookie)
        if driver_pic_name:
            driver.save_screenshot(driver_pic_name)
        if driver_url:
            page_url = driver.current_url
            all.append(page_url)
        if driver_source:
            page_source = driver.page_source
            all.append(page_source)
        if len(all) == 1:
            return all[0]
        else:
            return all
    except Exception as e:
        return f"Failed To Bypass \n\n{e.__class__.__name__}"
    finally:
        driver.quit()

async def flipkart(name_of_product):
    all_info = {}
    prices_list = []
    source_code = await ext_page_source(f"https://www.flipkart.com/search?q={name_of_product.replace(' ', '%20')}")

    soups = BeautifulSoup(source_code, "html.parser").find_all("div", {"class":"row"})

    for soup in soups:
        try:
            product_link = f'https://www.flipkart.com{soup.find_previous("a").get("href")}'
            product_info = soup.find_next('div', {'class':'col col-7-12'}).text
            product_info = product_info[:product_info.find(")")+1:]
            if all(name in product_info.casefold() for name in name_of_product.split()):
                main_part_source = soup.find_next('div', {'class':'col'}).find_next('div', {'class':'col-5-12'})
                main_part = BeautifulSoup(str(main_part_source), "html.parser")
                present_price = None
                original_price = None
                discount = main_part.find("span").text
                for ele in main_part.find_all("div"):
                    if "₹" in ele.text:
                        if not present_price:
                            present_price = ele.text.split("₹")[1].replace(",","")
                            original_price = ele.find_next("div").text.replace(",","").replace(discount, " ").replace(f"₹{present_price}", " ").split("₹")[1].split()[0]
                            break
                if int(present_price) not in all_info:
                    prices_list.append(int(present_price))
                    all_info[int(present_price)] = []
                all_info[int(present_price)].append({"Product_Link": product_link,"product_info": product_info, "present_price": present_price, "original_price": original_price, "discount": discount})
        except: pass

    if not all_info and not prices_list:
        soups = BeautifulSoup(source_code, "html.parser").find_all("div", {"class":"col-12-12"})
        for soup in soups:
            all_temp_links = soup.find_all("a")
            for a in all_temp_links:
                if a.get("title"):
                    product_info = a.get("title")
                    try:
                        all_things = a.find_next("a").text
                        if "₹" in all_things:
                            product_link = f'https://www.flipkart.com{a.find_next("a").get("href")}'
                            discount = a.find_next("a").find("span").text
                            present_price = None
                            original_price = None
                            present_price = int(all_things.split("₹")[1].replace(",",""))
                            original_price = all_things.replace(",","").replace(discount, " ").replace(f"₹{present_price}", " ").split("₹")[1].split()[0]
                            if int(present_price) not in all_info:
                                prices_list.append(int(present_price))
                                all_info[int(present_price)] = []
                            all_info[int(present_price)].append({"Product_Link": product_link,"product_info": product_info, "present_price": present_price, "original_price": original_price, "discount": discount})
                    except: pass
    return all_info, prices_list
