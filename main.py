import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from constants import checkFolderExists, createFolder, getCurrentDirectory
from downloadFile import downloadFile
from datetime import datetime

from writeToLog import writeToLog


today = datetime.strftime(datetime.now().date(), "%Y-%d-%m")
valid_file_extension = ["pdf", "doc", "docx", "jpg",
                        "jpeg", "png", "gif", "totm", "xlsx", "xlsv", "csv", "html", "mp3", "mp4", "ppt", "pptx", "psd", "zip", "rar", "txt", "tiff", "xls"]


url = "https://solargroup.com/"

if not checkFolderExists("Logs", getCurrentDirectory()):
    createFolder("Logs", getCurrentDirectory())

if not checkFolderExists(today, os.path.join(getCurrentDirectory(), "Logs")):
    createFolder(today, os.path.join(getCurrentDirectory(), "Logs"))

logs_date_path = os.path.join(os.path.join(
    getCurrentDirectory(), "Logs"), today)
total_run = 0

writeToLog(logs_date_path,
           "------------------------------------------------------\n")
writeToLog(logs_date_path,
           "------------------------------------------------------\n")
writeToLog(logs_date_path, "                Log: " + today)
writeToLog(logs_date_path,
           "------------------------------------------------------\n")
writeToLog(logs_date_path,
           "------------------------------------------------------\n")


