import urllib
from urllib.request import Request
from urllib.error import HTTPError
import json
import logging
from Activeconnect.status import Status
from Activeconnect.hmac import make_authentication_headers

logger = logging.getLogger("activeconnect")


class Session:
    """
        Represents an Activeconnect session.

        Attributes:

            authenticated (bool): True if the authentication request was successful (does not indicate authentication status).
            failure_reason (str): If authenticated is False indicates the reason for failure.
            session_status (Status): The status of the session - a value of Session.pending indicates authentication is in progress.
            session_token (str): Identifies the session.
            session_secret (str): Secret used to authenticate REST calls to Activeconnect service.
            status_url (str): The URL to call to get the status of the session.
            logout_url (str): The URL to call to destroy the session.

    """

    @property
    def failed(self):
        return self.session_status in [Status.failed, Status.timeout, Status.cancelled]

    @property
    def in_progress(self):
        return self.session_status in [Status.pending,Status.identifying]

    @property
    def active(self):
        return self.session_status == Status.active

    def __init__(self, session_data: dict):
        """
            The constructor for Session class.

            Parameters:
                session_data (dict): The data returned from a call to the Activeconnect authenticate_user API.
        """
        authentication_status = session_data.get("authentication_status")

        if authentication_status is None:
            raise ValueError("session_data does not contain the authentication_status key")

        authenticated = authentication_status.get("authenticated")

        self.authenticated = False
        self.failure_reason = ""
        self.session_status = Status[authentication_status["session_status"]]
        if authenticated:
            self.status_url = authentication_status["status_url"]
            self.session_token = authentication_status["session_token"]
            self.session_secret = authentication_status["session_secret"]
            self.logout_url = authentication_status["logout_url"]
        else:
            self.status_url = None
            self.session_token = None
            self.session_secret = None
            self.logout_url = None
            self.failure_reason = authentication_status["reason"]

    def get_status(self ):
        """
            Get the status of the session.

            Calls the Activeconnect service to get the status of the session.

            Returns:
            Status: The status of the session.

            """

        headers = make_authentication_headers(client_id=self.session_token,
                                                   client_shared_secret=self.session_secret,
                                                   request_uri=self.status_url)
        headers["Content-Type"] = "application/json"

        req = urllib.request.Request(self.status_url, headers=headers, method='GET')

        try:
            auth_response = urllib.request.urlopen(req)
            if 200 <= auth_response.code < 300:
                d = auth_response.read()
                j = json.loads(d)
                auth_status = j.get('authentication_status')
                self.session_status = auth_status['session_status']
                return self.session_status
        except HTTPError as ex:
            logger.warning("get status failed {}".format(ex))
        return Status.failed

    def destroy(self):
        """
            Terminates the session.

            Calls the Activeconnect service to terminate this session.

            Returns:
            Boolean: True of the session was destroyed otherwise False.

            """

        headers = make_authentication_headers(client_id=self.session_token,
                                                   client_shared_secret=self.session_secret,
                                                   request_uri=self.logout_url)
        headers["Content-Type"] = "application/json"

        req = urllib.request.Request(self.logout_url, headers=headers, method='POST')

        try:
            destroy_response = urllib.request.urlopen(req)
            if 200 <= destroy_response.code < 300:
                body = destroy_response.read()
                j = json.loads(body)

                destroyed = j.get('status')

                if destroyed is None:
                    destroyed = False

                return destroyed
        except HTTPError as ex:
            logger.warning("destroy session failed {}".format(ex))

        return False
