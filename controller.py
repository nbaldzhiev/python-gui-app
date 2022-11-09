"""This module contains the controller functionalities of the app."""
import copy
import glob
import re

import wx
from wx.adv import EVT_HYPERLINK, HyperlinkCtrl

from model import Model
from views import MAX_DOCUMENTS, MAX_SUBMISSIONS, MainView


class Controller:
    """This class represents the controller of the app."""

    def __init__(self):
        ## leaving this as it is a decent candidate for project's ugliest line of code
        self.submissions = {
            str(i): {
                "meta": {},
                "documents": {
                    str(j): {"content": "", "meta": {}}
                    for j in range(1, MAX_DOCUMENTS + 1)
                },
            }
            for i in range(1, MAX_SUBMISSIONS + 1)
        }
        #
        self.colour_db = wx.ColourDatabase()
        self.model = Model()
        self.main_view = MainView(None)

        self.main_view.Bind(wx.EVT_CLOSE, self.on_main_view_close)
        self.main_view.subs_ctrl.Bind(wx.EVT_SPINCTRL, self.manage_submissions)
        self.main_view.send_btn.Bind(wx.EVT_BUTTON, self.on_send_click)
        wx.Button.FindWindowByName("sub_1_btn").Bind(wx.EVT_BUTTON, self.show_sub_meta)
        wx.CheckBox.FindWindowByName("sub_1_dir").Bind(
            wx.EVT_CHECKBOX, self.on_dir_checkbox_click
        )
        wx.Frame.FindWindowByName(f"sub_1_view").save_button.Bind(
            wx.EVT_BUTTON, self.on_sub_meta_save
        )
        wx.Frame.FindWindowByName(f"sub_1_view").Bind(
            wx.EVT_CLOSE, self.on_sub_meta_close
        )
        wx.SpinCtrl.FindWindowByName("sub_1_documents").Bind(
            wx.EVT_SPINCTRL, self.manage_documents
        )
        self.main_view.Show()

    def on_send_click(self, event):
        """Event handler for when the send button is clicked."""
        # TODO - refactor this method!!! quite the spaghetti now

        env_url = self.main_view.url_ctrl.GetValue()
        token = self.main_view.token_ctrl.GetValue()
        num_of_subs = self.main_view.subs_ctrl.GetValue()
        submissions = copy.deepcopy(self.submissions)

        # trim the submissions dict's leftover submissions
        for i in range(int(num_of_subs) + 1, MAX_SUBMISSIONS + 1):
            del submissions[str(i)]

        # trim the submissions dict's leftover submission documents
        for i in range(1, num_of_subs + 1):
            if not wx.Frame.FindWindowByName(f"sub_{str(i)}_view").checkbox.IsChecked():
                del submissions[str(i)]["meta"]
            if wx.CheckBox.FindWindowByName(f"sub_{str(i)}_dir").IsChecked():
                docs_len = len(submissions[str(i)]["documents"])
                for j in range(1, docs_len + 1):
                    if submissions[str(i)]["documents"][str(j)]["content"] != "":
                        continue
                    else:
                        del submissions[str(i)]["documents"][str(j)]
                        continue
                if len(submissions[str(i)]["documents"]) == 0:
                    del submissions[str(i)]["documents"]
            else:
                num_of_docs = wx.SpinCtrl.FindWindowByName(
                    f"sub_{i}_documents"
                ).GetValue()

                if num_of_docs == 0 and "meta" not in submissions[str(i)]:
                    submissions[str(i)] = {}
                    continue
                elif num_of_docs == 0 and "meta" in submissions[str(i)]:
                    del submissions[str(i)]["documents"]
                    continue

                for j in range(1, int(num_of_docs) + 1):
                    if (
                        submissions[str(i)]["documents"][str(j)]["content"] == ""
                        and not wx.Frame.FindWindowByName(
                            f"sub_{str(i)}_meta_{str(j)}_view"
                        ).checkbox.IsChecked()
                    ):
                        del submissions[str(i)]["documents"][str(j)]
                    elif (
                        submissions[str(i)]["documents"][str(j)]["content"] != ""
                        and not wx.Frame.FindWindowByName(
                            f"sub_{str(i)}_meta_{str(j)}_view"
                        ).checkbox.IsChecked()
                    ):
                        del submissions[str(i)]["documents"][str(j)]["meta"]
                    elif (
                        submissions[str(i)]["documents"][str(j)]["content"] == ""
                        and wx.Frame.FindWindowByName(
                            f"sub_{str(i)}_meta_{str(j)}_view"
                        ).checkbox.IsChecked()
                    ):
                        del submissions[str(i)]["documents"][str(j)]["content"]

                for j in range(int(num_of_docs) + 1, MAX_DOCUMENTS + 1):
                    del submissions[str(i)]["documents"][str(j)]

                if (
                    len(submissions[str(i)]["documents"]) == 0
                    and "meta" not in submissions[str(i)]
                ):
                    submissions[str(i)] = {}
                elif (
                    len(submissions[str(i)]["documents"]) == 0
                    and "meta" in submissions[str(i)]
                ):
                    del submissions[str(i)]["documents"]

        self.model.upload_submissions(
            env_url=env_url, token=token, submissions=submissions
        )
        try:
            with open("upload-gui-tool-settings.txt", "r") as f:
                if f.read() != env_url + " | " + token:
                    raise FileNotFoundError
        except FileNotFoundError:
            with open("upload-gui-tool-settings.txt", "w") as f:
                f.write(env_url + " | " + token)

    def manage_submissions(self, event) -> None:
        """Manages creation, deletion and binding of all submission
        widgets."""
        self.main_view.num_of_subs = self.main_view.subs_ctrl.GetValue()
        try:
            self.main_view.prev_num_of_subs = self.main_view._buffer[
                len(self.main_view._buffer) - 1
            ]
        except:
            self.main_view.prev_num_of_subs = 1

        if self.main_view.num_of_subs >= self.main_view.prev_num_of_subs:
            self.main_view.create_submissions()
        elif self.main_view.num_of_subs < self.main_view.prev_num_of_subs:
            self.main_view.delete_submissions()

        self.bind_sub_meta()

        self.main_view._buffer.append(self.main_view.num_of_subs)

        event.Skip()

    def bind_sub_meta(self) -> None:
        """Creates all necessary bindings in the submission metadata
        window."""
        for i in range(
            self.main_view.prev_num_of_subs + 1, self.main_view.num_of_subs + 1
        ):
            wx.Button.FindWindowByName(f"sub_{i}_btn").Bind(
                wx.EVT_BUTTON, self.show_sub_meta
            )
            wx.Frame.FindWindowByName(f"sub_{i}_view").save_button.Bind(
                wx.EVT_BUTTON, self.on_sub_meta_save
            )
            wx.Frame.FindWindowByName(f"sub_{i}_view").Bind(
                wx.EVT_CLOSE, self.on_sub_meta_close
            )
            wx.CheckBox.FindWindowByName(f"sub_{i}_dir").Bind(
                wx.EVT_CHECKBOX, self.on_dir_checkbox_click
            )
            wx.SpinCtrl.FindWindowByName(f"sub_{i}_documents").Bind(
                wx.EVT_SPINCTRL, self.manage_documents
            )

    def show_sub_meta(self, event) -> None:
        """Event handler for when a user clicks on a submission
        metadata button."""
        id = re.search(r"sub_([0-9]+)_", event.GetEventObject().GetName()).group(1)
        event.GetEventObject().SetForegroundColour(self.colour_db.Find("GREY"))
        wx.Frame.FindWindowByName(f"sub_{id}_view").Show()

    @staticmethod
    def on_sub_meta_save(event) -> None:
        """Event handler for when a user clicks on a submission
        metadata save button."""
        event.GetEventObject().GetParent().Close(False)

    def on_sub_meta_close(self, event) -> None:
        """Event handler for when a user closes a submission metadata
        window."""
        id = re.search(r"sub_([0-9]+)_v", event.GetEventObject().GetName()).group(1)
        sub_meta = event.GetEventObject().get_metadata
        self.submissions[id]["meta"] = sub_meta
        event.GetEventObject().Hide()

    def on_dir_checkbox_click(self, event) -> None:
        """Event handler for when a 'Directory' checkbox is clicked"""
        id = re.search(r"sub_([0-9]+)_dir", event.GetEventObject().GetName()).group(1)
        if event.GetEventObject().IsChecked():
            wx.SpinCtrl.FindWindowByName(f"sub_{id}_documents").Disable()
            self.main_view.delete_documents(num_of_docs=0, id=id)
            wx.SpinCtrl.FindWindowByName(f"sub_{id}_documents").SetValue("0")
            self.main_view._documents_buffer[str(id)] = 0
            self.main_view.create_dir(id=id)
            HyperlinkCtrl.FindWindowByName(f"sub_{id}_dir_link").Bind(
                EVT_HYPERLINK, self.open_dir_dialog
            )
        else:
            wx.SpinCtrl.FindWindowByName(f"sub_{id}_documents").Enable()
            for doc in self.submissions[id]["documents"].values():
                doc["content"] = ""
            self.main_view.delete_dir(id=id)

    def manage_documents(self, event) -> None:
        """Manages creation and deletion of document links corresponding
        to a submission."""
        id = re.search(r"sub_([0-9]+)_doc", event.GetEventObject().GetName()).group(1)
        num_of_docs = event.GetEventObject().GetValue()

        current_number = self.main_view._documents_buffer[id]
        if num_of_docs >= self.main_view._documents_buffer[id]:
            self.main_view.create_documents(num_of_docs=num_of_docs, id=id)
        elif num_of_docs < self.main_view._documents_buffer[id]:
            self.main_view.delete_documents(num_of_docs=num_of_docs, id=id)
            for i in range(current_number, num_of_docs, -1):
                self.submissions[id]["documents"][str(i)]["content"] = ""

        self.bind_doc_meta(num_of_docs=num_of_docs, id=id)

        self.main_view._documents_buffer[id] = num_of_docs

    def bind_doc_meta(self, num_of_docs: int, id: str) -> None:
        """Creates all necessary bindings for a document metadata."""
        current_number = self.main_view._documents_buffer[id]
        for i in range(current_number + 1, num_of_docs + 1):
            HyperlinkCtrl.FindWindowByName(f"sub_{id}_link_{i}").Bind(
                EVT_HYPERLINK, self.open_file_dialog
            )
            wx.Button.FindWindowByName(f"sub_{id}_meta_{i}").Bind(
                wx.EVT_BUTTON, self.show_doc_meta
            )
            wx.Frame.FindWindowByName(f"sub_{id}_meta_{i}_view").save_button.Bind(
                wx.EVT_BUTTON, self.on_doc_meta_save
            )
            wx.Frame.FindWindowByName(f"sub_{id}_meta_{i}_view").Bind(
                wx.EVT_CLOSE, self.on_doc_meta_close
            )

    def show_doc_meta(self, event) -> None:
        """Event handler for when a user clicks on a submission
        metadata button."""
        ids = re.search(
            r"sub_([0-9]+)_meta_([0-9]+)", event.GetEventObject().GetName()
        ).groups()
        wx.Frame.FindWindowByName(f"sub_{ids[0]}_meta_{ids[1]}_view").Show()
        wx.Button.FindWindowByName(f"sub_{ids[0]}_meta_{ids[1]}").SetForegroundColour(
            self.colour_db.Find("GREY")
        )

    @staticmethod
    def on_doc_meta_save(event) -> None:
        """Event handler for when a user clicks on a document
        metadata save button."""
        event.GetEventObject().GetParent().Close(False)

    def on_doc_meta_close(self, event) -> None:
        """Event handler for when a user closes a document metadata
        window."""
        ids = re.search(
            r"sub_([0-9]+)_meta_([0-9]+)", event.GetEventObject().GetName()
        ).groups()
        doc_meta = event.GetEventObject().get_metadata
        self.submissions[ids[0]]["documents"][ids[1]]["meta"] = doc_meta
        event.GetEventObject().Hide()

    def open_file_dialog(self, event) -> None:
        """Event handler for opening a file dialog for opening files."""
        ids = re.search(
            r"sub_([0-9]+)_link_([0-9]+)", event.GetEventObject().GetName()
        ).groups()
        HyperlinkCtrl.FindWindowByName(f"sub_{ids[0]}_link_{ids[1]}").SetVisitedColour(
            self.colour_db.Find("GREY")
        )
        with wx.FileDialog(
            None,
            "Open Document File",
            wildcard="PDF files and TIFF files (*.pdf;*.tiff)|*.pdf;*.tif|"
            "Any files (*.*)|*.*",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = fileDialog.GetPath()
            self.submissions[ids[0]]["documents"][ids[1]]["content"] = pathname

    def open_dir_dialog(self, event) -> None:
        """Event handler for opening a directory dialog for opening directorys."""
        id = re.search(r"sub_([0-9]+)_dir", event.GetEventObject().GetName()).group(1)
        HyperlinkCtrl.FindWindowByName(f"sub_{id}_dir_link").SetVisitedColour(
            self.colour_db.Find("GREY")
        )
        with wx.DirDialog(
            None,
            "Open Documents Directory",
            style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST,
        ) as dirDialog:

            if dirDialog.ShowModal() == wx.ID_CANCEL:
                return

            pathname = dirDialog.GetPath()
            # TODO - improve the way files are matched
            files_paths: list = (
                glob.glob(pathname=pathname + "/**/*.pdf", recursive=True)
                + glob.glob(pathname=pathname + "/**/*.tif", recursive=True)
                + glob.glob(pathname=pathname + "/**/*.tiff", recursive=True)
            )

            for path in files_paths:
                ix = str(files_paths.index(path) + 1)
                self.submissions[id]["documents"][ix] = {"content": path, "meta": {}}

    def on_main_view_close(self, event) -> None:
        """Event handler for when a user closes the main app window."""
        if (
            wx.MessageBox(
                "Do you really want to close the application?",
                "Please confirm",
                wx.ICON_QUESTION | wx.YES_NO,
            )
            != wx.YES
        ):

            event.Veto()
            return

        self.main_view.Destroy()
