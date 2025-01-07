# google-drive-downloader
Minimal class to download shared files from Google Drive.

### How to install:

This package is on [PyPI](https://pypi.org/project/googledrivedownloader/). Installing is as simple as

```
pip install googledrivedownloader
```

### Hello World

```python
from googledrivedownloader import download_file_from_google_drive

# Single image file
download_file_from_google_drive(file_id='1H1ett7yg-TdtTt6mj2jwmeGZaC8iY1CH',
                                dest_path='data/crossing.jpg')
# Zip archive
download_file_from_google_drive(file_id='13nD8T7_Q9fkQzq9bXF2oasuIZWao8uio',
                                dest_path='data/docs.zip', unzip=True)
```


### Tips
* Set `showsize=True` to see the download progress
* Set `overwrite=True` you really want to overwrite an already existent file.
