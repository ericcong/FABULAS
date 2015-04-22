""" Google Drive Filesystem. """
__author__ =  'Chen Cong <chen.cong@cs.rutgers.edu>'
__version__=  '1.0'

import oauth2client, httplib2, magic, json, apiclient

class GoogleDriveFS(object):
    """ This class provides a convenient way of using Google Drive APIs. """


    def __init__(self, key_file_name):
        """ Initializer

        Args:
            key_file_name (str): Path to the key of Google Drive service account.
        """

        with open(key_file_name) as key_fd:
            key_info = json.load(key_fd)
        credentials = oauth2client.client.SignedJwtAssertionCredentials(
                key_info["client_email"],
                key_info["private_key"],
                'https://www.googleapis.com/auth/drive')
        self.service = apiclient.discovery.build('drive', 'v2',
                http=credentials.authorize(httplib2.Http()))



    def upload(self, file_name, title=None, description=None):
        """ Upload a file

        Args:
            file_name (str): Path to the file that needs to be uploaded.
            title (str, optional): Title of the file. Defaults to file_name.
            description (str, optional): Description of the file. Defaults to None.

        Returns:
            File object defined in: https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html#insert
            None if error occurs.

        Raises:
            IOError: If connection error occurs.
        """

        mime_type = magic.Magic(mime=True).from_file(file_name)
        if not title:
            title = file_name
        media_body = apiclient.http.MediaFileUpload(file_name, mimetype=mime_type, resumable=True)
        body = {
            'title': title,
            'description': description,
            'mimeType': mime_type
        }
        try:
            return self.service.files().insert(
                    body=body,
                    media_body=media_body).execute()
        except apiclient.errors.HttpError as error:
            raise IOError(error)
            return None



    def list(self, query=None):
        """ List all files

        Args:
            query (str): The query of the list. The syntax can be found at: https://developers.google.com/drive/web/search-parameters

        Returns:
            A list of File objects defined in: https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html#list

        Reises:
            IOError: If connection error occurs.
        """

        result = []
        page_token = None
        while True:
            try:
                param = { }
                if query:
                    param['q'] = query
                if page_token:
                    param['pageToken'] = page_token
                files = self.service.files().list(**param).execute()
                result.extend(files['items'])
                page_token = files.get('nextPageToken')
                if not page_token:
                    break
            except apiclient.errors.HttpError as error:
                raise IOError(error)
                break
        return result



    def delete(self, file_id):
        """ Delete a file

        Args:
            file_id (str): The ID of the file that needs to be deleted.

        Returns:
            True if succeeded
            False if failed.

        Reises:
            IOError: If connection error occurs.
        """

        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except apiclient.errors.HttpError as error:
            raise IOError(error)
            return False



    def info(self, file_id):
        """ Return the meta info of a file

        Args:
            file_id (str): The ID of the file that needs to be checked.

        Returns:
            File object defined in: https://developers.google.com/resources/api-libraries/documentation/drive/v2/python/latest/drive_v2.files.html#get
            None if error occurs.

        Reises:
            IOError: If connection error occurs.
        """

        try:
            return self.service.files().get(fileId=file_id).execute()
        except apiclient.errors.HttpError as error:
            raise IOError(error)
            return None



    def read(self, file_id):
        """ Return the content of a file
        Args:
            file_id (str): The ID of the file that needs to be checked.

        Returns:
            Str, the content of the file.
            None if error occurs.

        Reises:
            IOError: If connection error occurs.
        """

        try:
            return self.service.files().get_media(fileId=file_id).execute()
        except apiclient.errors.HttpError as error:
            raise IOError(error)
            return None



    def download(self, file_id, local_file_name):
        """ Download a file to local

        Args:
            file_id (str): The ID of the file that needs to be download.
            local_file_name: The path of the destination of the download.

        Returns:
            True if succeeded.
            False if failed.

        Reises:
            IOError: If connection error occurs.
        """

        request = self.service.files().get_media(fileId=file_id)
        with open(local_file_name, 'w+') as local_fd:
            media_request = apiclient.http.MediaIoBaseDownload(local_fd, request)
            while True:
                try:
                    download_progress, done = media_request.next_chunk()
                except apiclient.errors.HttpError as error:
                    raise IOError(error)
                    return False
                if done:
                    return True