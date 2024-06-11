import typing as t
import os
import json

import requests


class PinataApi:
    @property
    def base_url(self) -> str:
        return "https://api.pinata.cloud"

    @property
    def auth_token(self) -> str:
        return os.getenv("pinata_jwt")

    def get_headers(self, content_type: t.Literal["json", "form"] = "json"):
        headers = {
            "authorization": f"Bearer {self.auth_token}",
        }

        if content_type == "json":
            headers["Content-Type"] = "application/json"

        elif content_type == "form":
            headers["Content-Type"] = "multipart/form-data"
        return headers

    def check_auth(self):
        return requests.get(
            url=f"{self.base_url}/data/testAuthentication", headers=self.get_headers()
        )

    def pin_json(
        self,
        file_name: str,
        json_data: t.Dict[str, t.Any],
        tags: t.Dict[str, t.Any] = None,
        options: t.Dict[str, t.Any] = None,
    ):
        pinata_metadata = {"name": file_name}

        if tags:
            pinata_metadata["keyvalues"] = tags

        data = (
            f"file={json.dumps(json_data)}pinataMetadata={json.dumps(pinata_metadata)}"
        )

        if options:
            data += f"pinataOptions={json.dumps(options)}"

        res = requests.post(
            url=f"{self.base_url}/pinning/pinJSONToIPFS",
            headers=self.get_headers(),
            json={
                "pinataContent": json_data,
                "pinataMetadata": pinata_metadata,
                "pinataOptions": options,
            },
        )

        assert res.status_code == 200
        return res
