from time import sleep
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Placeholder, Button, Static, LoadingIndicator, Footer
from textual.containers import HorizontalScroll, VerticalScroll, Center
from widgets.widgets import *
import subprocess


#START-------------------------Header and Footer---------------------------------------
class Header(Static):  
    def compose(self) -> ComposeResult:
        yield Static("Rai Sound Terminal Player", id="header-text")

# class Footer(Placeholder):  
#     pass

#END-------------------------Header and Footer---------------------------------------


class Loading(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:

        button_id = event.button.id
        if button_id == "interrupt":
            command = ['killall','mpv']
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            try:
                loading_kill = self.app.query_one("#loading")
                loading_kill.remove()

            except:
                pass

        elif button_id == "pause":
            command = ['pkill','-STOP', 'mpv']
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.add_class("master_button")
        elif button_id == "continue":
            command = ['pkill','-CONT', 'mpv']
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.remove_class("master_button")

    def compose(self) -> ComposeResult:
        with Center(id='player_buttons'):
            yield Button("Stop", id="interrupt", variant="error")
            yield Button("Pause", id="pause")
            yield Button("Continue", id="continue",variant="success")


            
#START-------------------------Live Radio Channel list---------------------------------------
class ChannelName(Static):
    def __init__(self, radio_name, **kwargs):
        super().__init__(**kwargs)
        self.radio_name = radio_name  # Store the radio_name passed

    def compose(self) -> ComposeResult:
        # Use self.radio_name to generate the buttons, not a static list
        with Center(id="main-list"):
            yield Button(f"{self.radio_name}", id=f"{self.radio_name.lower().strip().replace(' ', '').replace('è', 'e').replace('ü', 'u')}")



class RadioChannelName(VerticalScroll):
    
    

    def compose(self) -> ComposeResult:

        radio_list = RaiRadioInfo().parsing_data()[0]
        for radio_id in radio_list:

            yield ChannelName(f"{radio_id}")

#END-------------------------Live Radio Channel list---------------------------------------

#START-------------------------Podcast buttons list---------------------------------------
class PodcastName(Static):
    def __init__(self, radio_name, **kwargs):
        super().__init__(**kwargs)
        self.radio_name = radio_name  # Store the radio_name passed

    def compose(self) -> ComposeResult:
        # Use self.radio_name to generate the buttons, not a static list
        with Center(id="main-list"):
            yield Button(f"{self.radio_name}", id=f"{self.radio_name.lower().strip().replace(' ', '').replace('è', 'e').replace('ü', 'u')}")



class PodcastChannelName(VerticalScroll):
    
    def compose(self) -> ComposeResult:

        radio_list = podcast_list()[0]
        for radio_id in radio_list:

            yield PodcastName(f"{radio_id}")

#----------------------------------------------------------------------------------------------------------


class VideoPodcastName(Static):
    def __init__(self, radio_name, **kwargs):
        super().__init__(**kwargs)
        self.radio_name = radio_name  # Store the radio_name passed

    def compose(self) -> ComposeResult:
        # Use self.radio_name to generate the buttons, not a static list
        with Center(id="main-list"):
            yield Button(f"{self.radio_name}", id=f"{self.radio_name.lower().strip().replace(' ', '').replace('è', 'e').replace('ü', 'u')}")



class VideoPodcastChannelName(VerticalScroll):
    
    def compose(self) -> ComposeResult:

        radio_list = podcast_list()[2]
        for radio_id in radio_list:

            yield VideoPodcastName(f"{radio_id}")




class PodcastEpisode(Static):
    def __init__(self, radio_name, **kwargs):
        super().__init__(**kwargs)
        self.radio_name = radio_name  # Store the radio_name passed

    def compose(self) -> ComposeResult:
        # Use self.radio_name to generate the buttons, not a static list
        with Center(id="main-list"):
            yield Button(f"{self.radio_name}", id=f"{self.radio_name.lower().strip().replace(' ', '').replace(':', '_')}")



class PodcastEpisodeList(VerticalScroll):
    def __init__(self, podcast, **kwargs):
        super().__init__(**kwargs)
        self.podcast = podcast  # Store the radio_name passed
   
    def compose(self) -> ComposeResult:

        for radio_id in self.podcast:

            yield PodcastEpisode(f"{radio_id}")




class VideoPodcastEpisode(Static):
    def __init__(self, radio_name, **kwargs):
        super().__init__(**kwargs)
        self.radio_name = radio_name  # Store the radio_name passed

    def compose(self) -> ComposeResult:
        # Use self.radio_name to generate the buttons, not a static list
        with Center(id="main-list"):
            yield Button(f"{self.radio_name}", id=f"{self.radio_name.lower().strip().replace(' ', '').replace(':', '_')}")



class VideoPodcastEpisodeList(VerticalScroll):
    def __init__(self, podcast, **kwargs):
        super().__init__(**kwargs)
        self.podcast = podcast  # Store the radio_name passed
   
    def compose(self) -> ComposeResult:

        for radio_id in self.podcast:

            yield VideoPodcastEpisode(f"{radio_id}")




#END-------------------------END Podcast buttons list---------------------------------------


#START-------------------------Sidebar---------------------------------------
class SideBar(Static):

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "live-radio":
            self.app.clear_main_content()

            self.update("")
            main_content = self.app.query_one("#main-content")
            main_content.mount(RadioChannelName())

        elif button_id == "podcast":
            self.app.clear_main_content()
            self.update("")
            main_content = self.app.query_one("#main-content")
            main_content.mount(PodcastChannelName())

        elif button_id == "podcast-video":
            self.app.clear_main_content()
            self.update("")
            main_content = self.app.query_one("#main-content")
            main_content.mount(VideoPodcastChannelName())

    def compose(self) -> ComposeResult:
        yield Button("Live Radio", id="live-radio")
        yield Button("Podcast", id='podcast')
        yield Button("Podcast Video", id='podcast-video')




class SideBarCloumn(VerticalScroll):
    def compose(self) -> ComposeResult:
        yield SideBar(id=f"sidebar")


#END-------------------------Sidebar---------------------------------------


#START-------------------------Application---------------------------------------
class AppScreen(Screen):
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        button_label = event.button.label
        radio_id_list = RaiRadioInfo().returning_list_id_channel()
        description_channel = RaiRadioInfo().parsing_data()[1]
        time_interval = RaiRadioInfo().parsing_data()[2]

        for x in radio_id_list:
            if button_id == x:
                self.app.clear_main_content()
                stream_url = RaiRadioInfo().returning_stream(x)[0]
                logo_path = RaiRadioInfo().returning_stream(x)[1]
                
                command = ['nohup', 'mpv', '--force-window=yes', f'--audio-file={stream_url}', logo_path, '--loop-file=inf']
                subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                main_content = self.app.query_one("#main-content")
                main_content.mount(Static(f"{button_label} - {time_interval[x]}", id="current_live_radio_text"))
                main_content.mount(Loading())
                main_content.mount(Static(description_channel[x], id="description"))

        possibile_podcasts = podcast_list()[0]
        possibile_podcasts_ids = [x.strip().lower().replace(" ", "") for x in possibile_podcasts]
        for x,y in zip(possibile_podcasts, possibile_podcasts_ids):
            if button_id == y:
                self.app.clear_main_content()
                url = podcast_list()[1][x]['url'] 
                episodes = PodcastInfo(url)
                episodes_date = episodes.episodes_date()[0]
                main_content = self.app.query_one("#main-content")
                main_content.mount(PodcastEpisodeList(episodes_date))

            instance = PodcastInfo(podcast_list()[1][x]['url']) 
            list_id_complete = instance.episodes_date()[1]
            for f in list_id_complete:
                if button_id == f:
                    self.app.clear_main_content()
                    date_ref = f[11:]
                    main_content = self.app.query_one("#main-content")
                    main_content.mount(Loading())
                    instance.mpv_stream(instance.extract_audio_url(instance.episode_stream_url(date_ref)), date_ref , podcast_list()[1][x]['logo'])


#-----------------------------------------------------------------------------------------------------------------------------------------------------
        possibile_podcasts_video = podcast_list()[2]
        possibile_podcasts_ids_video = [x.strip().lower().replace(" ", "") for x in possibile_podcasts_video]
        for x,y in zip(possibile_podcasts_video, possibile_podcasts_ids_video):
            if button_id == "tintoriayoutube":
                self.app.clear_main_content()
                self.app.clear_main_content()
                url = podcast_list()[3][x]['url'] 
                episodes = PodcastInfo(url)
                episodes_date = episodes.episodes_date()[0]
                main_content = self.app.query_one("#main-content")
                main_content.mount(VideoPodcastEpisodeList(episodes_date))

            instance = PodcastInfo(podcast_list()[3][x]['url']) 
            list_id_complete_video = instance.episodes_date()[1]
            for m in list_id_complete_video:
                if button_id == m:
                    self.app.clear_main_content()
                    date_ref = m[11:]
                    main_content = self.app.query_one("#main-content")
                    main_content.mount(Loading())
                    f = instance.episode_stream_url(date_ref) 
                    main_content.mount(Static(f))
                    instance.mpv_stream_youtube(instance.episode_stream_url(date_ref))

    def compose(self) -> ComposeResult:
        yield Header(id="Header")  
        yield Footer(id="Footer")  

        with HorizontalScroll():
            yield SideBarCloumn()
            yield VerticalScroll(id="main-content")


class LayoutApp(App):
    
    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
        ("q", "quit_program", "Quit"),
    ]


    CSS_PATH = 'tcss/style.tcss'

    def on_mount(self) -> None:
        self.push_screen(AppScreen())

    def clear_header(self):
        """Clears all content in the right panel by removing its children."""
        header = self.query_one("#Header")
        # Unmount all the children in the right-panel
        for child in header.children:
            child.remove()

    def clear_main_content(self):
        """Clears all content in the right panel by removing its children."""
        radio_channel_name = self.query_one("#main-content")
        # Unmount all the children in the right-panel
        for child in radio_channel_name.children:
            child.remove()
    
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def action_quit_program(self) -> None:
        """Action to quit the applicatio"""
        self.app.exit()

#END-------------------------Application---------------------------------------

if __name__ == "__main__":
    app = LayoutApp()
    app.run()
