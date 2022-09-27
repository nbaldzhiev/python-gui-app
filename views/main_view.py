"""This module contains the code for the main window of the application."""
from typing import List, Tuple

import wx
from wx.adv import HyperlinkCtrl

from .submission_meta_view import SubmissionMetadataView
from .document_meta_view import DocumentMetadataView


MAX_SUBMISSIONS = 10
MAX_DOCUMENTS = 10


class MainView(wx.Frame):
    """Main window of the application."""
    def __init__(self, parent):
        super().__init__(parent=parent, title='Python GUI App')
        self._buffer = []
        self._documents_buffer = {str(i): 0 for i in range(1, MAX_SUBMISSIONS + 1)}
        self.num_of_subs = 1
        self.prev_num_of_subs = 1

        self.fgs = wx.FlexGridSizer(4, 2, 10, 10)
        self.fgs_subs = wx.FlexGridSizer(cols=MAX_SUBMISSIONS, vgap=10, hgap=10)
        self.bs_subs_1 = wx.BoxSizer(wx.VERTICAL)
        for i in range(2, MAX_SUBMISSIONS + 1):
            var_name = f'self.bs_subs_{i}'
            exec(var_name + ' = wx.BoxSizer(wx.VERTICAL)')
        self.bs = wx.BoxSizer(wx.VERTICAL)

        self.url_text = wx.StaticText(self, label='Environment URL:')
        try:
            with open('upload-gui-tool-settings.txt', 'r') as f:
                split = f.read().replace(' ', '').split('|')
                env_url = split[0]
                token = split[1]
        except FileNotFoundError:
            env_url = 'https://default-environment.com'
            token = '897dfe8b2621e040f77ef550cbc58ecad07e763c'
        self.url_ctrl = wx.TextCtrl(self, value=env_url, size=(300, -1), style=wx.TE_PROCESS_ENTER)
        self.token_text = wx.StaticText(self, label='Token:')
        self.token_ctrl = wx.TextCtrl(self, size=(300, -1), style=wx.TE_PROCESS_ENTER, value=token)
        self.send_btn = wx.Button(self, label='Send')
        self.subs_text = wx.StaticText(self, label='Number of Submissions:')
        self.subs_ctrl = wx.SpinCtrl(self, value='1', min=1, max=MAX_SUBMISSIONS)

        ## Create the initial windows for the first submission
        self.sub_1_text = wx.StaticText(self, label='Submission 1:',
                                        name='sub_1_title')
        self.sub_1_meta = wx.Button(self, id=1, label='Metadata',
                                style=wx.BU_EXACTFIT, name='sub_1_btn')
        self.sub_1_dir = wx.CheckBox(self, label='Directory',
                                style=wx.CHK_2STATE, name='sub_1_dir')
        self.sub_1_dir.SetToolTip(tipString=
                'Enable to allow opening (recursively) a directory with documents.')
        self.sub_1_documents = wx.SpinCtrl(self, value='0', min=0,
                            max=MAX_DOCUMENTS, name='sub_1_documents')
        self.sub_1_documents.SetToolTip(tipString=
                            'Enter the number of documents to open.')
        SubmissionMetadataView(None, 'sub_1_view')
        #

        self.fgs_elements: List[Tuple] = \
            [(self.url_text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
             (self.url_ctrl),
             (self.token_text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
             (self.token_ctrl),
             (self.subs_text, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
             (self.subs_ctrl),
             (self.send_btn, 0, wx.ALIGN_LEFT)]
        self.bs_subs_elements: List[Tuple] = \
            [(self.sub_1_text, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (self.sub_1_meta, 0, wx.ALIGN_CENTER_HORIZONTAL),
             (self.sub_1_dir, 0, wx.ALIGN_CENTER_HORIZONTAL),
             (self.sub_1_documents, 0, wx.ALIGN_CENTER_HORIZONTAL)]
        self.bs_elements: List[Tuple] = [(self.fgs, 1, wx.EXPAND | wx.ALL, 5),
                            (self.fgs_subs, 0, wx.EXPAND | wx.ALL, 5)]

        self.fgs.AddMany(self.fgs_elements)
        self.bs_subs_1.Add(wx.StaticLine(self, wx.LI_VERTICAL,
                                         name="self.static_line_1"))
        self.bs_subs_1.AddMany(self.bs_subs_elements)
        self.fgs_subs.Add(self.bs_subs_1)
        for i in range(2, MAX_SUBMISSIONS + 1):
            var_name = f'self.bs_subs_{i}'
            exec(f'self.bs_subs_{i}.Add(wx.StaticLine(self, wx.LI_VERTICAL, name="self.static_line_{i}"))')
            self.fgs_subs.Add(eval(var_name))
        self.bs.AddMany(self.bs_elements)

        self.SetSizerAndFit(self.bs)

    def create_submissions(self) -> None:
        """Creates the necessary amount of submission texts, metadata
        buttons and metadata windows."""
        for i in range(self.prev_num_of_subs + 1, self.num_of_subs + 1):
            wx.StaticText(self, label=f'Submission {i}:', name=f'sub_{i}_title')
            wx.Button(self, label='Metadata', style=wx.BU_EXACTFIT,
                      name=f'sub_{i}_btn')
            wx.CheckBox(self, label='Directory', style=wx.CHK_2STATE,
                        name=f'sub_{i}_dir').SetToolTip(
                tipString='Enable to allow opening (recursively) a directory with documents.')
            wx.SpinCtrl(self, value='0', min=0, max=MAX_DOCUMENTS,
                        name=f'sub_{i}_documents').SetToolTip(
                tipString='Enter the number of documents to open')
            SubmissionMetadataView(None, f"sub_{i}_view")

            var_name = f'self.bs_subs_{i}'
            exec(var_name + ".Add(wx.StaticText.FindWindowByName(f'sub_{i}_title'), 0, wx.ALIGN_CENTER_HORIZONTAL)")
            exec(var_name + ".Add(wx.Button.FindWindowByName(f'sub_{i}_btn'), 0, wx.ALIGN_CENTER_HORIZONTAL)")
            exec(var_name + ".Add(wx.CheckBox.FindWindowByName(f'sub_{i}_dir'), 0, wx.ALIGN_CENTER_HORIZONTAL)")
            exec(var_name + ".Add(wx.SpinCtrl.FindWindowByName(f'sub_{i}_documents'), 0, wx.ALIGN_CENTER_HORIZONTAL)")
            exec(f'self.bs_subs_{i}.Fit(self)')

        self.bs.Fit(self)

    def delete_submissions(self) -> None:
        """Deletes the necessary amount of submission texts, metadata
        buttons and metadata windows."""
        for i in range(self.prev_num_of_subs, self.num_of_subs, -1):
            num_of_docs = wx.SpinCtrl.FindWindowByName(f'sub_{i}_documents').GetValue()

            wx.StaticText.FindWindowByName(f'sub_{i}_title').Destroy()
            wx.Button.FindWindowByName(f'sub_{i}_btn').Destroy()
            if wx.CheckBox.FindWindowByName(f'sub_{i}_dir').IsChecked():
                HyperlinkCtrl.FindWindowByName(f'sub_{i}_dir_link').Destroy()
            wx.CheckBox.FindWindowByName(f'sub_{i}_dir').Destroy()
            wx.Button.FindWindowByName(f'sub_{i}_documents').Destroy()
            wx.Frame.FindWindowByName(f"sub_{i}_view").Destroy()

            # Delete document objects
            for j in range(1, num_of_docs + 1):
                HyperlinkCtrl.FindWindowByName(f'sub_{i}_link_{j}').Destroy()
                wx.Button.FindWindowByName(f'sub_{i}_meta_{j}').Destroy()
                wx.Frame.FindWindowByName(f"sub_{i}_meta_{j}_view").Destroy()
            self._documents_buffer[str(i)] = 0

        self.bs.Fit(self)

    def create_documents(self, num_of_docs: int, id: str) -> None:
        """Creates the necessary amount of document links, specified by
         num_of_docs, for a given submission, specified by id."""
        current_number = self._documents_buffer[id]
        for i in range(current_number + 1, num_of_docs + 1):
            HyperlinkCtrl(self, label=f'Document {i}', name=f'sub_{id}_link_{i}')
            wx.Button(self, label='Metadata', style=wx.BU_EXACTFIT,
                      name=f'sub_{id}_meta_{i}')
            DocumentMetadataView(None, f"sub_{id}_meta_{i}_view")

            exec(f"self.bs_subs_{id}.Add(HyperlinkCtrl.FindWindowByName(f'sub_{id}_link_{i}'), 0, wx.ALIGN_CENTER_HORIZONTAL)")
            exec(f"self.bs_subs_{id}.Add(wx.Button.FindWindowByName(f'sub_{id}_meta_{i}'), 0, wx.ALIGN_CENTER_HORIZONTAL)")

        exec(f'self.bs_subs_{id}.Fit(self)')
        self.bs.Fit(self)

    def delete_documents(self, num_of_docs: int, id: str) -> None:
        """Deletes the necessary amount of document links, specified by
         num_of_docs, for a given submission, specified by id."""
        current_number = self._documents_buffer[id]
        for i in range(current_number, num_of_docs, -1):
            HyperlinkCtrl.FindWindowByName(f'sub_{id}_link_{i}').Destroy()
            wx.Button.FindWindowByName(f'sub_{id}_meta_{i}').Destroy()
            wx.Frame.FindWindowByName(f"sub_{id}_meta_{i}_view").Destroy()

        self.bs.Fit(self)

    def create_dir(self, id: str) -> None:
        """Creates a directory link for a given submission, specified
         by id."""
        HyperlinkCtrl(self, label=f'Directory', name=f'sub_{id}_dir_link')
        exec(f"self.bs_subs_{id}.Add(HyperlinkCtrl.FindWindowByName(f'sub_{id}_dir_link'), 0, wx.ALIGN_CENTER_HORIZONTAL)")

        exec(f'self.bs_subs_{id}.Fit(self)')
        self.bs.Fit(self)

    def delete_dir(self, id: str) -> None:
        """Deletes a directory link for a given submission, specified
         by id."""
        HyperlinkCtrl.FindWindowByName(f'sub_{id}_dir_link').Destroy()

        self.bs.Fit(self)

