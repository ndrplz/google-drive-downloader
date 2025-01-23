import logging
import zipfile
from os import makedirs
from os.path import dirname
from os.path import exists

from requests import Session

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CHUNK_SIZE = 32768
DOWNLOAD_URL = 'https://docs.google.com/uc?export=download'


# From https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
def _sizeof_fmt(num, suffix='B'):
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return '{:.1f} {}{}'.format(num, unit, suffix)
        num /= 1024.0
    return '{:.1f} {}{}'.format(num, 'Yi', suffix)


def _save_response_content(response, destination, showsize, current_size):
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                if showsize:
                    logger.info('\r' + _sizeof_fmt(current_size[0]) + ' ')
                    current_size[0] += CHUNK_SIZE


def download_file_from_google_drive(file_id, dest_path, overwrite=False, unzip=False, showsize=False, raise_errors=False):
    """
    Downloads a shared file from Google Drive into a given folder.
    Optionally unzips it.

    Parameters
    ----------
    file_id: str
        the file identifier.
        You can obtain it from the sharable link.
    dest_path: str
        the destination where to save the downloaded file.
        Must be a path (for example: './downloaded_file.txt')
    overwrite: bool
        optional, if True forces re-download and overwrite.
    unzip: bool
        optional, if True unzips a file.
        If the file is not a zip file, ignores it.
    showsize: bool
        optional, if True print the current download size.
    raise_errors: bool
        optional, if True raises an error when the download fails.
    Returns
    -------
    None
    """

    destination_directory = dirname(dest_path)
    if destination_directory and not exists(destination_directory):
        makedirs(destination_directory)

    if not exists(dest_path) or overwrite:

        session = Session()

        logger.info('Downloading {} into {}... '.format(file_id, dest_path))

        params = {'id': file_id, 'confirm': True}
        response = session.post(DOWNLOAD_URL, params=params, stream=True)

        if not response.ok:
            msg = f'Download error code {response.status_code}: {response.reason}.'
            if raise_errors:
                raise Exception(msg)
            else:
                logger.warn(msg)
                return

        if showsize:
            logger.info()  # Skip to the next line

        current_download_size = [0]
        _save_response_content(response, dest_path, showsize, current_download_size)
        logger.info('Done.')

        if unzip:
            try:
                logger.info('Unzipping...')
                with zipfile.ZipFile(dest_path, 'r') as z:
                    z.extractall(destination_directory)
                logger.info('Done.')
            except zipfile.BadZipfile:
                msg = 'Ignoring `unzip` since "{}" does not look like a valid zip file'.format(file_id)
                if raise_errors:
                    raise Exception(msg)
                else:
                    logger.warn(msg)
