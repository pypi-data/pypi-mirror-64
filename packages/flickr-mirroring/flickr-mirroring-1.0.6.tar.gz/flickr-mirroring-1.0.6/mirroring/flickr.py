#!/usr/bin/env python
#
# Copyright (C) 2019 Intek Institute.  All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import argparse
import datetime
import enum
import getpass
import hashlib
import json
import logging
import os
import random
import re
import requests
import sys
import time
import traceback
import urllib.error

from langdetect.lang_detect_exception import LangDetectException
from majormode.perseus.model import obj
from majormode.perseus.model.label import Label
from majormode.perseus.model.locale import DEFAULT_LOCALE
from majormode.perseus.model.locale import Locale
from majormode.perseus.utils import file_util
from majormode.perseus.utils import image_util
import langdetect
import requests


# Default name of the folder where the photo of a Flickr user are
# locally stored in.
DEFAULT_CACHE_FOLDER_NAME = '~/.flickr'

# Default name of the file where the Flickr API keys are stored in.  By
# default, this file is save in the default Flickr cache folder.
DEFAULT_API_KEYS_FILE = 'flickr_keys'

# Time in seconds between two consecutive scans of the photos of a
# Flickr user.
IDLE_DURATION_BETWEEN_CONSECUTIVE_SCANS = 60 * 5

# Build the logging formatter instance to log message including the
# human-readable time when message was logged and the level name for
# this message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
LOGGING_FORMATTER = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

# Logging levels supported by the application.
LOGGING_LEVELS = (
    logging.CRITICAL,
    logging.ERROR,
    logging.WARNING,
    logging.INFO,
    logging.DEBUG
)

# Photo information levels supported by the application.
PHOTO_INFO_LEVEL_TITLE = 0
PHOTO_INFO_LEVEL_DESCRIPTION = 1
PHOTO_INFO_LEVEL_COMMENTS = 2

PHOTO_INFO_LEVELS = (
    PHOTO_INFO_LEVEL_TITLE,
    PHOTO_INFO_LEVEL_DESCRIPTION,
    PHOTO_INFO_LEVEL_COMMENTS
)

# Regular expression that matches HTML tags.
REGEX_HTML_TAG = re.compile(r'<[^>]*>')

REGEX_HTML_TAG_START = re.compile(r'<([a-z]+)\s*[^>]*>')

REGEX_HTML_STANDALONE_TAG = re.compile(r'<([a-z]+)\s*[^>^/]*\s*/>')

# Specify the method to mirror the photostream of a Flickr user.
CachingStrategy = enum.Enum(
    'CachingStrategy',
    [
        # First-In First-Out: this method consists in downloading photos from
        # the latest published by the user to the earliest.
        'FIFO',

        # Last-In First-Out: This method consists in downloading photos from the
        # earliest photo published by the user to the latest.
        'LIFO'
    ]
)




