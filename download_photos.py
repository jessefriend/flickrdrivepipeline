import requests
import os
import sys
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient.http import MediaInMemoryUpload, MediaFileUpload
import urllib.request
import io
import csv


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def get_credentials():

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'lbs\python_scripts\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    return service

def create_folder(folder_name):
        #gets service created above, and hard code folder id in to place all new data within it
        service = get_credentials()
        folder_id = "FOLDER_ID"

        # Create a folder on Drive, returns the newely created folders ID
        body = {
          'name': folder_name,
          'mimeType': "application/vnd.google-apps.folder",
          'parents': [folder_id]
        }

        root_folder = service.files().create(body = body).execute()

        return root_folder['id']

def download_images(urls, tag, photo_info):

    #get service, then create a new folder based on each tag
    service = get_credentials()

    folder_id= create_folder(tag)  # makes sure path exists

    #for loop through urls to create image in Drive
    for url in urls:
        image_name = url.split("/")[-1]
        file_metadata = {
            'name': image_name,
            'parents': [folder_id]
        }

        #response opens up the data. then image_file stores it
        response = urllib.request.urlopen(url)
        image_file = io.BytesIO(response.read())

        #create Drive media, then upload it
        media = MediaInMemoryUpload(image_file.read(),
                                        mimetype='image/jpeg',
                                        resumable=True)
        file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()

    #create CSV based on all images' information with certain tags
    with open('coordinates.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_NONE)

        #COMMENTED SECTION ONLY DOWNLOADS LAT,LONG, AND PHOTOID TO SAVE TIME AND VISUALIZE LOCATION OF IMAGES
        # writer.writerow(['Latitude', 'Longitude', "PhotoID", "Description", "Title", "Taken", "Real Name", "User Name"])
        #
        # for field in photo_info:
        #     writer.writerow([field[0], field[1], field[2]])
        writer.writerow(['Latitude', 'Longitude', "PhotoID", "Description", "Title", "Taken", "Real Name", "User Name"])

        for field in photo_info:
            writer.writerow([field[0], field[1], field[2], field[3], field[4], field[5], field[6], field[7]])

    csv_file_metadata = {
                'name': tag,
                'parents': [folder_id]
    }

    #create mdeia file for csv and upload it
    media = MediaFileUpload('coordinates.csv',
                            mimetype='text/csv',
                            resumable=True)
    file = service.files().create(body=csv_file_metadata,
                                  media_body=media,
                                  fields='id').execute()
