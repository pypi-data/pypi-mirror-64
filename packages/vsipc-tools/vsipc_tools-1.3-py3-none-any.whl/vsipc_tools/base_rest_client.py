import aiohttp
from typing import Dict
from urllib.parse import urlencode


class BaseRestApiClient:
    REQUEST_TIMEOUT = 30

    async def make_http_request(self, request_method, url, headers: Dict, data: Dict = None):

        print(f"Request to url {url}")
        async with aiohttp.ClientSession() as session:
            async with session.request(
                    method=request_method, url=url, data=data, headers=headers, timeout=self.REQUEST_TIMEOUT
            ) as response:
                try:
                    return await response.text()
                except aiohttp.ContentTypeError:
                    return dict(raw_content=response.content, status=response.status, headers=response.headers)

    async def get(self, path, headers: Dict = None, **args):
        """
        Make GET HTTP-request
        :param path: str resource to request
        :param headers: dict HTTP request headers
        :param args: URL-parameters
        :return: str response data
        """
        if not headers:
            headers = {}

        params = urlencode(args, True)

        if params:
            url = f"{path}?{params}"
        else:
            url = f"{path}"

        return await self.make_http_request("GET", url=url, headers=headers)

    async def post(self, path, headers=None, body=None):
        """
        Make POST HTTP-request
        :param path: str resource to request
        :param headers: dict HTTP request headers
        :param body: str request body
        :return:
        """
        if not headers:
            headers = {}

        return await self.make_http_request("POST", url=path, headers=headers, data=body)

    async def put(self, path, headers=None, body=None):
        """
        Make PUT HTTP-request
        :param path: str resource to request
        :param headers: dict HTTP request headers
        :param body: str request body
        :return:
        """
        if not headers:
            headers = {}

        return await self.make_http_request("PUT", url=path, headers=headers, data=body)

    async def delete(self, path, headers=None):
        """
        Make DELETE HTTP-request
        :param path: str resource to request
        :param headers: dict HTTP request headers
        :param body: str request body
        :return: tuple(data: str, status_code: int)
        """
        if not headers:
            headers = {}
        return await self.make_http_request("DELETE", url=path, headers=headers)

    async def patch(self, path, headers=None, body=None):
        """
        Make PATCH HTTP-request
        :param path: str resource to request
        :param headers: dict HTTP request headers
        :param body: str request body
        :return:
        """
        if not headers:
            headers = {}

        return await self.make_http_request("PATCH", url=path, headers=headers, data=body)