class FlickrApi:
    DEFAULT_TIMEOUT = 5000

    FLICKR_REST_API_METHOD_URL = 'https://www.flickr.com/services/rest/?method={}'

    def __call_remote_method(self, method_name, parameters=None, timeout=None):
        """

        :param method_name:
        :param parameters:
        :param timeout:
        :return:
        """
        url = self.FLICKR_REST_API_METHOD_URL.format(method_name)

        if parameters is None:
            parameters = {}

        parameters.update({
            'api_key': self.__consumer_key,
            'format': 'json',
            'nojsoncallback': 1  # If you just want the raw JSON, with no function wrapper.
        })

        response = requests.get(url, params=parameters, timeout=timeout or self.DEFAULT_TIMEOUT)

        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        data = response.json()
        if data['stat'] != 'ok':
            raise Exception(data['message'])

        return data

    def __init__(self, consumer_key, consumer_secret):
        """

        :param consumer_key:
        :param consumer_secret:
        """
        self.__consumer_key = consumer_key
        self.__consumer_secret = consumer_secret

    def find_user(self, username):
        """
        Build an object `FlickrUser` providing his username


        :param username: The username of a Flickr user.


        :return: An object `FlickrUser`.


        :raise Exception: If a network error occurs of if the Flickr API
            returns an error.
        """
        if not isinstance(username, str):
            raise TypeError("the argument 'username' MUST be a string")

        data = self.__call_remote_method('flickr.people.findByUsername', {'username': username})

        return FlickrUser.from_json(data['user'])

    def get_photo_comments(self, photo_id):
        """
        Return the comments of a photo.


        :param photo_id: Identification of a photo to fetch size information
            for.

        :return: A list of strings corresponding to comments posted to the
              photo.
        """
        parameters = {'photo_id': photo_id}
        data = self.__call_remote_method('flickr.photos.comments.getList', parameters)
        comments = [payload['_content'] for payload in data['comments'].get('comment', [])]
        return comments

    def get_photo_description(self, photo_id):
        """
        Return the description of a photo.


        :param photo_id: Identification of a photo to fetch the description
            for.

        :return: A string corresponding to the description of the photo.
        """
        parameters = {'photo_id': photo_id}
        data = self.__call_remote_method('flickr.photos.getInfo', parameters)
        description = data['photo']['description']['_content']
        return description

    def get_photo_sizes(self, photo_id):
        """
        Returns the available sizes for a public photo.


        :param photo_id: Identification of a photo to fetch information for.


        :return: A list of objects `FlickrPhotoSize`.
        """
        parameters = {'photo_id': photo_id}
        data = self.__call_remote_method('flickr.photos.getSizes', parameters)
        return [FlickrPhotoSize.from_json(payload) for payload in data['sizes']['size']]

    def get_photos(self, user_id, page=None, per_page=None):
        """
        Return a list of public photos of the specified user.


        :param user_id: The NSID of the user who's photo to search.

        :param page: The page of photos to return. If this argument is omitted,
            it defaults to `1`.

        :param per_page: Number of photos to return per page.  If this
            argument is omitted, it defaults to 100.  The maximum allowed
            value is 500.


        :return: A tuple `photos, page_count, photo_count` where:

            * `photos`: A list of objects `FlickrPhoto`.

            * `page_count`: The number of pages of `per_page` photos in the user's
              photostream.

            * `photo_count`: The total number of photos in the user's photostream.
        """
        parameters = {'user_id': user_id}

        if page is not None:
            if not isinstance(page, int):
                raise TypeError("the argument 'page' MUST be an integer")

            if page <= 0:
                raise ValueError("the argument 'page' MUST be a strictly positive integer")

            parameters['page'] = page

        if per_page is not None:
            if not isinstance(per_page, int):
                raise TypeError("the argument 'limit' MUST be an integer")

            if not 0 < per_page <= 500:
                raise ValueError("the argument 'limit' MUST between 1 and 500")

            parameters['per_page'] = per_page

        data = self.__call_remote_method('flickr.people.getPublicPhotos', parameters)

        result = data['photos']
        page_count = int(result['pages'])
        photo_count = int(result['total'])
        photos = [FlickrPhoto.from_json(payload )for payload in result['photo']]

        return photos, page_count, photo_count

class FlickrUser:
    """
    Represent a Flickr user.
    """
    def __init__(self, user_id, username):
        self.__id = user_id
        self.__username = username

    @staticmethod
    def from_json(payload):
        """
        Build an object `FlickrUser` from a JSON expression that identifies a
        user, as returned by several Flickr API methods.


        :param payload: A JSON expression with the following structure:

                {
                  "id": "13476480@N07",
                  "nsid": "13476480@N07",
                  "username": {
                    "_content": "manhhai"
                  }
                }

        where:

        * `nsid` (required): A string representing the unique identifier that
          Flickr uses to associate all of the user's photos, settings, etc.
          This number is also used by default for the Flickr personalized URL
          of the user until he choose a more user-friendly one.

        * `username`(required): A JSON expression containing the profile name
          by which the user is identified by Flickr, and this is what others
          will see when you post to the Flickr Forums or leave comments.


        :return: An object `FlickrUser`.
        """
        return payload and FlickrUser(
            payload['nsid'],
            payload['username']['_content'])

    @property
    def id(self):
        return self.__id

    @property
    def username(self):
        return self.__username


