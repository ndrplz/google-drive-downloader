from __future__ import print_function
import re
import requests
import zipfile
import warnings
from sys import stdout, platform, exit
from os import makedirs
from os.path import dirname
from os.path import exists


class GoogleDriveDownloader:
    """
    Minimal class to download shared files from Google Drive.
    """

    CHUNK_SIZE = 32768
    DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'

    @staticmethod
    def download_file_from_google_drive(file_id, dest_path='', overwrite=False, unzip=False, showsize=False):
        """
        Downloads a shared file from google drive into a given folder.
        Optionally unzips it.

        Parameters
        ----------
        file_id: str
            the file identifier.
            You can obtain it from the sharable link.
        dest_path: str
            optional, the destination where to save the downloaded file.
            Must be a path (for example: './downloaded_file.txt')
            If omitted, it will try to get the correct name from the
            response headersand download in the local directory.
            It will abort the download if the filename couldn't be
            retrieved from header Content-Disposition.
        overwrite: bool
            optional, if True forces re-download and overwrite.
        unzip: bool
            optional, if True unzips a file.
            If the file is not a zip file, ignores it.
        showsize: bool
            optional, if True prints the current download size.
        Returns
        -------
        None
        """

        if dest_path:
            # Make sure the directories for the destination path exists
            destination_directory = dirname(dest_path)
            if not exists(destination_directory):
                makedirs(destination_directory)

            # If the file already exists and we're not overwritting, stop here (Performance Check)
            if exists(dest_path) and not overwrite:
                exit('File already exists on disk. Set `overwrite` flag to download it again.')

        session = requests.Session()

        response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params={'id': file_id}, stream=True)

        token = GoogleDriveDownloader._get_confirm_token(response)
        if token:
            params = {'id': file_id, 'confirm': token}
            response = session.get(GoogleDriveDownloader.DOWNLOAD_URL, params=params, stream=True)

        if not dest_path:
            # Get the filename from the response header 'Content-Disposition'
            match = re.search(r'filename="(?P<filename>.+)"', response.headers['Content-Disposition'])

            # Make sure we found the filename field inside Content-Disposition
            if match is None:
                exit('\n\nERROR: Unable to retrieve `dest_path` from `file_id`, please set it manually.')

            if platform == 'win32':
                # Make it Windows safe, stripping: \/<>:"|?*
                remove_characters = dict((ord(char), None) for char in '\\/<>:"|?*')
            else:
                # Make it macOS and linux safe, stripping: /
                remove_characters = dict((ord(char), None) for char in '/')

            dest_path = match['filename'].translate(remove_characters)

            # Check to see if the filename retrieved already exists and we're not overwritting it
            if exists(dest_path) and not overwrite:
                exit('File already exists on disk. Set `overwrite` flag to download it again.')

        print('Downloading {} into {}... '.format(file_id, dest_path), end='')
        stdout.flush()

        if showsize:
            print()  # Skip to the next line

        current_download_size = [0]
		
        try:
            GoogleDriveDownloader._save_response_content(response, dest_path, showsize, current_download_size)
            print('Done.')

            if unzip:
                try:
                    print('Unzipping...', end='')
                    stdout.flush()
                    with zipfile.ZipFile(dest_path, 'r') as z:
                        z.extractall(destination_directory)
                    print('Done.')
                except zipfile.BadZipfile:
                    warnings.warn('Ignoring `unzip` since "{}" does not look like a valid zip file'.format(file_id))
        except KeyboardInterrupt:
            print('\n\nFile download cancelled.')
            if not overwrite:
                print('Delete the incomplete download from the disk before retrying.')

    @staticmethod
    def _get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    @staticmethod
    def _save_response_content(response, destination, showsize, current_size):
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(GoogleDriveDownloader.CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    if showsize:
                        print('\r' + GoogleDriveDownloader.sizeof_fmt(current_size[0]), end='  ')
                        stdout.flush()
                        current_size[0] += GoogleDriveDownloader.CHUNK_SIZE

    # From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    @staticmethod
    def sizeof_fmt(num, suffix='B'):
        for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
            if abs(num) < 1024.0:
                return '{:.1f} {}{}'.format(num, unit, suffix)
            num /= 1024.0
        return '{:.1f} {}{}'.format(num, 'Yi', suffix)
