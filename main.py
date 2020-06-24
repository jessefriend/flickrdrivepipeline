from flickr import get_info, get_photos, get_all_info
from download_photos import download_images
import os
import time

#set tags to search through Flickr
all_tags = ['coffee', 'schnitzel', 'wine', 'strudel', 'sachertorte']

def download():
    #initiate downloading and uploading photos for each tag
    for tag in all_tags:

        print('Gettings photos for', tag)
        photos = get_photos(tag)

        print('Getting urls for', tag)
        info = get_info(photos)

        print('Getting coordinates for', tag)
        photo_info = get_all_info(info)

        print('Downloading images for', tag)
        download_images(info[0], tag, photo_info)

if __name__=='__main__':

    start_time = time.time()

    download()

    print('Took', round(time.time() - start_time, 2), 'seconds')