class FlickrPhoto:
    PHOTO_PROVIDER = 'flickr'

    FormatType = enum.Enum(
        'FormatType',
        ['JPEG', 'PNG', 'TIFF'])

    FORMAT_TYPE_EXTENSIONS = {
        FormatType.JPEG: 'jpg',
        FormatType.PNG: 'png',
        FormatType.TIFF: 'tiff'
    }

    @staticmethod
    def __detect_locale(text):
        """
        Detect the language of a text.


        :param text: A human-readable text.


        :return: An instance `Locale` representing the language used to write in
            the specified text.
        """
        try:
            return Locale.from_string(langdetect.detect(text), strict=False)
        except langdetect.lang_detect_exception.LangDetectException:
            return DEFAULT_LOCALE

    def __eq__(self, other):
        return self.__inventory_number == other.__inventory_number

    @staticmethod
    def __find_best_size(sizes):
        """
        Return a photo size that has the highest resolution.


        :param sizes: A list of objects `FlickrPhotoSize`.


        :return: An object `FlickPhotoSize` that has the highest resolution.
        """
        if sizes:
            sorted_sizes = sorted(sizes, key=lambda size: size.width * size.height, reverse=True)
            return sorted_sizes[0]

    def __init__(self, photo_id, title):
        """

        :param photo_id:
        :param title:
        """
        self.__id = photo_id
        self.__provider = self.PHOTO_PROVIDER
        self.__format = self.FormatType.JPEG

        # Generate the Inventory number of the photo.  This identification
        # MUST be unique from any sources of photos.
        self.__inventory_number = hashlib.md5(f'{self.__provider}.{self.__id}'.encode()).hexdigest()

        # For better performance, when browsing the photos of a user, store
        # the original title and only build the localized title the first time
        # the property `title` is called.
        self.__original_title = title
        self.__title = None

        self.__sizes = None
        self.__best_size = None

        self.__description = None
        self.__comments = None

    @property
    def best_size(self):
        if self.__best_size is None:
            self.__best_size = self.__find_best_size(self.__sizes)

        return self.__best_size

    @property
    def comments(self):
        return self.__comments

    @comments.setter
    def comments(self, comments):
        self.__comments = []

        for comment in comments:
            cleansed_comments = cleanse_text_content(comment)
            self.__comments.append(Label(
                cleansed_comments,
                DEFAULT_LOCALE if len(cleansed_comments) == 0 else self.__detect_locale(cleansed_comments)))

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, description):
        cleansed_description = cleanse_text_content(description)
        self.__description = Label(
            cleansed_description,
            DEFAULT_LOCALE if len(cleansed_description) == 0 else self.__detect_locale(cleansed_description))

    @staticmethod
    def from_json(payload):
        return payload and FlickrPhoto(
            payload['id'],
            payload['title'])

    @property
    def id(self):
        return self.__id

    @property
    def image_filename(self):
        return f'{self.__inventory_number}.{self.FORMAT_TYPE_EXTENSIONS[self.__format]}'

    @property
    def info_filename(self):
        return f'{self.__inventory_number}.json'

    @property
    def inventory_number(self):
        return self.__inventory_number

    def provider(self):
        return self.__provider

    @property
    def sizes(self):
        return self.__sizes

    @sizes.setter
    def sizes(self, sizes):
        self.__sizes = sizes
        self.__best_size = None

    @property
    def title(self):
        if self.__title is None:
            title = cleanse_text_content(self.__original_title)
            self.__title = Label(title, DEFAULT_LOCALE if len(title) == 0 else self.__detect_locale(title))

        return self.__title


class FlickrPhotoSize:
    def __init__(self, label, width, height, url):
        self.__label = label
        self.__width = width
        self.__height = height
        self.__url = url

    @staticmethod
    def from_json(payload):
        return payload and FlickrPhotoSize(
            payload['label'],
            int(payload['width']),
            int(payload['height']),
            payload['source'])

    @property
    def height(self):
        return self.__height

    @property
    def label(self):
        return self.__label

    @property
    def url(self):
        return self.__url

    @property
    def width(self):
        return self.__width


