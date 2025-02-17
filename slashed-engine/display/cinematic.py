import moviepy.editor as mp
import numpy as np
import time
import pygame
import tempfile
import os
import threading
import queue
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time

class Cinematic:
    def __init__(self, game):
        self.game = game
        self.frame_queue = queue.Queue()
        self.playing_cinematic = False
        self.skip_cinematic = False
        self.audio_initialized = False

    def play(self, video_path):
        # Arrêter la musique du menu
        self.game.menu_manager.stop_background_music()
        
        # Définir immédiatement la lecture de la cinématique comme active
        self.playing_cinematic = True

        # Démarrer la lecture de la cinématique dans un thread séparé
        self.cinematic_thread = threading.Thread(target=self._play_cinematic_thread, args=(video_path,))
        self.cinematic_thread.start()


    def _play_cinematic_thread(self, video_path):
        clip = mp.VideoFileClip(video_path)
        clip = clip.resize((self.game.screen_width, self.game.screen_height))

        # Extraire l'audio et sauvegarder dans un fichier temporaire
        temp_audio_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio_file.close()
        clip.audio.write_audiofile(temp_audio_file.name)

        # Initialiser pygame pour la lecture audio
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file.name)
        pygame.mixer.music.play()

        start_time = time.time()
        frame_index = 0
        self.playing_cinematic = True

        while frame_index < clip.reader.nframes:
            if self.skip_cinematic:
                break

            frame = clip.get_frame(frame_index / clip.fps)
            frame = np.flipud(frame)  # Flip vertical pour correspondre à OpenGL
            frame_index += 1

            self.frame_queue.put(frame)

            elapsed_time = time.time() - start_time
            frame_time = frame_index / clip.fps
            if elapsed_time < frame_time:
                time.sleep(frame_time - elapsed_time)

        self.skip_cinematic = True
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        self.playing_cinematic = False
        
        # Vider la queue des frames
        while not self.frame_queue.empty():
            self.frame_queue.get()
        # Tenter de supprimer le fichier temporaire
        try:
            os.remove(temp_audio_file.name)
        except PermissionError:
            print(f"PermissionError: impossible de supprimer le fichier {temp_audio_file.name}")

        # Signaler que la cinématique est terminée
        self.game.cinematic_finished = True
        
        # Reprendre la musique du menu après la cinématique
        self.game.menu_manager.play_background_music()


    def render_frame(self):
        if self.playing_cinematic:
            try:
                # Essayer de récupérer une nouvelle frame sans bloquer
                frame = self.frame_queue.get_nowait()
                self.last_frame = frame  # Conserver la frame
            except queue.Empty:
                # Si la file est vide, réutiliser la dernière frame connue
                frame = self.last_frame if hasattr(self, 'last_frame') else None

            if frame is not None:
                glMatrixMode(GL_PROJECTION)
                glPushMatrix()
                glLoadIdentity()
                gluOrtho2D(0, self.game.screen_width, 0, self.game.screen_height)

                glMatrixMode(GL_MODELVIEW)
                glPushMatrix()
                glLoadIdentity()

                glRasterPos2i(0, 0)
                glDrawPixels(frame.shape[1], frame.shape[0], GL_RGB, GL_UNSIGNED_BYTE, frame)
                check_gl_errors()

                glPopMatrix()
                glMatrixMode(GL_PROJECTION)
                glPopMatrix()
                glMatrixMode(GL_MODELVIEW)



def check_gl_errors():
    error = glGetError()
    if error != GL_NO_ERROR:
        print(f"OpenGL Error: {error}")