from selenium import webdriver
from pathlib import Path
import os, shutil
import zipfile
from glob import glob
import time

# empty downloads folder
downloads_path = "/home/lary-research-pc/Downloads"
downloads = os.listdir(downloads_path)

if len(downloads) != 0:
    print("Non-empty /Downloads/ folder")
    for dl in downloads:
        print("\t Removing {}".format(dl))
        os.remove(os.path.join(downloads_path, dl))
    print("\n")



def is_download_finished(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False
    # firefox_temp_file = sorted(Path(temp_folder).glob('*.part'))
    # chrome_temp_file = sorted(Path(temp_folder).glob('*.crdownload'))
    # downloaded_files = sorted(Path(temp_folder).glob('*.*'))
    # if (len(firefox_temp_file) == 0) and \
    #    (len(chrome_temp_file) == 0) and \
    #    (len(downloaded_files) >= 1):
    #     return True
    # else:
    #     return False




# states = {"27": "Minnesota"}

states = {"01": "Alabama",
          "02": "Alaska ",
          "04": "Arizona",
          "05": "Arkansas",
          "06": "California",
          "08": "Colorado",
          "09": "Connecticut",
          "10": "Delaware",
          "11": "District of Columbia",
          "12": "Florida",
          "13": "Georgia",
          "15": "Hawaii",
          "16": "Idaho",
          "17": "Illinois",
          "18": "Indiana",
          "19": "Iowa",
          "20": "Kansas",
          "21": "Kentucky",
          "22": "Louisiana",
          "23": "Maine",
          "24": "Maryland",
          "25": "Massachusetts",
          "26": "Michigan",
          "27": "Minnesota",
          "28": "Mississippi",
          "29": "Missouri",
          "30": "Montana",
          "31": "Nebraska",
          "32": "Nevada",
          "33": "New Hampshire",
          "34": "New Jersey",
          "35": "New Mexico",
          "36": "New York",
          "37": "North Carolina",
          "38": "North Dakota",
          "39": "Ohio",
          "40": "Oklahoma",
          "41": "Oregon",
          "42": "Pennsylvania",
          "72": "Puerto Rico",
          "44": "Rhode Island",
          "45": "South Carolina",
          "46": "South Dakota",
          "47": "Tennessee",
          "48": "Texas",
          "49": "Utah",
          "50": "Vermont",
          "51": "Virginia",
          "53": "Washington",
          "54": "West Virginia",
          "55": "Wisconsin",
          "56": "Wyoming"
}



# setup web driver
browser = webdriver.Chrome('/home/lary-research-pc/chromedriver')

# open browser and navigate to census page
url = "https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2010&layergroup=Census+Tracts"
browser.get(url)

# grab the necessary ui elements
state_selection_bar_10 = browser.find_element_by_id('fips_81')
xpath = '//*[@id="div81"]/input'
download_button = browser.find_element_by_xpath(xpath)
if download_button.is_displayed():
    print("Download button located successfully!")

path_to_data = "/home/lary-research-pc/john-waczak/gitrepos/census-data/data/decennial_2010/tracts/"

for key, value in states.items():
    print("Working on {}".format(value))
    state_selection_bar_10.send_keys(value)
    download_button.click()

    # i = 0
    # while i < 20:
    #     print(is_download_finished(os.path.join(downloads_path, 'tl_2010_{}_tract10.zip'.format(key))))
    #     print("sleeping...")
    #     time.sleep(5)

    new_zipfile = os.path.join(downloads_path, 'tl_2010_{}_tract10.zip'.format(key))
    while not is_download_finished(new_zipfile):
        print("\tdownloading {}...".format(value))
        time.sleep(1)

    outpath = os.path.join(path_to_data, value)
    if not os.path.exists(outpath):
        print('Making new directory at: {}'.format(outpath))
        os.makedirs(outpath)

    with zipfile.ZipFile(new_zipfile, 'r') as zip_ref:
        zip_ref.extractall(outpath)



# # test download
# print("All finished!")
