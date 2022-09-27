"""This module contains the code for document metadata window."""
from functools import partial

import wx

from .submission_meta_view import EditableListCtrl


class DocumentMetadataView(wx.Frame):
    """The view class for the document metadata window."""
    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name,
                         title='Document Metadata')
        self.metadata = {}

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.checkbox = wx.CheckBox(self, label='Enable',
                                    style=wx.CHK_2STATE)
        self.list_ctrl = EditableListCtrl(
            self, size=(-1, 150), style = wx.LC_REPORT)
        self.save_button = wx.Button(self, label='Save',
                                     name='document_save_btn')

        self.list_ctrl.InsertColumn(0, 'Parameter', width=200)
        self.list_ctrl.InsertColumn(2, 'Value', width=200)

        self.list_ctrl.InsertItem(0, 'Document Name')
        self.list_ctrl.InsertItem(1, 'Document Received Date')
        self.list_ctrl.InsertItem(2, 'Source')
        self.list_ctrl.InsertItem(3, 'Adjudication Level')
        self.list_ctrl.InsertItem(4, 'Section')
        self.list_ctrl.InsertItem(5, 'Exhibit Number')

        self.sizer_elements = [(self.checkbox, 0, wx.ALL | wx.CENTER, 5),
                        (self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5),
                        (self.save_button, 0, wx.ALL | wx.CENTER, 5)]

        self.main_sizer.AddMany(self.sizer_elements)

        self.SetSizerAndFit(self.main_sizer)

    @property
    def get_metadata(self) -> dict:
        """Creates a dictionary with the metadata for the current
        submission."""
        self.metadata['state'] = self.checkbox.GetValue()
        for index in range(0, self.list_ctrl.ItemCount):
            get_text = partial(self.list_ctrl.GetItemText, item=index)
            self.metadata[get_text(col=0)] = get_text(col=1)
        return self.metadata
