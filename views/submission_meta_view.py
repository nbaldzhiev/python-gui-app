"""This module contains the code for the submission metadata window."""
from functools import partial

import wx
from wx.lib.mixins.listctrl import TextEditMixin


class EditableListCtrl(wx.ListCtrl, TextEditMixin):
    """A class for creating Editable ListCtrl objects"""

    def __init__(
        self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0
    ):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        TextEditMixin.__init__(self)


class SubmissionMetadataView(wx.Frame):
    """The view class for the submission metadata window."""

    def __init__(self, parent, name):
        super().__init__(parent=parent, name=name, title="Submission Metadata")
        self.metadata = {}

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self.checkbox = wx.CheckBox(self, label="Enable", style=wx.CHK_2STATE)
        self.list_ctrl = EditableListCtrl(self, size=(-1, 200), style=wx.LC_REPORT)
        self.save_button = wx.Button(self, label="Save", name="sub_save_btn")

        self.list_ctrl.InsertColumn(0, "Parameter", width=200)
        self.list_ctrl.InsertColumn(2, "Value", width=200)

        self.list_ctrl.InsertItem(0, "Folder Number")
        self.list_ctrl.InsertItem(1, "Claimant Name")
        self.list_ctrl.InsertItem(2, "Claimant SSN")
        self.list_ctrl.InsertItem(3, "Submitted By Email")
        self.list_ctrl.InsertItem(4, "Priority")
        self.list_ctrl.InsertItem(5, "Find Sections")
        self.list_ctrl.InsertItem(6, "External ID")

        self.sizer_elements = [
            (self.checkbox, 0, wx.ALL | wx.CENTER, 5),
            (self.list_ctrl, 0, wx.ALL | wx.EXPAND, 5),
            (self.save_button, 0, wx.ALL | wx.CENTER, 5),
        ]

        self.main_sizer.AddMany(self.sizer_elements)

        self.SetSizerAndFit(self.main_sizer)

    @property
    def get_metadata(self) -> dict:
        """Creates a dictionary with the metadata for the current
        submission."""
        self.metadata["state"] = self.checkbox.GetValue()
        for index in range(0, self.list_ctrl.ItemCount):
            get_text = partial(self.list_ctrl.GetItemText, item=index)
            self.metadata[get_text(col=0)] = get_text(col=1)
        return self.metadata
