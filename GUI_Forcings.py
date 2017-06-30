import os 
import wx
import netCDF4
import Forcings as f

selected_file = []

class DemoPanel(wx.Panel):

    def __init__(self, parent, *args, **kwargs):
        """Create the DemoPanel."""
        global selected_file
        wx.Panel.__init__(self, parent, *args, **kwargs)

        self.parent = parent  # Sometimes one can use inline Comments

        self.heading = wx.StaticText(self, -1,"Input NetCDF File:", style=wx.ALIGN_LEFT)
        self.file_opened = wx.TextCtrl(self, -1, "")
##        sampleList = ['Hey','Hi','Hello','test','try','final:)']
        
        Sizer = wx.BoxSizer(wx.VERTICAL)
        
        BrowseBtn = wx.Button(self,-1, label="Browse")
        BrowseBtn.Bind(wx.EVT_BUTTON, self.onDir )
        Sizer.Add(BrowseBtn, 0, wx.ALIGN_RIGHT|wx.ALL)

        Sizer.Add(self.file_opened,0, wx.EXPAND )
        
        self.combo = wx.ComboBox(self, size = wx.DefaultSize, choices=[])
##        self.text = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)
        self.widgetMaker(self.combo, [])
        
        self.param = wx.StaticText(self, -1,"Parameters", style=wx.ALIGN_LEFT)
        Sizer.Add(self.param,0, wx.ALIGN_LEFT)

        Sizer.Add(self.combo, 0, wx.ALIGN_LEFT )
##        self.combo = wx.ComboBox(self, size = wx.DefaultSize, choices=sampleList)

        OkBtn = wx.Button(self,-1, label="Ok")
        OkBtn.Bind(wx.EVT_BUTTON, self.file_selected )
        Sizer.Add(OkBtn, 0, wx.ALIGN_LEFT|wx.ALL)
        
        self.date = wx.StaticText(self, -1,"Enter date(e.g. 13/05/2005--13/06/2005):   ")
        Sizer.Add(self.date,0, wx.ALIGN_RIGHT)

        self.select_date = wx.TextCtrl(self, -1, "")
        Sizer.Add(self.select_date,0, wx.ALIGN_RIGHT)

        self.format = wx.StaticText(self, -1,"Enter desired time format (3/6/12/24):   ")
        Sizer.Add(self.format,0, wx.ALIGN_RIGHT)
        
        self.select_format = wx.TextCtrl(self, -1, "")
        Sizer.Add(self.select_format,0, wx.ALIGN_RIGHT)       

        self.temp_format = wx.StaticText(self, -1,"Enter 0 for Tmax/Tmin or 1 for Avg Temp:   ")
        Sizer.Add(self.temp_format,0, wx.ALIGN_RIGHT)
        
        self.select_temp = wx.TextCtrl(self, -1, "")
        Sizer.Add(self.select_temp,0, wx.ALIGN_RIGHT)

        OkBtn1 = wx.Button(self,-1, label="Ok")
        OkBtn1.Bind(wx.EVT_BUTTON, self.option_select)
        Sizer.Add(OkBtn1, 0, wx.ALIGN_RIGHT|wx.ALL)
        
        self.disp = wx.StaticText(self, -1, "Parameters selected from each file:\n", style=wx.ALIGN_CENTRE)
        Sizer.Add(self.disp,-1, wx.EXPAND)
        
        self.select_param = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        Sizer.Add(self.select_param,2, wx.EXPAND)

        self.output_folder = wx.StaticText(self, -1,"Output Directory:")
        Sizer.Add(self.output_folder,0, wx.ALIGN_LEFT)
        self.out_directory = wx.TextCtrl(self, -1, "")
        Sizer.Add(self.out_directory,0, wx.EXPAND)

        BrowseBtn2 = wx.Button(self,-1, label="Browse")
        BrowseBtn2.Bind(wx.EVT_BUTTON, self.outDir )
        Sizer.Add(BrowseBtn2, 0, wx.ALIGN_RIGHT|wx.ALL)

        RunBtn = wx.Button(self, -1, label="Run")
##        RunBtn.Bind(wx.EVT_BUTTON, ##Event here)
        Sizer.Add(RunBtn,0, wx.ALIGN_CENTRE)
        
        self.SetSizer(Sizer)

    def option_select(self, event):
        f.entered_date(self.select_date.GetValue())
        f.desired_time_format(self.select_format.GetValue())
        f.choice_for_temp(self.select_temp.GetValue())

    def file_selected(self, event):
        global selected_file
        f.addtoFiles(selected_file)
        selected_file = map(lambda x: x.encode('ascii','replace'), selected_file)
        
        self.select_param.AppendText(str(selected_file[0])+" - "+str(selected_file[1:])+"\n")
        
    def widgetMaker(self, widget, objects):
        widget.Bind(wx.EVT_COMBOBOX, self.onSelect)

    def onSelect(self, event):
        global selected_file
        selected_file = f.selected_param(selected_file, self.combo.GetStringSelection())

    def OnMsgBtn(self, event=None):
        """Bring up a wx.MessageDialog with a useless message."""
        dlg = wx.MessageDialog(self,
                               message='A completely useless message',
                               caption='A Message Box',
                               style=wx.OK|wx.ICON_INFORMATION
                               )
        dlg.ShowModal()
        dlg.Destroy()
    def onDir(self, event=None):
        wildcard = "All files (*.*)|*.*"
        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            global selected_file
            selected_file = f.netCDF_file(dialog.GetPath())
            self.file_opened.SetValue(dialog.GetPath())
            dset = netCDF4.Dataset(selected_file[0])
            variables = dset.variables.keys()
##            variables = map(lambda x: x.encode('ascii','replace'), variables)
##            print variables
            self.combo.Clear()
            for var in variables:
                self.combo.Append(var)

        dialog.Destroy()

    def outDir(self, event=None):
        wildcard = "All files (*.*)|*.*"
##        dialog = wx.FileDialog(None, "Choose a file", os.getcwd(), "", wildcard, wx.OPEN)
        dialog = wx.DirDialog(None, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dialog.ShowModal() == wx.ID_OK:
            f.chgdir(dialog.GetPath()) 
            self.out_directory.SetValue(dialog.GetPath())

        dialog.Destroy()
        
class DemoFrame(wx.Frame):
    """Main Frame holding the Panel."""
    def __init__(self, *args, **kwargs):
        """Create the DemoFrame."""
        wx.Frame.__init__(self, *args, **kwargs)
        # Add the Widget Panel
        self.Panel = DemoPanel(self)
##        self.Maximize(True)
##        self.Fit()
        
    def OnQuit(self, event=None):
        """Exit application."""
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    
    frame = DemoFrame(None, title="Forcing Files Generation")
    frame.Show()
    
    app.MainLoop()
