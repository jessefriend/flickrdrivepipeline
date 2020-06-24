import flickrapi
import webbrowser
import xml.etree.ElementTree as ET
import re

#SIZES ensures the photos we are getting from Flickr are not too large
SIZES = ["url_o", "url_k", "url_h", "url_l", "url_c"]
api_key = "API KEY"
api_secret = "API SECRET"


def get_photos(image_tag):
    extras = ','.join(SIZES)
    flickr = flickrapi.FlickrAPI(api_key, api_secret)

    # Only do this if we don't have a valid token already
    # if not flickr.token_valid(perms=u'read'):
    #
    #     # Get a request token
    #     flickr.get_request_token(oauth_callback='oob')
    #
    #     # Open a browser at the authentication URL. Do this however
    #     # you want, as long as the user visits that URL.
    #     authorize_url = flickr.auth_url(perms=u'read')
    #     webbrowser.open_new_tab(authorize_url)
    #
    #     # Get the verifier code from the user. Do this however you
    #     # want, as long as the user gives the application the code.
    #     verifier = str(input('Verifier code: 966-106-432 '))
    #
    #     # Trade the request token for an access token
    #     flickr.get_access_token(verifier)

    #photos walks through Flickr based on the arguments and returns the photos as data objects
    photos = flickr.walk(text=image_tag,  # it will search by image title and image tags
                         extras=extras,  # get the urls for each size we want, and only in Vienna
                         privacy_filter=1,  # search only for public photos
                         per_page=50,
                         has_geo=1,
                         bbox = '16.195221,48.122134,16.578369,48.320795',
                         place_type_id = '11',
                         min_taken_date='2016-01-01',
                         max_taken_date='2016-12-31',
                         sort='relevance')  # we want what we are looking for to appear first

    return photos

def get_photo_info(photo):
    info =['','']

    for i in range(len(SIZES)):
        # makes sure the loop is done in the order we want
        info[0] = photo.get(SIZES[i])
        info[1] = photo.get('id')

        if info[0]:  # if url is None try with the next size

            return info

def get_info(photos):
    #can add a counter and max to limit the amount of photos downlaoded, uncomment commented code in below section
    # counter=0
    # max= 10
    urls=[]
    ids=[]

    #look through photo objects and append urls, and important info to arrays
    for photo in photos:

        # if counter < max:

        info = get_photo_info(photo)  # get preffered size url
        if info[0]:
            urls.append(info[0])

            # counter += 1
            # if no url for the desired sizes then try with the next photo
        if info[1]:
            ids.append(info[1])
        else:
            break

    information=[urls, ids]

    return information

def get_all_info(info):
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    total_info = []


    for photoID in info[1]:
        #gather info for each photo
        full_info = flickr.photos.getInfo(api_key=api_key,photo_id=photoID)

        #full_info returns as an unorganized xml, so it is converted to a string, then regex applied below for information parsing
        full_data = ET.tostring(full_info).decode("utf-8")

        #regex for attributes
        lat_find = re.compile(r'(?<=latitude=)\S+')
        long_find = re.compile(r'(?<=longitude=)\S+')
        desc_find = re.compile(r'(?<=description>)\S+')
        title_find = re.compile(r'(?<=title>)\S+')
        taken_find = re.compile(r'(?<=taken=)\S+')
        realname_find = re.compile(r'(?<=realname=)\S+')
        username_find = re.compile(r'(?<=username=)\S+')

        #cleaning data
        lat = [x.strip('"') for x in re.findall(lat_find, full_data)][0]
        long = [x.strip('">') for x in re.findall(long_find, full_data)][0]
        desc = [x.strip('>') for x in re.findall(desc_find, full_data)][0]
        title = [x.strip('>') for x in re.findall(title_find, full_data)][0]
        taken = [x.strip('"') for x in re.findall(taken_find, full_data)][0]
        realname = [x.strip('"') for x in re.findall(realname_find, full_data)][0]
        username = [x.strip('"') for x in re.findall(username_find, full_data)][0]

        #storing data to return attribute array
        photo_info=[]
        photo_info.append(lat)
        photo_info.append(long)
        photo_info.append(photoID)
        photo_info.append(desc)
        photo_info.append(title)
        photo_info.append(taken)
        photo_info.append(realname)
        photo_info.append(username)

        total_info.append(photo_info)

    return total_info
