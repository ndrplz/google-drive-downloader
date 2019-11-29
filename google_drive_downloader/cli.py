import plac
from .google_drive_downloader import GoogleDriveDownloader

def entry_point():
    plac.call(GoogleDriveDownloader.download_file_from_google_drive)
