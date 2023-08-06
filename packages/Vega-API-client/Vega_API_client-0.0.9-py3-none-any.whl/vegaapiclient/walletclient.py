import requests

from typing import Any, Dict, List


class WalletClient(object):

    def __init__(
        self,
        url: str
    ):
        self.token = ""
        self.url = url

        self._httpsession = requests.Session()

    def _header(self) -> Dict[str, Any]:
        if self.token == "":
            raise Exception("not logged in")
        return {"Authorization": "Bearer " + self.token}

    def create(
        self,
        walletname: str,
        passphrase: str
    ) -> requests.Response:
        """
        Create a wallet using a wallet name and a passphrase. If a wallet
        already exists, the action fails. Otherwise, a JWT (json web token) is
        returned.
        """
        req = {
            "wallet": walletname,
            "passphrase": passphrase
        }
        r = self._httpsession.post(self.url + "/api/v1/wallets", json=req)
        if r.status_code != 200:
            self.token = ""
        else:
            self.token = r.json()["Data"]
        return r

    def login(
        self,
        walletname: str,
        passphrase: str
    ) -> requests.Response:
        """
        Log in to an existing wallet. If the wallet does not exist, or if the
        passphrase is incorrect, the action fails. Otherwise, a JWN (json web
        token) is returned.
        """
        req = {
            "wallet": walletname,
            "passphrase": passphrase
        }
        r = self._httpsession.post(
            "{}/api/v1/auth/token".format(self.url), json=req)
        if r.status_code == 200:
            self.token = r.json()["Data"]
        else:
            self.token = ""
        return r

    def logout(self) -> requests.Response:
        """
        Log out from a wallet. The token is deleted from the WalletClient
        object.
        """
        r = self._httpsession.delete(
            "{}/api/v1/auth/token".format(self.url), headers=self._header())
        if r.status_code == 200:
            self.token = ""
        return r

    def getkey(
        self,
        pubKey: str
    ) -> requests.Response:
        """
        Get keypair information (excluding private key).

        pubKey must be a hex-encoded string.
        """
        return self._httpsession.get(
            "{}/api/v1/key/{}".format(self.url, pubKey),
            headers=self._header())

    def taintkey(
        self,
        pubKey: str
    ) -> requests.Response:
        """
        Label a keypair as tainted.

        pubKey must be a hex-encoded string.
        """
        return self._httpsession.put(
            "{}/api/v1/key/{}/taint".format(self.url, pubKey),
            headers=self._header())

    def listkeys(self) -> requests.Response:
        """
        List information (excluding private keys) on all keypairs.
        """
        return self._httpsession.get(
            "{}/api/v1/keys".format(self.url), headers=self._header())

    def generatekey(
        self,
        passphrase: str,
        metadata: List[Dict[str, str]]
    ) -> requests.Response:
        """
        Generate a new keypair with the given metadata.
        """
        req = {
            "passphrase": passphrase,
            "meta": metadata
        }
        return self._httpsession.post(
            "{}/api/v1/keys".format(self.url), json=req,
            headers=self._header())

    def signtx(self, tx, pubKey) -> requests.Response:
        """
        Sign a transaction.

        tx must be a base64-encoded string, e.g.
        tx = base64.b64encode(someBlob).decode("ascii")

        pubKey must be a hex-encoded string.
        """
        req = {
            "tx": tx,
            "pubKey": pubKey,
            "propagate": False
        }
        return self._httpsession.post(
            "{}/api/v1/messages".format(self.url), headers=self._header(),
            json=req)