class FlickrUserPhotostreamMirroringAgent:
    # Default number of photos per page fetched from Flickr API.
    DEFAULT_PHOTO_COUNT_PER_PAGE = 100

    # Maximum number of photos per page that can fetched from Flickr API.
    MAXIMUM_PHOTO_COUNT_PER_PAGE = 500

    REQUEST_TIMEOUT = 10

    def __build_cached_photo_image_file_path_name(self, photo):
        """
        Return the path and name of the image file of a photo.


        :return: the complete file path name of the specified file.


        :raise AssertionError: If the length of the photo's file name is not
            long enough.
        """
        assert len(photo.image_filename) >= self.__cache_directory_depth, \
            f"The filename {photo.image_filename} is not long enough: {self.__cache_directory_depth} characters required"

        return os.path.join(
            self.__cache_root_path_name,
            file_util.build_tree_file_pathname(photo.image_filename, directory_depth=self.__cache_directory_depth))

    def __build_cached_photo_info_file_path_name(self, photo):
        """
        Return the path and name of the image file of a photo.


        :param cache_path_name: absolute path where files of photos are stored
            into.

        :param file_extension: extension of the file of this photo to return
            its complete path and name.

        :param cache_directory_depth: number of sub-directories the cache file
            system is composed, its depth, to store photo files into the child
            directories, the leaves, of this cache.


        :return: the complete file path name of the specified file.


        :raise AssertionError: If the length of the photo's file name is not
            long enough.
        """
        assert len(photo.image_filename) >= self.__cache_directory_depth, \
            f"The filename {photo.image_filename} is not long enough: {self.__cache_directory_depth} characters required"

        return os.path.join(
            self.__cache_root_path_name,
            file_util.build_tree_file_pathname(photo.info_filename, directory_depth=self.__cache_directory_depth))

    def __cache_photo_info(
            self,
            photo,
            info_level=PHOTO_INFO_LEVEL_TITLE):
        """

        :param photo:
        :param info_level:
        :return:
        """
        info_file_path_name = self.__build_cached_photo_info_file_path_name(photo)
        file_util.make_directory_if_not_exists(os.path.dirname(info_file_path_name))

        info = {}
        if info_level >= PHOTO_INFO_LEVEL_TITLE:
            info['title'] = photo.title

        if info_level >= PHOTO_INFO_LEVEL_DESCRIPTION:
            if photo.description is None:
                photo.description = self.__flickr_api.get_photo_description(photo.id)
            info['description'] = photo.description

        if info_level >= PHOTO_INFO_LEVEL_COMMENTS:
            if photo.comments is None:
                photo.comments = self.__flickr_api.get_photo_comments(photo.id)
            info['comments'] = photo.comments

        with open(info_file_path_name, 'wt') as fd:
            fd.write(json.dumps(obj.stringify(info)))

    @classmethod
    def __download_file_from_url(cls, url, image_file_path_name):
        """

        :param url:

        :param image_file_path_name:

        :return:
        """
        response = requests.get(url, allow_redirects=True, timeout=cls.REQUEST_TIMEOUT)
        with open(image_file_path_name, 'wb') as fd:
            fd.write(response.content)

    def __download_photo_image(self, photo):
        """
        Download the best resolution image of the photo into the local cache.


        @param photo: An object `FlickrPhoto`.
        """
        image_file_path_name = self.__build_cached_photo_image_file_path_name(photo)
        file_util.make_directory_if_not_exists(os.path.dirname(image_file_path_name))

        photo.sizes = self.__flickr_api.get_photo_sizes(photo.id)

        self.__download_file_from_url(photo.best_size.url, image_file_path_name)

    def __fetch_photos(
            self,
            photo_count_per_page=DEFAULT_PHOTO_COUNT_PER_PAGE,
            page_index=1):
        """
        Fetch the list of photos that the specified user has posted on Flickr.


        :param photo_count_per_page: Number of photos that are returned per
            page.  The maximum allowed value is `MAXIMUM_PHOTO_COUNT_PER_PAGE`.

        :param page_index: Integer representing the number of the page to
            return photos.


        :return: A tuple `photos, page_count, photo_count` where

            * `photos`: A list of objects representing the photos of the specified
              page.

            * `photo_count`: The total number of photos.

            * `page_count`: The number of available pages.

            * `photo_count_per_page`: Number of photos that are returned per page.
        """
        if photo_count_per_page < 0:
            photo_count_per_page = self.DEFAULT_PHOTO_COUNT_PER_PAGE
        elif photo_count_per_page > self.MAXIMUM_PHOTO_COUNT_PER_PAGE:
            photo_count_per_page = self.MAXIMUM_PHOTO_COUNT_PER_PAGE

        while True:
            try:
                photos, page_count, photo_count = self.__flickr_api.get_photos(self.__flickr_user.id, page=page_index, per_page=photo_count_per_page)
                return photos, photo_count, page_count, photo_count_per_page

            except:
                logging.error(traceback.format_exc())
                time.sleep(random.randint(5, 10))

    def __init__(
            self,
            username,
            flickr_consumer_key,
            flickr_consumer_secret,
            cache_root_path_name=None,
            cache_directory_depth=4,
            caching_strategy=None,
            info_level=PHOTO_INFO_LEVEL_TITLE,
            image_only=False,
            info_only=False,
            verify_image=False):
        """
        Build an agent object responsible for mirroring the photostream of a
        Flickr user.


        :param username: Username of the account of a user on Flickr to mirror
            his photostream.

        :param flickr_consumer_key: A unique string used by the Consumer to
            identify itself to the Flickr API.

        :param flickr_consumer_secret: A secret used by the Consumer to
            establish ownership of the Consumer Key.

        :param cache_root_path_name: Specify the absolute path where the
            images and/or information of the photos downloaded from Flickr
            need to be stored in.

        :param cache_directory_depth: Number of sub-directories the cache file
            system is composed, its depth, to store photo files into the child
            directories, the leaves, of this cache.

        :param caching_strategy: An item of the enumeration `CachingStrategy`

        :param image_only: Specify whether the script must only download
            photos' images.

        :param info_level: Specify the level of information of a photo to
            fetch (value between 0 and 2).

        :param info_only: Specify whether the agent must only download photos'
            information.

        :param verify_image: Specify whether the images that are downloaded
            must be verified, to prevent from broken images that are partially
            downloaded, for instance when a network outage occurs.


        :raise TypeError: If the argument `caching_strategy` is not None and
            its value is not an item of the enumeration `CachingStrategy`.

        :raise ValueError: If both arguments `image_only` and `info_only` are
            `True`, or if the argument `info_level` is specified while the
            argument `image_only` has been specified.
        """
        if image_only and info_only:
            raise ValueError(f"conflicting options 'image_only' ({image_only}) and 'info_only' ({info_only})")

        if image_only and info_level:
            raise ValueError(f"the argument 'info_level' cannot be specified with the argument `image_only`")

        if caching_strategy and not isinstance(caching_strategy, CachingStrategy):
            raise TypeError(f"argument 'caching_strategy' MUST be an item of the enumeration {CachingStrategy.__name__}")

        self.__flickr_api = FlickrApi(flickr_consumer_key, flickr_consumer_secret)

        self.__flickr_user = self.__flickr_api.find_user(username)

        self.__cache_root_path_name = self.__initialize_cache(root_path_name=cache_root_path_name)
        self.__cache_directory_depth = cache_directory_depth

        self.__caching_strategy = caching_strategy or CachingStrategy.LIFO

        self.__image_only = image_only
        self.__info_level = info_level
        self.__info_only = info_only
        self.__verify_image = verify_image

    def __initialize_cache(self, root_path_name=None):
        """
        Initialize the cache folder where photos' image and information (meta
        data) will be stored in.


        :param root_path_name: Root path of the cache folder.


        :return: Root path of the cache folder.
        """
        # Define the path of the folder to locally store the photos of this
        # Flickr user, and create this folder if it not already exists.
        path_name = os.path.join(
            os.path.expanduser(root_path_name or DEFAULT_CACHE_FOLDER_NAME),
            self.__flickr_user.username)

        file_util.make_directory_if_not_exists(path_name)
        return path_name

    def __is_photo_image_cached(self, photo, verify_image=False):
        """
        Indicate whether the image of the photo has been successfully cached.


        :param photo: An object `Photo`.

        :param verify_image: Indicate whether the function needs to check if
            the cached image is valid or not.  An image file could have been
            partially downloaded because of a network outage.

            If the image is not valid, and the value of the argument 'verify_image'
            is `True`, the function deletes this file from the cache to avoid
            checking uselessly the validity of this image, again and again, the
            next times this function is called.


        :return: `True` if the image of this photo has been cached; `False`
            otherwise.
        """
        image_file_path_name = self.__build_cached_photo_image_file_path_name(photo)
        if not os.path.exists(image_file_path_name):
            return False

        if verify_image:
            if not image_util.is_image_file_valid(image_file_path_name):
                logging.debug(f"Remove the invalid image {photo.inventory_number} from the cache")
                os.remove(image_file_path_name)
                return False

        return True

    def __is_photo_info_cached(self, photo, info_level=PHOTO_INFO_LEVEL_TITLE):
        """
        Indicate whether the info of the photo has been successfully cached.

        The function checks whether the photo's JSON file has been stored in
        the cache.


        :param photo: An object `Photo`.

        :param info_level:


        :return: `True` if the info of this photo has been cached; `False`
            otherwise.
        """
        info_file_path_name = self.__build_cached_photo_info_file_path_name(photo)
        if not os.path.exists(info_file_path_name):
            return False

        with open(info_file_path_name, 'rt') as fd:
            photo_info = json.loads(fd.read())

        if info_level == PHOTO_INFO_LEVEL_COMMENTS:
            return 'comments' in photo_info
        if info_level == PHOTO_INFO_LEVEL_DESCRIPTION:
            return 'description' in photo_info
        if info_level == PHOTO_INFO_LEVEL_TITLE:
            return 'title' in photo_info

        return True

    def __process_photo(
            self,
            photo,
            image_only=False,
            info_level=PHOTO_INFO_LEVEL_TITLE,
            info_only=False,
            verify_image=True):
        """
        Process the specified photo.

        The function checks whether the image and/or the information (at the
        level required) of this photo has been already cached.  If not, the
        function downloads the photo's image and/or fetches the information of
        this photo.


        :param photo: An object `FlickrObject`.

        :param image_only: Specify whether to only download photos' image.

        :param info_level: Specify the level of information of a photo to
            fetch (value between 0 and 2).

        :param info_only: Specify whether the agent must only download photos'
            information.

        :param verify_image: Specify whether the images that are downloaded
            must be verified, to prevent from broken images that are partially
            downloaded, for instance when a network outage occurs.


        :return: The function returns `True` if the cache has been updated by
            downloading the photo's image and/or the information of the photo;
            `False` otherwise.
        """
        cache_updated = False

        if not info_only and not self.__is_photo_image_cached(photo, verify_image=verify_image):
            logging.info(f"Caching image of photo {photo.inventory_number}...")
            self.__download_photo_image(photo)
            cache_updated = True

        if not image_only and not self.__is_photo_info_cached(photo):
            logging.info(f"Caching information of photo {photo.inventory_number}...")
            self.__cache_photo_info(photo, info_level=info_level)
            cache_updated = True

        return cache_updated

    def __run_fifo(self, photo_count, page_count, photo_count_per_page, flickr_photos=None, page_index=None):
        """
        Mirror the users' photostream using the First-In First-Out strategy.


        :param photo_count: Total number of photos that the user has published
            in his photostream.

        :param page_count: Number of pages of `photo_count_per_page` photos
            each that composes the user's photostream.

        :param photo_count_per_page: Number of photos that are returned per
            page.

        :param flickr_photos: A list of objects `FlickrPhoto` that have been
            initially fetched.  The Flickr API doesn't support any methods
            that would allow to get the number of photos/pages of the user's
            photostream without fetching a first set of photos.

        :param page_index: The index of the page where this list of objects
            `FlickrPhoto` have been fetched from.
        """
        page_index = page_count
        flickr_photos, page_count, photo_count = self.__fetch_photos(page_index=page_index)

        while page_index > 0:
            try:
                logging.info(f"Scanning page {page_index}/{page_count}...")

                for flickr_photo in flickr_photos:
                    self.__process_photo(
                        flickr_photo,
                        image_only=self.__image_only,
                        info_level=self.__info_level,
                        info_only=self.__info_only,
                        verify_image=self.__verify_image)

                page_index -= 1
                flickr_photos, photo_count, page_count, photo_count_per_page = self.__fetch_photos(page_index=page_index)

                # if photo_count != _photo_count:

            except urllib.error.URLError:
                logging.error(traceback.format_exc())

    def __run_lifo(self, photo_count, page_count, photo_count_per_page, flickr_photos=None, page_index=None):
        """
        Mirror the users' photostream using the Last-In First-Out strategy.


        :param photo_count: Total number of photos that the user has published
            in his photostream.

        :param page_count: Number of pages of `photo_count_per_page` photos
            each that composes the user's photostream.

        :param photo_count_per_page: Number of photos that are returned per
            page.

        :param flickr_photos: A list of objects `FlickrPhoto` that have been
            initially fetched.  The Flickr API doesn't support any methods
            that would allow to get the number of photos/pages of the user's
            photostream without fetching a first set of photos.

        :param page_index: The index of the page where this list of objects
            `FlickrPhoto` have been fetched from.
        """
        while page_index < page_count:
            try:
                logging.info(f"Scanning page {page_index}/{page_count}...")

                for flickr_photo in reversed(flickr_photos):
                    self.__process_photo(
                        flickr_photo,
                        image_only=self.__image_only,
                        info_level=self.__info_level,
                        info_only=self.__info_only,
                        verify_image=self.__verify_image)

                page_index += 1
                flickr_photos, photo_count, page_count, photo_count_per_page = self.__fetch_photos(page_index=page_index)

                # if photo_count != _photo_count:

            except urllib.error.URLError:
                logging.error(traceback.format_exc())

    @property
    def caching_strategy(self):
        return self.__caching_strategy

    def run(self, photo_count_per_page=DEFAULT_PHOTO_COUNT_PER_PAGE):
        """
        Mirror the users' photostream using the specified caching strategy.
        """
        is_running = True

        while is_running:
            try:
                # Fetch a first list of photos (from the first page) and the current
                # number of pages and total number of photos.
                page_index = 1
                flickr_photos, photo_count, page_count, photo_count_per_page = self.__fetch_photos(page_index=page_index, photo_count_per_page=photo_count_per_page)

                if self.__caching_strategy == CachingStrategy.LIFO:
                    self.__run_lifo(photo_count, page_count, photo_count_per_page, flickr_photos=flickr_photos, page_index=page_index)
                else:
                    self.__run_fifo(photo_count, page_count, photo_count_per_page, flickr_photos=flickr_photos, page_index=page_index)

                logging.info("Last iteration completed; breathing a little bit...")
                time.sleep(IDLE_DURATION_BETWEEN_CONSECUTIVE_SCANS)

            except KeyboardInterrupt:
                logging.info('Stopping this script...')
                is_running = False

            except:
                logging.error(traceback.format_exc())

    @property
    def user(self):
        return self.__flickr_user