writeToLog(logs_date_path, "Opening Browser...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, slow_mo=10)

    page = browser.new_page()

    writeToLog(logs_date_path, "Going to URL:: " + url + " ...")

    page.goto(url)
    page.wait_for_timeout(3000)

    '''
        Working On Home Page
    '''

    writeToLog(logs_date_path, "URL is opened...")
    # Getting Menu On Hover
    page.mouse.move(0, 0)
    writeToLog(logs_date_path, "Hovering to the top for menu...")
    page.wait_for_timeout(3000)

    page.hover("#my-navbar")
    writeToLog(logs_date_path, "Clicking on Nav menu...")
    page.click("#my-navbar > div.ham > img")
    writeToLog(logs_date_path, "Clicked on the Nav Menu...")

    # Locate Main Menu
    # menu_list = page.locator("#menu-main-menu")
    html = page.inner_html("div.my-sidenav")

    soup = BeautifulSoup(html, 'html.parser')

    writeToLog(logs_date_path, "Parsing all the UL present in navbar...")
    # Find the ul tag for all menus
    ul_tag = soup.find("ul")
    # Find all main menus
    li_tags = ul_tag.find_all("li")

    # To store all the main menus
    writeToLog(logs_date_path, "Storing All menus list in navbar...")
    list_of_main_menus = []
    for option in li_tags:
        list_of_main_menus.append(option.text)

    # Filtering the sub-menu
    list_of_main_menus = [
        i for i in list_of_main_menus if list_of_main_menus.count(i) == 1]

    # Re-Filtering the sub-menu
    for i in list_of_main_menus:
        splitted = i.split("\n")
        if len(splitted) >= 2:
            splitted.remove('')
            list_of_main_menus += splitted
            list_of_main_menus.remove(i)
        else:
            pass

    # Removing Duplicate One
    list_of_main_menus = [
        i for i in list_of_main_menus if list_of_main_menus.count(i) == 1]

    cwd = getCurrentDirectory()

    for i in list_of_main_menus:
        writeToLog(logs_date_path, "                 On " + i + " Page")
        writeToLog(logs_date_path,
                   "-------------------------------------------------------\n")
        # Create Folder with Main Menu Name
        if i != "Company" and i != "Products":
            if i is not None:
                writeToLog(logs_date_path, "Checking " +
                           i + " Folder's availability...")
                if not checkFolderExists(i, cwd):
                    writeToLog(logs_date_path, "Creating " + i + " Folder...")
                    createFolder(i, cwd)
                current_menu_directory = os.path.join(cwd, i)

                writeToLog(logs_date_path, "Checking " +
                           today + " Folder's availability...")
                if not checkFolderExists(today, current_menu_directory):
                    writeToLog(logs_date_path,
                               "Creating Date Folder in " + i + " ...")
                    date_menu_directory = createFolder(
                        today, current_menu_directory)
                date_menu_directory = os.path.join(
                    current_menu_directory, today)
            else:
                continue

            writeToLog(logs_date_path,
                       "Checking Screenshot Folder's availability...")
            if not checkFolderExists("Screenshots", date_menu_directory):
                writeToLog(logs_date_path,
                           "Creating Screenshot Folder is there...")
                createFolder("Screenshots", date_menu_directory)
            screenshot_directory = os.path.join(
                date_menu_directory, "Screenshots")

            # Locate the Main Menu
            home_page_locator = page.locator(
                "#menu-main-menu .menu-item > a", has_text=i)

            # Click the Menu
            home_page_locator.click()
            page.wait_for_timeout(5000)

            writeToLog(logs_date_path, "Taking Landing Section Screenshot...")
            page.screenshot(path=os.path.join(
                screenshot_directory, "Landing_page.png"))

            writeToLog(logs_date_path, "Scrolling landing section...")
            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)
            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)
            page.keyboard.press("End")
            page.wait_for_timeout(3000)
            writeToLog(logs_date_path, "Took Landing Section Screenshot...")

            writeToLog(logs_date_path, "Taking Full Screen Screenshot...")
            page.screenshot(path=os.path.join(
                screenshot_directory, "Full_page.png"), full_page=True)
            writeToLog(logs_date_path, "Took Full Page Screenshot...")

            # if i == "Investor Relations":
            #     if not checkFolderExists("Files", date_menu_directory):
            #         createFolder("Files", date_menu_directory)
            #     file_directory = os.path.join(date_menu_directory, "Files")

            #     # Select the Main container for PDFs
            #     page.is_visible("#section6 > ul")
            #     html = page.inner_html("#section6 > ul")

            #     soup = BeautifulSoup(html, 'html.parser')
            #     writeToLog(logs_date_path,
            #                "Fetching all file links in " + i + " Page...")
            #     all_tabs_li = soup.find_all("a")

            #     for i in all_tabs_li:
            #         writeToLog(logs_date_path, "Downloading " + str(i['href']))
            #         if i['href'] is not None and i['href'] != "#" and i['href'] != "":
            #             string = i['href']
            #             print(string)
            #             string = string.split(".")[-1]

            #             if string.lower() in valid_file_extension:
            #                 downloaded_file_name = downloadFile(url=i['href'],
            #                                                     download_directory=file_directory)
            #                 writeToLog(logs_date_path, "Downloaded File " +
            #                            downloaded_file_name)
            #             else:
            #                 print("Not a File URL")
            #                 writeToLog(logs_date_path, "Invalid URL")
            #         else:
            #             print("Invalid URL")
            #             writeToLog(logs_date_path, "Invalid URL")


            # if i == "Sustainability":
            #     createFolder(date_menu_directory, "Files")
            #     file_directory = os.path.join(date_menu_directory, "Files")

            #     # Select the Main container for PDFs
            #     page.is_visible(
            #         "#pagerock2 > div.pageCenter > div.pageContent > div.layer.main.mainCenter > div.solar-container > div.sustain-cover-main-pdf-sec")

            #     html = page.inner_html(
            #         "#pagerock2 > div.pageCenter > div.pageContent > div.layer.main.mainCenter > div.solar-container > div.sustain-cover-main-pdf-sec")

            #     soup = BeautifulSoup(html, 'html.parser')
            #     writeToLog(logs_date_path,
            #                "Fetching all file links in " + i + " Page...")
            #     all_category_download_div = soup.find_all("a")

            #     for i in all_category_download_div:
            #         writeToLog(logs_date_path, "Downloading " + str(i['href']))
            #         if i['href'] is not None and i['href'] != "#" and i['href'] != "":
            #             string = i['href']
            #             string = str.split(".")[-1]

            #             if string.lower() in valid_file_extension:
            #                 downloaded_file_name = downloadFile(url=i['href'],
            #                                                     download_directory=file_directory)
            #                 writeToLog(logs_date_path, "Downloaded File " +
            #                            downloaded_file_name)
            #             else:
            #                 print("Not a File URL")
            #                 writeToLog(logs_date_path, "Invalid URL")
            #         else:
            #             print("Invalid URL")
            #             writeToLog(logs_date_path, "Invalid URL")

            writeToLog(logs_date_path, "Hover to the Nav menu")
            # Move to Top to get the Menu Icon
            page.mouse.move(0, 0)
            page.wait_for_timeout(3000)

            # Hover the menu bar
            page.hover("#my-navbar")
            page.click("#my-navbar > div.ham > img")
        else:
            if i is not None:
                writeToLog(logs_date_path, "Checking " +
                           i + " Folder's availability...")
                if not checkFolderExists(i, cwd):
                    writeToLog(logs_date_path, "Creating " + i + " Folder...")
                    createFolder(i, cwd)
                current_menu_directory = os.path.join(cwd, i)

                writeToLog(logs_date_path, "Checking " +
                           today + " Folder's availability...")
                if not checkFolderExists(today, current_menu_directory):
                    writeToLog(logs_date_path,
                               "Creating Date Folder in " + i + " ...")
                    date_menu_directory = createFolder(
                        today, current_menu_directory)
                date_menu_directory = os.path.join(
                    current_menu_directory, today)
            else:
                continue
            
            
            if i == "Company":
                html = page.inner_html("#menu-item-401 > ul")

                soup = BeautifulSoup(html, 'html.parser')

                writeToLog(logs_date_path, "Parsing all the UL present in "+ str(i) +"...")
                # Find the ul tag for all menus
                li_tags = soup.find_all("li")

                # To store all the main menus
                writeToLog(logs_date_path, "Storing All menus list in navbar...")
                list_of_main_menus = []
                for option in li_tags:
                    list_of_main_menus.append(option.text)
                
                print(list_of_main_menus)

                cwd = date_menu_directory

                for inner in list_of_main_menus:
                    writeToLog(logs_date_path, "                 On " + inner + " Page")
                    writeToLog(logs_date_path,
                            "-------------------------------------------------------\n")
                    # Create Folder with Main Menu Name

                    if inner is not None:
                        writeToLog(logs_date_path, "Checking " +
                           inner + " Folder's availability...")
                        if not checkFolderExists(inner, cwd):
                            writeToLog(logs_date_path, "Creating " + inner + " Folder...")
                            createFolder(inner, cwd)
                        inner_current_menu_directory = os.path.join(cwd, inner)
                    else:
                        continue

                    writeToLog(logs_date_path,
                       "Checking Screenshot Folder's availability...")
                    if not checkFolderExists("Screenshots", inner_current_menu_directory):
                        writeToLog(logs_date_path,
                                "Creating Screenshot Folder...")
                        createFolder("Screenshots", inner_current_menu_directory)
                    screenshot_directory = os.path.join(
                        inner_current_menu_directory, "Screenshots")

                    # Locate the Main Menu
                    home_page_locator = page.locator(
                    "#menu-main-menu .menu-item > a", has_text=inner)


            # Click the Menu
            home_page_locator.click()
            page.wait_for_timeout(5000)

            writeToLog(logs_date_path, "Scrolling landing section...")
            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)
            page.keyboard.press("PageDown")
            page.wait_for_timeout(3000)
            page.keyboard.press("End")
            page.wait_for_timeout(3000)
            writeToLog(logs_date_path, "Took Landing Section Screenshot...")

            writeToLog(logs_date_path, "Taking Full Screen Screenshot...")
            page.screenshot(path=os.path.join(
                screenshot_directory, "Full_page.png"), full_page=True)
            writeToLog(logs_date_path, "Took Full Page Screenshot...")


            


            writeToLog(logs_date_path, "Hover to the Nav menu")
            # Move to Top to get the Menu Icon
            page.mouse.move(0, 0)
            page.wait_for_timeout(3000)

            # Hover the menu bar
            page.hover("#my-navbar")
            page.click("#my-navbar > div.ham > img")

