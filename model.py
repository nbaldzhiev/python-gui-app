"""This module contains the model class of the application."""
import json


from typing import List, Tuple

from requests import Request, Session
from wx import LogError, LogMessage


class Model:
    """The model class of the application."""

    def __init__(self):
        self.session = Session()

    def prepare_submissions(self, env_url: str, token: str, submissions: dict):
        """Parses the submissions input by the user."""
        endpoint = "api/submissions" if env_url.endswith("/") else "/api/submissions"
        url = env_url + endpoint
        headers = {"Authorization": f"Token {token}"}

        prepared_requests: List[Tuple] = []

        for sub_id, sub_data in submissions.items():
            req = Request(method="POST", url=url, headers=headers)

            data: List[Tuple] = []
            if "meta" in sub_data:
                sub_meta = {}
                external_id = None
                for meta_key, meta_value in sub_data["meta"].items():
                    if meta_key == "state":
                        continue
                    if meta_key == "External ID":
                        external_id = meta_value
                        continue
                    if meta_key == "Priority" or meta_key == "Find Sections":
                        data.append((meta_key.replace(" ", "_").lower(), meta_value))
                        continue
                    sub_meta[meta_key.replace(" ", "_").lower()] = meta_value
                data.extend(
                    [
                        ("submission_metadata", json.dumps(sub_meta)),
                        ("external_id", external_id),
                    ]
                )

            if "documents" in sub_data:
                files: List[Tuple] = []
                for doc in sub_data["documents"].values():
                    if not doc["content"]:
                        del doc
                        continue
                    if "meta" in doc:
                        template = {"sv_labels": []}
                        for meta_key, meta_value in doc["meta"].items():
                            if meta_key == "state":
                                continue
                            template["sv_labels"].append(
                                {"label": meta_key, "value": meta_value}
                            )
                        data.append(("document_metadata", json.dumps(template)))
                    if "content" in doc:
                        try:
                            files.append(("document", open(doc["content"], "rb")))
                        except:
                            LogError(f"Cannot open file {doc['content']}.")

                req.files = files

            if data:
                req.data = data
            preped_req = self.session.prepare_request(req)
            prepared_requests.append((sub_id, preped_req))

        return prepared_requests

    def upload_submissions(self, env_url: str, token: str, submissions: dict):
        """"""
        ssl = True if "https" in env_url else False

        prepared_requests = self.prepare_submissions(
            env_url=env_url.strip(), token=token.strip(), submissions=submissions
        )
        for tup in prepared_requests:
            req = tup[1]
            try:
                if ssl:
                    resp = self.session.send(req, verify=False)
                else:
                    resp = self.session.send(req)
            except:
                LogError(
                    "ERROR !\n"
                    "Please verify the URL and Token are correct"
                    " and also that you have access to the "
                    "desired environment!"
                )
            else:
                if str(resp.status_code).startswith("5"):
                    Model.log_submission_result(
                        sub_id=tup[0], resp_status=resp.status_code
                    )
                    return
                resp_content = json.loads(resp.content)
                Model.log_submission_result(
                    sub_id=tup[0],
                    resp_status=resp.status_code,
                    resp_content=resp_content,
                )

    @staticmethod
    def log_submission_result(
        sub_id=None, resp_status=None, resp_content: dict = None
    ) -> None:
        """Shows a log dialog to the user after a submission request
        has been sent and has a response; this log dialog lets the user
        know what the status of the uploaded submission is."""

        # TODO - move this method to the controller or main view

        if str(resp_status).startswith("2"):
            sub_db_id = resp_content["submission_id"]
            LogMessage(
                f"Submission {sub_id} - SUCCESS !\n"
                f"HTTP Status Code - {resp_status}.\n"
                f"Submission's database id is {sub_db_id}."
            )
        else:
            err_msg = (
                f"Submission {sub_id} - FAILURE !\n"
                + f"HTTP Status Code -  {resp_status}.\n"
            )
            if resp_content:
                err = resp_content["error"]
                err_msg += f'The returned error message is - \n"{err}" .'
            LogMessage(err_msg)
