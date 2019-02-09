# google-drive-downloader
Minimal class to download shared files from Google Drive.

### How to install:
Installing is as simple as

```
pip install googledrivedownloader
```

### Hello World
You will need to obtain the sharable link from Google Drive:

```python
from google_drive_downloader import GoogleDriveDownloader as gdd

gdd.download_file_from_google_drive(file_id='1iytA1n2z4go3uVCwE__vIKouTKyIDjEq',
                                    dest_path='./data/mnist.zip',
                                    unzip=True)
```
This will download a `mnist.zip` file into a `data` folder and unzip it.


### Tips
* Set `showsize=True` to see the download progress
* Set `overwrite=True` you really want to overwrite an already existent file.