def get_arguments():
    """
    Convert argument strings to objects and assign them as attributes of
    the namespace.


    @return: an instance `Namespace` corresponding to the populated
        namespace.
    """
    parser = argparse.ArgumentParser(description="Flickr Mirroring")

    parser.add_argument(
        '--cache-path',
        dest='flickr_cache_root_path_name',
        metavar='CACHE PATH',
        required=False,
        default='',
        help="specify the absolute path where the images and/or information of the photos downloaded from Flickr need to be stored in")

    parser.add_argument(
        '--consumer-key',
        dest='flickr_consumer_key',
        metavar='CONSUMER KEY',
        required=False,
        help="a unique string used by the Consumer to identify itself to the Flickr API")

    parser.add_argument(
        '--consumer-secret',
        dest='flickr_consumer_secret',
        metavar='CONSUMER SECRET',
        required=False,
        help="a secret used by the Consumer to establish ownership of the Consumer Key")

    parser.add_argument(
        '--debug',
        dest='logging_level',
        metavar='LEVEL',
        required=False,
        default=0,
        type=int,
        help=f"specify the logging level (value between 0 and {len(LOGGING_LEVELS) - 1}, from critical to debug)")

    parser.add_argument(
        '--fifo',
        dest='fifo',
        action='store_true',
        default=False,
        help="specify the First-In First-Out method to mirror the user's photostream, from the latest uploaded photo to the earliest")

    parser.add_argument(
        '--image-only',
        dest='image_only',
        action='store_true',
        help="specify whether the script must only download photos' images")

    parser.add_argument(
        '--info-level',
        dest='info_level',
        metavar='LEVEL',
        required=False,
        default=0,
        type=int,
        help=f"specify the level of information of a photo to fetch (value between 0 and {len(PHOTO_INFO_LEVELS) - 1})")

    parser.add_argument(
        '--info-only',
        dest='info_only',
        action='store_true',
        help="specify whether the script must only download photos' information")

    parser.add_argument(
        '--lifo',
        dest='lifo',
        action='store_true',
        default=False,
        help="specify the Last-In First-Out method to mirror the user's photostream, from the earliest uploaded photo to the lastest (default option)")

    parser.add_argument(
        '--save-api-keys',
        dest='save_api_keys',
        required=False,
        action='store_true',
        default=False,
        help="specify whether to save the Flickr API keys for further usage")

    parser.add_argument(
        '--verify-image',
        dest='verify_image',
        action='store_true',
        help="specify whether the script must verify images that have been download")

    parser.add_argument(
        '--username',
        dest='flickr_username',
        metavar='USERNAME',
        required=True,
        help="username of the account of a user on Flickr to mirror his photostream")

    return parser.parse_args()


