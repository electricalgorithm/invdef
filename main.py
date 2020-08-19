from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.theming import ThemeManager
from os import remove

# Configs and Variables
Window.size = (667, 375)
car_status = 0
light_status = 0
tempshield_status = 0
jammer_status = 0
gps_data = {
    "longitude": 27.687123,
    "latitude": 42.784624,
    "altitude": 2743.2
}
user = {
    "username": "d",
    "pass": "f"
}
logs = [
    {
        "t": "120920200752",
        "x": "error",
        "s": "110-10111EE01-1-111",
        "m": "Invalid operation Temperature Shield can't open.",
        "a": "gokhankocmarli"
    },
    {
        "t": "120920200752",
        "x": None,
        "s": "110-101111E01-1-111",
        "m": "Upword 0.57, Left 0.28.",
        "a": "osmankilic"
    },
    {
        "t": "120920200750",
        "x": "error",
        "s": "110-101111E01-1-111",
        "m": "Peltier (id 7X5A) has a overheating problem.",
        "a": None
    },
    {
        "t": "120920200750",
        "x": None,
        "s": "110-100000101-1-111",
        "m": "Connection lost, reconnecting!",
        "a": "gokhankocmarli"
    },
    {
        "t": "120920200752",
        "x": "green",
        "s": "110-100000101-1-111",
        "m": "System reconnecting with user gokhankocmarli",
        "a": None
    },
    {
        "t": "120920200752",
        "x": "error",
        "s": "110-10111EE01-1-111",
        "m": "Invalid operation Temperature Shield can't open.",
        "a": "gokhankocmarli"
    },
    {
        "t": "120920200752",
        "x": None,
        "s": "110-101111E01-1-111",
        "m": "Upword 0.57, Left 0.28.",
        "a": "osmankilic"
    },
    {
        "t": "120920200750",
        "x": "error",
        "s": "110-101111E01-1-111",
        "m": "Peltier (id 7X5A) has a overheating problem.",
        "a": None
    },
    {
        "t": "120920200750",
        "x": None,
        "s": "110-100000101-1-111",
        "m": "Connection lost, reconnecting!",
        "a": "gokhankocmarli"
    },
    {
        "t": "120920200752",
        "x": "green",
        "s": "110-100000101-1-111",
        "m": "System reconnecting with user gokhankocmarli",
        "a": None
    }

]
peltiers = [
    {
        "i": "AX1",
        "a": True,
        "s": False,
        "t": 21
    },
    {
        "i": "AX2",
        "a": True,
        "s": True,
        "t": 21
    },
    {
        "i": "peltier2",
        "a": False,
        "s": False,
        "t": 20
    },
    {
        "i": "peltier3",
        "a": True,
        "s": False,
        "t": 22.4
    },
    {
        "i": "peltier4",
        "a": False,
        "s": True,
        "t": 24
    },
    {
        "i": "peltier5",
        "a": True,
        "s": True,
        "t": 24.2
    }
]

# Making GUI file from template.kv and mdcard.kv
line_count = 471
combined_kv = open("combined.kv", "w+")
template_kv = open("template.kv", "r+")
template_kv_list = template_kv.readlines()
for peltier in peltiers:
    mdcard_kv = open("mdcard.kv", "r+")
    x = mdcard_kv.readlines()
    mdcard_kv.close()
    idtext = peltier["i"]
    x[0] = "\n" + x[0]
    x[8] = x[8][0:(len(x[8]) - 1)] + idtext + "_name" + "\n"
    x[26] = x[26][0:(len(x[26]) - 1)] + idtext + "_activity" + "\n"
    x[38] = x[38][0:(len(x[38]) - 1)] + idtext + "_setting" + "\n"
    x[50] = x[50][0:(len(x[50]) - 1)] + idtext + "_temp" + "\n"
    for i in x:
        template_kv_list.insert(line_count, i)
        line_count += 1
for i in template_kv_list:
    combined_kv.writelines(i)
template_kv.close()
combined_kv.close()


# Global Functions
def send_data(datatype, data):
    sent_status = 1
    if sent_status:
        print(f"Data sent! - datatype: {datatype} data: {data} ")
        return 0
    else:
        return 1


def throw_error(error):
    print(error)
    toast(error)
    return 0


# Screens and classes
class MainWindow(Screen):

    def login(self):
        if self.ids.usernameID.text == user['username'] and self.ids.passwordID.text == user['pass']:
            self.ids.usernameID.text = ""
            self.ids.passwordID.text = ""
            return 1
        else:
            self.ids.usernameID.text = ""
            self.ids.passwordID.text = ""
            toast("Wrong password or username. Try again.")
            return 0


