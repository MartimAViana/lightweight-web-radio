import os
import pygame
from flask import Flask, Response, stream_with_context, Blueprint
import time
from pathlib import Path

DEBUG = False

class AudioPlayer:
    def __init__(self, music_folder, radio_name):
        self.music_folder = Path(music_folder)
        self.radio_name = radio_name
        self.current_track = None
        self.playlist = []
        self.is_playing = False
        
        # Initialize pygame mixer
        pygame.mixer.init()
        self.refresh_playlist()
    
    def refresh_playlist(self):
        """Scan the music folder and update playlist"""
        self.playlist = [
            file for file in self.music_folder.glob('*')
            if file.suffix.lower() in ('.mp3', '.wav', '.ogg')
        ]
    
    def play_next(self):
        """Play the next track in the playlist"""
        if not self.playlist:
            self.refresh_playlist()
            if not self.playlist:
                return False
            
        if self.current_track is None or self.current_track >= len(self.playlist) - 1:
            self.current_track = 0
        else:
            self.current_track += 1
            
        track = str(self.playlist[self.current_track])
        pygame.mixer.music.load(track)
        pygame.mixer.music.play()
        self.is_playing = True
        return True
    
    def get_current_track(self):
        """Get the name of the currently playing track"""
        if self.current_track is not None and self.playlist:
            return self.playlist[self.current_track].name
        return "No track playing"

class WebRadio:
    def __init__(self, name, folder, url_prefix):
        self.blueprint = Blueprint(f'radio_{name}', __name__, url_prefix=f'/{url_prefix}')
        self.player = AudioPlayer(folder, name)
        self.setup_routes()
    
    def setup_routes(self):
        @self.blueprint.route('/')
        def index():
            return f'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>{self.player.radio_name}</title>
            </head>
            <body>
                <h1>{self.player.radio_name}</h1>
                <p>Now playing: <span id="current-track">Loading...</span></p>
                
                <script>
                    const eventSource = new EventSource('./stream');
                    eventSource.onmessage = function(e) {{
                        document.getElementById('current-track').textContent = e.data;
                    }};
                </script>
            </body>
            </html>
            '''

        @self.blueprint.route('/stream')
        def stream():
            def generate():
                while True:
                    if not pygame.mixer.music.get_busy() and self.player.is_playing:
                        self.player.play_next()
                    yield f"data: {self.player.get_current_track()}\n\n"
                    time.sleep(1)
            
            return Response(
                stream_with_context(generate()),
                mimetype='text/event-stream'
            )
    
    def start_playing(self):
        self.player.play_next()

app = Flask(__name__)
radios = {}

def create_radio(name, folder, url_prefix):
    radio = WebRadio(name, folder, url_prefix)
    radios[name] = radio
    app.register_blueprint(radio.blueprint)
    radio.start_playing()

def start_server():
    app.run(host='127.0.0.1', port=5000, debug=DEBUG)

if __name__ == '__main__':
    print("Please run this through main.py instead") 