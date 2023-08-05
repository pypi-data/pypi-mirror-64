import requests
from requests.exceptions import Timeout
from .errors import UnauthorizedException, NotFoundException, InternalServerErrorException


class Client(requests.Session):
    def __init__(self, verify_ssl):
        super().__init__()
        self.verify_ssl = verify_ssl

    def request(self, method, url, *args, **kwargs):
        res = super().request(method, url, verify=self.verify_ssl, *args, **kwargs)

        if res.status_code == 401:
            raise UnauthorizedException(message=f"Unauthorized when {method} data to {url}")
        elif res.status_code == 404:
            raise NotFoundException(message=f"Not found when {method} data to {url}")
        elif res.status_code == 500:
            raise InternalServerErrorException()
        return res
