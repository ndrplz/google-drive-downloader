from setuptools import setup

setup(
    name='googledrivedownloader',
    version='0.4',
    packages=['google_drive_downloader'],
    install_requires=['plac'],
    url='https://github.com/ndrplz/google-drive-downloader',
    download_url='https://github.com/ndrplz/google-drive-downloader/archive/0.2.tar.gz',
    license='MIT',
    author='Davide Abati and Andrea Palazzi',
    author_email='ndrplz@gmail.com',
    description='Minimal class to download shared files from Google Drive.',
    entry_points={
        "console_scripts": ["googledrivedownloader=google_drive_downloader.cli:entry_point"]
    }
)
