import os
import re
import shutil
import time
import urllib
import requests
import io
from PIL import Image
from seleniumrequests import Chrome

# noinspection SpellCheckingInspection
IMGFOLDER = os.getcwd() + '/downloaded_images/'
IMAGE_URLS_FILE = os.getcwd() + '/out_10ea.txt'


def main():
    # file_reader = open(IMAGE_URLS_FILE)
    # try:
    #     print(list(file_reader))
    # finally:
    #     file_reader.close()
    # return
    all_links = []

    with open(IMAGE_URLS_FILE, 'r') as reader:
        # Read and print the entire file line by line
        line = reader.readline()
        while line != '':  # The EOF char is an empty string
            # print(line, end='')
            if line[0] != '-':
                all_links.append(line.strip())
            line = reader.readline()
    webdriver = Chrome()
    for url in all_links:
        try:
            filename = re.search(r"(boohoo\/.+\?)", url).group()
            filename = filename[7:-1]
            filename = IMGFOLDER + re.sub("[/%]", "_", filename) + '.jpeg'
            print(filename)
            response = webdriver.request('GET', url)
            file = open(filename, 'wb')
            for chunk in response.iter_content(10000):
                file.write(chunk)
            file.close()
        finally:
            continue
    webdriver.quit()


if __name__ == "__main__":
    main()
