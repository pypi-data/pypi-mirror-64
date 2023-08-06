import re
from pathlib import Path
from typing import Dict

import requests
from requests import Session


def download_file_content(url: str, session: Session, dir_path) -> Path:
    """
    Check if file exists. If not, download it.
    :param url: url of the file
    :param session: session http
    :param dir_path: destination dir
    :return:
    """
    with session.get(url, stream=True) as response:
        filename = obtain_filename(response, url)
        path_filename = dir_path / filename
        if path_filename.exists():
            return path_filename
        try:
            with open(path_filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            raise e
        return path_filename


def download_files(data_files: Dict[str, Dict[str, any]], dir_path=Path('/tmp/'), target_data_urls=None) -> Dict[
    str, Dict[str, any]]:
    """
    @param data_files: A Dict with Dict
    @param dir_path: destination dir
    @param target_data_urls: ModelCatalog urls of DataSpecifications to download
    @return: A Dict with Dict
    """

    session = requests.Session()
    if not target_data_urls:
        target_data_urls = data_files.keys()

    for key in data_files:
        if key in target_data_urls:
            data_files[key]['path'] = download_file_content(data_files[key]['url'], session, dir_path)
    return data_files


def obtain_filename(response, url):
    if 'content-disposition' in response.headers:
        filename = re.findall("filename=(.+)", response.headers['content-disposition'])[0]
    else:
        filename = url.split("/")[-1]
    return filename
