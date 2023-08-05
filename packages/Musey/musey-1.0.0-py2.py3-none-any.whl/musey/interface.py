import os

os.environ["KIVY_NO_CONSOLELOG"] = "1"
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.popup import Popup
import kivy.utils

Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.uix.image import Image
from kivy.graphics import *
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from musey.muse import Muse
from .Backend import Backend
import pkg_resources

from kivy.core.window import Window

Window.clearcolor = (23 / 256, 63 / 256, 95 / 256, 0.1)


# Frontend Test Branch
class UVicMuse(FloatLayout):

    def __init__(self, **kwargs):
        super(UVicMuse, self).__init__(**kwargs)

        self.press_search_txt = "Search for a list of Available Muses"
        self.btn_color = (23 / 256, 54 / 256, 121 / 256, 1)
        self.txt_color = kivy.utils.get_color_from_hex("#7FC5DC")
        # self.txt_color = kivy.utils.get_color_from_hex("#F8B195")
        self.muses = []
        self.sock = None
        self.muse = None
        self.did_connect = False
        self.udp_address = ""
        self.connected_address = ""
        self.muse_backend = 'bgapi'
        self.host_address = 'localhost'
        self.backend = Backend(self.muse_backend)
        self.current_muse_id = 0

        # Create UVic Muse Logo
        DATA_PATH = pkg_resources.resource_filename('musey', 'docs/')
        self.img_bg = Image(source=os.path.join(DATA_PATH, 'background.png'))

        self.add_widget(self.img_bg)

        # self.img_header = Image(source=os.path.join(DATA_PATH, 'Header.png'))

        # Initiate Labels
        self.status_label = Label(
            text="Press Search to Look For Nearby Muse                                                ",
            color=self.txt_color, font_size=14)

        # self.canvas.add(Color(133 / 256, 169 / 256, 204 / 256))
        # self.canvas.add(Rectangle(size=(750, 150), pos=(0, 600 - 150)))

        # # Footer
        # self.canvas.add(Color(11 / 256, 30 / 256, 56 / 256, 0.5))
        # self.canvas.add(Rectangle(size=(750, 30), pos=(0, 0 + 0)))

        self.sensors_title = Label(text="Sensors", color=self.txt_color, font_size=18, bold=True)
        self.LSL_title = Label(text="Lab Streaming", color=self.txt_color, font_size=18, bold=True)
        self.LSL2_title = Label(text="Layer (LSL)", color=self.txt_color, font_size=18, bold=True)
        self.filter_title = Label(text="Filters", color=self.txt_color, font_size=18, bold=True)

        # self.about_button = Button(text="About Us", size_hint=(.15, .00020), pos_hint={'x': 0.84, 'y': .0235},
        #                            background_color=self.btn_color, font_size=12,
        #                            on_release=self.about)
        #
        # self.reset_button = Button(text="Reset Kernel", size_hint=(.15, .000040), pos_hint={'x': 0.01, 'y': .0235},
        #                            background_color=(kivy.utils.get_color_from_hex("#DB901C")), font_size=12,
        #                            on_release=self.reset)

        self.search_button = Button(text="Search", size_hint=(.15, .07), pos_hint={'x': 0.82, 'y': .6},
                                    background_color=self.btn_color, on_press=self.update_status_search,
                                    on_release=self.search)

        # Initiate Buttons and bind press and release to functions
        self.connect_button = Button(text="Connect", size_hint=(.15, .07), pos_hint={'x': 0.82, 'y': .5},
                                     background_color=self.btn_color,
                                     on_release=self.connect, on_press=self.on_connect_press)
        self.stream_button = Button(text="Start Stream", size_hint=(.15, .07), pos_hint={'x': 0.82, 'y': .4},
                                    background_color=self.btn_color,
                                    on_release=self.stream)

        self.LSL_label = Label(text="LSL", color=self.txt_color, font_size=14)
        self.EEG_label = Label(text="EEG", color=self.txt_color, font_size=14)
        self.PPG_label = Label(text="PPG", color=self.txt_color, font_size=14)
        self.ACC_label = Label(text="ACC", color=self.txt_color, font_size=14)
        self.GYRO_label = Label(text="GYRO", color=self.txt_color, font_size=14)
        self.notch_label = Label(text="Notch Filter (60Hz)", color=self.txt_color, font_size=14)
        self.lowpass_label = Label(text="Lowpass Filter", color=self.txt_color, font_size=14)
        self.highpass_label = Label(text="Highpass Filter", color=self.txt_color, font_size=14)
        self.lowpass_cutoff = Label(text="Cutoff", color=self.txt_color, font_size=14)
        self.highpass_cutoff = Label(text="Cutoff", color=self.txt_color, font_size=14)

        # initiate List with max height
        self.list_box = Spinner(text=self.press_search_txt, values='', size_hint=(0.77, 0.07),
                                pos_hint={'x': 0.03, 'y': .6}, background_color=self.btn_color)
        self.list_box.dropdown_cls.max_height = self.list_box.height * 1.6

        # Initiate Checkbox's
        self.LSL_checkbox = CheckBox(active=True, size_hint_y=0.02, size_hint_x=0.02)
        self.EEG_checkbox = CheckBox(active=True, size_hint_y=0.02, size_hint_x=0.02)
        self.PPG_checkbox = CheckBox(active=False, size_hint_y=0.02, size_hint_x=0.02)
        self.ACC_checkbox = CheckBox(active=False, size_hint_y=0.02, size_hint_x=0.02)
        self.GYRO_checkbox = CheckBox(active=False, size_hint_y=0.02, size_hint_x=0.02)
        self.lowpass_checkbox = CheckBox(active=False, size_hint_y=0.02, size_hint_x=0.02)
        self.highpass_checkbox = CheckBox(active=False, size_hint_y=0.02, size_hint_x=0.02)
        self.notch_checkbox = CheckBox(active=True, size_hint_y=0.02, size_hint_x=0.02)

        # Initiate textbox's to enter text
        self.lowpass_text = TextInput(font_size=13, pos_hint={"x": 0.795, "y": 0.225}, size_hint=(0.07, 0.043),
                                      multiline=False, text='30', write_tab=False)
        self.highpass_text = TextInput(font_size=13, pos_hint={"x": 0.795, "y": 0.092}, size_hint=(0.07, 0.043),
                                       multiline=False, text='0.1', write_tab=False, )

        # add widgets that have been initiated to frame
        # self.add_widget(self.img_header)
        # self.add_widget(self.about_button)
        # self.add_widget(self.reset_button)
        self.add_widget(self.search_button)
        self.add_widget(self.connect_button)
        self.add_widget(self.stream_button)
        self.add_widget(self.status_label)
        self.add_widget(self.lowpass_text)
        self.add_widget(self.highpass_text)
        self.add_widget(self.EEG_label)
        self.add_widget(self.PPG_label)
        self.add_widget(self.ACC_label)
        self.add_widget(self.GYRO_label)
        self.add_widget(self.LSL_checkbox)
        self.add_widget(self.EEG_checkbox)
        self.add_widget(self.PPG_checkbox)
        self.add_widget(self.ACC_checkbox)
        self.add_widget(self.GYRO_checkbox)
        self.add_widget(self.lowpass_label)
        self.add_widget(self.highpass_label)
        self.add_widget(self.lowpass_checkbox)
        self.add_widget(self.highpass_checkbox)
        # self.add_widget(self.lowpass_cutoff)
        # self.add_widget(self.highpass_cutoff)
        self.add_widget(self.notch_checkbox)
        self.add_widget(self.notch_label)
        self.add_widget(self.list_box)
        self.add_widget(self.sensors_title)
        self.add_widget(self.filter_title)
        self.add_widget(self.LSL_title)
        self.add_widget(self.LSL2_title)

        # Adjust positions of widgets that have been added to the frame
        # self.img_header.pos = (0, 225)
        self.img_bg.pos = (0, 0)
        self.status_label.pos = (-155, 120)

        self.EEG_label.pos = (-263, -150)
        self.PPG_label.pos = (-160, -150)
        self.ACC_label.pos = (-263, -200)
        self.GYRO_label.pos = (-158, -200)

        self.LSL_checkbox.pos = (355, 110)
        self.EEG_checkbox.pos = (104, 122)
        self.PPG_checkbox.pos = (210, 122)
        self.ACC_checkbox.pos = (104, 71)
        self.GYRO_checkbox.pos = (210, 71)

        self.notch_label.pos = (128, -190)
        self.lowpass_label.pos = (140, -150)
        self.highpass_label.pos = (140, -230)
        self.lowpass_checkbox.pos = (570, 142)
        self.highpass_checkbox.pos = (570, 63)
        self.notch_checkbox.pos = (570, 102)

        self.lowpass_cutoff.pos = (235, -150)
        self.highpass_cutoff.pos = (235, -230)

        self.sensors_title.pos = (-213, -125)
        self.LSL_title.pos = (-10, -125)
        self.LSL2_title.pos = (-12, -142)
        self.filter_title.pos = (200, -125)

        # initial state
        self.PPG_checkbox.disabled = True
        self.LSL_checkbox.disabled = True
        self.EEG_checkbox.disabled = True
        self.ACC_checkbox.disabled = True
        self.GYRO_checkbox.disabled = True
        self.notch_checkbox.disabled = True
        self.lowpass_checkbox.disabled = True
        self.highpass_checkbox.disabled = True
        self.highpass_text.disabled = True
        self.lowpass_text.disabled = True
        self.stream_button.disabled = True
        self.connect_button.disabled = True

    # logic

    def on_connect_press(self, event):
        if self.did_connect:
            pass
        else:
            self.status_label.text = "Connecting to the selected MUSE...                                 " \
                                     "                      "

    # As Search takes 10 seconds, update the status before the process begins
    def update_status_search(self, event):
        self.status_label.text = "Searching for nearby Muses, this may take up to ten seconds..."

    # Function to change state of all components
    def button_state(self, connect_state, disconnect_state, search_state,
                     stream_state, stop_state, LSL_state, EEG_state, PPG_state,
                     ACC_state, GYRO_state, Notch_state, Lowpass_check_state,
                     lowpass_cut_state, highpass_check_state, highpass_cut_state, list_box_state):
        # self.connect_button.disabled = connect_state
        self.search_button.disabled = search_state
        self.stream_button.disabled = stream_state
        self.LSL_checkbox.disabled = LSL_state
        self.EEG_checkbox.disabled = EEG_state
        self.PPG_checkbox.disabled = PPG_state
        self.ACC_checkbox.disabled = ACC_state
        self.GYRO_checkbox.disabled = GYRO_state
        self.notch_checkbox.disabled = Notch_state
        self.lowpass_checkbox.disabled = Lowpass_check_state
        self.lowpass_text.disabled = lowpass_cut_state
        self.highpass_checkbox.disabled = highpass_cut_state
        self.highpass_text.disabled = highpass_cut_state
        self.list_box.disabled = list_box_state

    def about(self, event):
        popup = Popup(title="About UVicMUSE", content=Label(text='Developed and Designed by \nBardia'
                                                                 'Barabadi & Jamieson Fregeau\n\nKrigolson Lab '
                                                                 '(Theoretical and \nApplied Neuroscience Laboratory)\n\n'
                                                                 'University of Victoria, Canada, 2020.'
                                                            ), size_hint=(None, None), size=(300, 200))
        popup.open()

    def reset(self, event):
        if self.did_connect:
            self.disconnect(event)
        else:
            self.muses = []
            self.muse = []
            self.host_address = 'localhost'
            self.backend = Backend(self.muse_backend)
            self.current_muse_id = 0
            self.did_connect = False
            self.connect_button.text = "Connect"
            self.connect_button.disabled = True
            self.list_box.values = []
            self.list_box.text = self.press_search_txt

    # Function for starting Data Stream
    def stream(self, event):

        if self.backend.is_udp_streaming:
            self.backend.udp_stop_btn_callback()
            self.status_label.text = "Data stream has been stopped                                           " \
                                     "                       "
            self.stream_button.text = "Start Streaming"

            self.lowpass_checkbox.disabled = False
            self.highpass_checkbox.disabled = False
            self.notch_checkbox.disabled = False
            self.highpass_text.disabled = False
            self.lowpass_text.disabled = False

            return

        self.button_state(True, True, True, False, False, True, True, True,
                          True, True, True, True, True, True, True, True)

        self.backend.udp_stream_btn_callback(
            use_low_pass=self.lowpass_checkbox.active,
            use_high_pass=self.highpass_checkbox.active,
            low_pass_cutoff=(float)(self.get_lowpass_cutoff()),
            high_pass_cutoff=(float)(self.get_highpass_cutoff()),
            use_notch=self.get_notch_checkbox, )
        if self.backend.is_udp_streaming:
            self.status_label.text = "Streaming Data                                                      " \
                                     "                                            "
            self.stream_button.text = "Stop Streaming"
        else:
            self.status_label.text = "Unsuccessful streaming attempt"

    # Function for stopping Data Stream
    def stop_stream(self, event):
        self.button_state(True, False, True, False, True, False, True, True, True, True,
                          False, False, False, False, False, True)
        self.backend.udp_stop_btn_callback()
        self.status_label.text = "Data stream has been stopped                                           " \
                                 "                       "

    def get_lowpass_cutoff(self):
        return float(self.lowpass_text.text)

    def get_highpass_cutoff(self):
        return float(self.highpass_text.text)

    def get_notch_checkbox(self):
        if self.notch_checkbox.active:
            return True
        return False

    def get_LSL_checkbox(self):
        if self.LSL_checkbox.active:
            return True
        return False

    def get_EEG_checkbox(self):
        if self.EEG_checkbox.active:
            return True
        return False

    def get_PPG_checkbox(self):
        if self.PPG_checkbox.active:
            return True
        return False

    def get_ACC_checkbox(self):
        if self.ACC_checkbox.active:
            return True
        return False

    def get_GYRO_checkbox(self):
        if self.GYRO_checkbox.active:
            return True
        return False

    def get_host_entry(self):
        return str(self.host_text.text)

    # Function for Connecting to selected Muse in Dropdown list
    def connect(self, event):

        if self.did_connect:
            self.disconnect(event)
            return

        try:
            self.button_state(True, False, True, False, True,
                              False, True, True, True, True,
                              False, False, False, False, False, True)

            self.current_muse_id = self.list_box.values.index(self.list_box.text)

            self.backend.connect_btn_callback(self.current_muse_id, self.get_EEG_checkbox(), self.get_PPG_checkbox(),
                                              self.get_ACC_checkbox(), self.get_GYRO_checkbox())
            self.did_connect = self.backend.is_connected()
            if self.did_connect:
                self.status_label.text = "                    Successfully connected to " + str(
                    self.muses[self.current_muse_id]['name'] + ", select filters to stream data with")
                self.connected_address = self.muses[self.current_muse_id]['address']
                self.connect_button.text = "Disconnect"
            else:
                self.status_label.text = "Unsuccessful connection attempt, make sure Muse is turned on         " \
                                         "                            "
        except:
            self.status_label.text = "                      Please select a Muse from the dropdown menu before" \
                                     " connecting                "
            self.button_state(True, True, False,
                              True, True, True, False, False,
                              False, False, True, True,
                              True, True, True, False)

    # Function for Disconnecting from connected Muse
    def disconnect(self, event):
        self.button_state(True, True,
                          False, True, True, False, False,
                          False, False, False, False,
                          False, False, False, False, False)

        self.backend.disconnect_btn_callback()
        self.status_label.text = "Disconnected from " + str(self.muses[self.current_muse_id][
                                                                'name'] + "                                        "
                                                                          "                         ")
        self.did_connect = False
        self.connect_button.text = "Connect"
        self.connect_button.disabled = True
        self.list_box.values = []
        self.list_box.text = self.press_search_txt

    # Function for Searching for nearby Muses
    def search(self, event):

        if self.did_connect:
            self.disconnect(event)

        try:
            self.button_state(False, True, False,
                              True, True, True, False, False,
                              False, False, True, True,
                              True, True, True, False)

            self.connect_button.disabled = False
            self.muses, succeed = self.backend.refresh_btn_callback()
            self.vals = []
            for i in range(len(self.muses)):
                self.vals.append(self.muses[i]['name'] + " Mac Address " + str(self.muses[i]['address']))

            if (len(self.muses)) == 0:
                self.status_label.text = "No nearby devices were found, please try again                               "
            if (len(self.muses)) == 1:
                self.status_label.text = "1 device was found, please choose sensors to connect with       "
            if (len(self.muses)) > 1:
                self.status_label.text = str(
                    len(self.muses)) + " Devices were found, please choose sensors to connect with       "

            self.list_box.values = self.vals

            self.list_box.text = str(len(self.muses)) + " Devices were found, Press to choose"
        except:
            self.status_label.text = "No BLE Module Found                                        " \
                                     "                                         "


class Muse(App):
    def build(self):
        return UVicMuse()


def runGUI():
    Muse().run()
