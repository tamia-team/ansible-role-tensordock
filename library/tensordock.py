#!/usr/bin/python
import requests
from ansible.module_utils.basic import AnsibleModule

import logging
import requests

LOGGER = logging.getLogger(__name__)

class TensordockAPIServerClient:
    """A client for interacting with the Tensordock API Server."""

    BASE_API_URL = 'https://marketplace.tensordock.com/api/v1'

    def __init__(self, api_key: str, api_token: str, server_id: str):
        """
        Initialize the TensordockAPIServerClient.

        Args:
            api_key (str): The API key for Tensordock.
            api_token (str): The API token for Tensordock.
            server_id (str): The server ID for Tensordock.
        """
        self.api_key: str = api_key
        self.api_token: str = api_token
        self.server_id: str = server_id

    @staticmethod
    def get_url(relative_path: str):
        """Construct the full API URL based on a relative path.

        Args:
            relative_path (str): A relative path to the specific API endpoint.

        Returns:
            str: The full URL to the API endpoint.
        """
        return f'{TensordockAPIServerClient.BASE_API_URL}{relative_path}'

    def server_start(self):
        """Starts the server specified by server_id.

        Returns:
            requests.Response: The response object from the API request.
        """
        try:
            url = self.get_url('/client/start/single')
            payload = {
                'api_key': self.api_key,
                'api_token': self.api_token,
                'server': self.server_id,
            }
            print(payload)
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            LOGGER.error(f'HTTP error occurred: {e}')
            print(e)
            raise
        except Exception as e:
            LOGGER.error(f'Error occurred: {e}')
            raise

    def server_stop(self, release_gpu: bool = True):
        """Stops the server specified by server_id.

        Args:
            release_gpu (bool, optional): Specifies whether to release the GPU resources. Defaults to True.

        Returns:
            requests.Response: The response object from the API request.
        """
        try:
            url = self.get_url('/client/stop/single')
            payload = {
                'api_key': self.api_key,
                'api_token': self.api_token,
                'server': self.server_id,
                'disassociate_resources': release_gpu,
            }
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            LOGGER.error(f'HTTP error occurred: {e}')
            raise
        except Exception as e:
            LOGGER.error(f'Error occurred: {e}')
            raise

    def server_details(self):
        """Fetches details of the server specified by server_id.

        Returns:
            requests.Response: The response object from the API request.
        """
        try:
            url = self.get_url('/client/get/single')
            payload = {
                'api_key': self.api_key,
                'api_token': self.api_token,
                'server': self.server_id,
            }
            headers = {}
            response = requests.request("POST", url, headers=headers, data=payload)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as e:
            LOGGER.error(f'HTTP error occurred: {e}')
            raise
        except Exception as e:
            LOGGER.error(f'Error occurred: {e}')
            raise


def main():
    module = AnsibleModule(
        argument_spec=dict(
            api_key=dict(required=True, type='str'),
            api_token=dict(required=True, type='str', no_log=True),
            server=dict(required=True, type='str'),
            state=dict(default='start', choices=['start', 'stop'])
        ),
        supports_check_mode=True
    )

    api_key = module.params['api_key']
    api_token = module.params['api_token']
    server = module.params['server']
    state = module.params['state']

    if state == 'start':
        result = server_start(api_key, api_token, server)
    elif state == 'details_server':
        result = server_details(api_key, api_token, server)
    else:
        result = server_stop(api_key, api_token, server)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