class MenuPanel(Screen):

    def open_menu(self):
        self.root.current = "menuPanel"
        self.root.manager.transition.direction = "right"
        return 0

    def update_logs(self):
        for log in logs:
            time = log["t"]
            typex = log["x"]
            status = log["s"]
            message = log["m"]
            if not log["a"] is None:
                auth = "(auth: " + log["a"] + ")"
            else:
                auth = ""
            time = "[" + time[0:2] + "." + time[2:4] + "." + time[4:8] + " " + time[8:10] + "." + time[10:12] + "]"
            if typex is "error":
                output = "[b]" + time + "[/b]" + " [color=#990000]" + status + ": [i]" + message + "[/i]" + auth + \
                         "[/color]" + "\n\n"
            elif typex is "green":
                output = "[b]" + time + "[/b]" + " [color=#336600]" + status + ": [i]" + message + "[/i]" + auth + \
                         "[/color]" + "\n\n"
            else:
                output = "[b]" + time + "[/b] " + status + ": [i]" + message + "[/i]" + auth + "\n\n"

            self.ids.logs_text.text = output + self.ids.logs_text.text

    # It's not static because of exec() function needs "self".
    def update_peltiers(self):
        for index_peltier in peltiers:
            if index_peltier["a"] is True:
                activity = "On"
            else:
                activity = "Off"
            if index_peltier["s"] is True:
                setting = "Hot"
            else:
                setting = "Cold"
            name_command = "self.ids." + index_peltier["i"] + "_name" + ".text = " + "index_peltier[\"i\"]"
            activity_command = "self.ids." + index_peltier["i"] + "_activity" + ".text = " + "activity"
            setting_command = "self.ids." + index_peltier["i"] + "_setting" + ".text = " + "setting"
            temperature_command = "self.ids." + index_peltier["i"] + "_temp" + ".text = " + "str(index_peltier[" \
                                                                                            "\"t\"]) + \" 'C\" "
            exec(name_command)
            exec(activity_command)
            exec(setting_command)
            exec(temperature_command)


class AdminPanel(Screen):

    @staticmethod
    def coordinates_show(selection):
        if selection == "lo":
            toast(f"Longitude: {gps_data['longitude']}")
        elif selection == "la":
            toast(f"Latitude: {gps_data['latitude']}")
        elif selection == "al":
            toast(f"Altitude: {gps_data['altitude']} meters")
        return 0

    def temp_shield_toggle(self):
        global tempshield_status
        if send_data("tempshield_status", not tempshield_status):
            throw_error("[ERR:1] Sending tempshield_status data failed!")
            return 1
        else:
            tempshield_status = not tempshield_status
            if tempshield_status:
                toast("Temperature shield is activated.")
                self.ids.temp_shield_toggle_icon.icon = "layers"
            else:
                toast("Temperature shield is deactivated.")
                self.ids.temp_shield_toggle_icon.icon = "layers-off"
            return 0

    def jammer_toggle(self):
        global jammer_status
        if send_data("jammer_status", not jammer_status):
            throw_error("[ERR:2] Sending jammer_status data failed!")
            return 1
        else:
            jammer_status = not jammer_status
            if jammer_status:
                toast("Jammer is activated.")
                self.ids.jammer_toggle_icon.icon = "access-point-network"
            else:
                toast("Jammer is deactivated.")
                self.ids.jammer_toggle_icon.icon = "access-point-network-off"
            return 0

    def car_light_toggle(self):
        global light_status
        if send_data("light_status", not light_status):
            throw_error("[ERR:3] Sending light_status data failed!")
            return 1
        else:
            light_status = not light_status
            if light_status:
                toast("Lights are activated.")
                self.ids.car_light_toggle_icon.icon = "car-light-high"
            else:
                toast("Lights are deactivated.")
                self.ids.car_light_toggle_icon.icon = "car-light-fog"
            return 0

    def car_engine_startstop(self):
        global car_status
        if send_data("car_status", not car_status):
            throw_error("[ERR:4] Sending car_status data failed!")
            return 1
        else:
            car_status = not car_status
            if car_status:
                toast("Engine started.")
                self.ids.car_engine_startstop_icon.icon = "engine"
            else:
                toast("Engine stopped.")
                self.ids.car_engine_startstop_icon.icon = "engine-off"
            return 0


class WinManager(ScreenManager):
    pass


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "500"
        self.title = "IUC Thermoelectricity Laboratory"

    def build(self):
        self.root = Builder.load_file("combined.kv")
        return 0

    def go_back(self):
        self.root.current = "adminPanel"
        self.root.transition.direction = "left"
        return 0

    @staticmethod
    def peltier_change_data(ids, onoff_status, setting_status):
        pass


if __name__ == "__main__":
    MainApp().run()

remove("combined.kv")
