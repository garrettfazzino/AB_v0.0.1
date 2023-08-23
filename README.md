# AutoBeats
A simple solution for music producers to getting your beats out to Youtube passively. 

# Environment Setup
In order to set your environment up to run the code here, first install all requirements:
'''
pip3 install -r requirements.txt
'''

Rename example.env to .env and edit the variables appropriately.
'''
YOUTUBE_API_SECRET= Path to file where your .json file lives
YOUTUBE_OAUTH= Path to the downloaded OAuth .json file lives
YOUTUBE_CHANNEL_ID= ID of your personal youtube channel
GOOGLE_STORAGE_KEY= API access to GCP project containing storage bucket
GCS_BUCKET_NAME= Name of the storage bucket where your audio files live
TOKEN_PICKLE= Path to token.pickle file if exists already
BACKGROUND_VIDEO_PATH= Path to the desired background video of your choice
'''

# How does it work?
AutoBeats is made to be a background uploader which takes your audio files from the cloud, downloads them to your disk, concatenates them with a video of your choosing for background viewing, and then uploads it to youtube with the correct category, a unique name, and other identifying factors for the upload. 

You will need to have a GCP account with audio files stored in a GCS bucket, or you can modify the download function within the app to pull from audio files on disk. You will also need to have the Youtube_API_V3 activated within GCP in order to create the uploads.

The process to authenticate is a bit tricky, but if all goes properly, when you run for the first time you will need to log in to your Youtube account and that will grant you the token.pickle file which is needed to authenticate access from the app.

# System Requirements
Python3.8 or later. I created this app on an M1 Macbook, so other platform translation may vary.