def get_console_handler(logging_formatter=LOGGING_FORMATTER):
    """
    Return a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.


    :return: An instance of the `StreamHandler` class.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(logging_formatter)
    return console_handler


def main():
    arguments = get_arguments()
    setup_logger(logging_level=LOGGING_LEVELS[arguments.logging_level])

    # Check whether the specification of the caching strategy is coherent.
    if arguments.fifo and arguments.lifo:
        raise ValueError("you cannot specify both FIFO and LIFO caching strategy")

    caching_strategy = CachingStrategy.FIFO if arguments.fifo else CachingStrategy.LIFO

    # Get the Flickr API keys using the following methods:
    #
    # 1. Read the arguments passed to the script from the command line;
    # 2. Use the keys previously specified and stored in a file, if any;
    # 3. Request the user to input the keys.
    flickr_consumer_key_, flickr_consumer_secret_ = load_api_keys()

    flickr_consumer_key = arguments.flickr_consumer_key \
        or flickr_consumer_key_ \
        or getpass.getpass("Enter your Flickr API key: ")

    flickr_consumer_secret = arguments.flickr_consumer_secret \
        or flickr_consumer_secret_ \
        or getpass.getpass("Enter your Flickr API secret: ")

    if flickr_consumer_key is None or flickr_consumer_secret is None:
        raise ValueError('you MUST provide Flickr API keys')

    flickr_consumer_key = flickr_consumer_key.strip()
    flickr_consumer_secret = flickr_consumer_secret.strip()
    if arguments.save_api_keys:
        save_api_keys(flickr_consumer_key, flickr_consumer_secret)

    # Execute the agent responsible for fetching photos from the specified
    # Flickr account and for refreshing the local cache.
    agent = FlickrUserPhotostreamMirroringAgent(
        arguments.flickr_username,
        flickr_consumer_key,
        flickr_consumer_secret,
        caching_strategy=caching_strategy,
        image_only=arguments.image_only,
        info_level=PHOTO_INFO_LEVELS[arguments.info_level],
        info_only=arguments.info_only,
        verify_image=arguments.verify_image)

    agent.run()


def load_api_keys(keys_file_path_name=None):
    """

    :param keys_file_path_name:
    :return:
    """
    if keys_file_path_name is None:
        keys_file_path_name = os.path.join(DEFAULT_CACHE_FOLDER_NAME, DEFAULT_API_KEYS_FILE)

    keys_file_path_name = os.path.expanduser(keys_file_path_name)

    if not os.path.exists(keys_file_path_name):
        return None, None

    with open(keys_file_path_name, 'rt') as fd:
        keys = json.loads(fd.read())

    return keys['consumer_key'], keys['consumer_secret']


def save_api_keys(consumer_key, consumer_secret, keys_file_path_name=None):
    """



    :param consumer_key:

    :param consumer_secret:

    :param keys_file_path_name:


    :return:
    """
    if keys_file_path_name is None:
        keys_file_path_name = os.path.join(DEFAULT_CACHE_FOLDER_NAME, DEFAULT_API_KEYS_FILE)

    keys_file_path_name = os.path.expanduser(keys_file_path_name)

    with open(keys_file_path_name, 'wt') as fd:
        fd.write(json.dumps({
            'consumer_key': consumer_key,
            'consumer_secret': consumer_secret
        }))

    os.chmod(keys_file_path_name, 0o600)


def cleanse_text_content(text):
    """
    Strip any HTML tags from the specified content.  The function retains
    the content of every HTML tag.


    :param text: a string that may contain HTML tags.


    :return: the string where HTML tags have been replaced by their
        content.
    """
    # Remove all the HTML tags from the text.
    pure_text = REGEX_HTML_TAG.sub('', text.strip())

    # Remove all the redundant space characters, keeping all other whitespace
    # characters.  This includes the characters tab, linefeed, return,
    # formfeed, and vertical tab..
    #
    # Note: We do not call the function `str.split` without arguments as it
    #     removes all whitespaces.
    cleansed_text = ' '.join([w for w in pure_text.split(' ') if w])

    return cleansed_text


def setup_logger(
        logging_formatter=LOGGING_FORMATTER,
        logging_level=logging.INFO,
        logger_name=None):
    """
    Setup a logging handler that sends logging output to the system's
    standard output.


    :param logging_formatter: An object `Formatter` to set for this handler.

    :param logger_name: Name of the logger to add the logging handler to.
        If `logger_name` is `None`, the function attaches the logging
        handler to the root logger of the hierarchy.

    :param logging_level: The threshold for the logger to `level`.  Logging
        messages which are less severe than `level` will be ignored;
        logging messages which have severity level or higher will be
        emitted by whichever handler or handlers service this logger,
        unless a handler’s level has been set to a higher severity level
        than `level`.


    :return: An object `Logger`.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    logger.addHandler(get_console_handler(logging_formatter=logging_formatter))
    logger.propagate = False
    return logger


if __name__ == '__main__':
    main()


# agent = FlickrUserPhotostreamMirroringAgent(
#     'manhhai',
#     'cd3f52105cf2d04c1c92f3b95f59224f',
#     '39b25f0bbee6dbca',
#     info_level=2)
# agent.run()

#requests.exceptions.ReadTimeout
#requests.exceptions.ConnectionError
