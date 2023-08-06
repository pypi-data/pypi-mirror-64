"""
Speech API algorithm
"""
# pylint: disable=no-name-in-module,import-error
import logging
import json
import struct
from datetime import datetime
import pyaudio
import speech_recognition as sr
from PySide2.QtCore import QObject, Signal, Slot, QThread, QTimer

from pvporcupine import Porcupine

LOGGER = logging.getLogger("voice_recognition_logger")


class VoiceRecognitionService(QObject):
    """
    Voice Recognition service which takes an microphone input and converts it
    to text by using the Google Cloud Speech-to-Text API
    """

    start_listen = Signal()
    stop_timer = Signal()
    next = Signal()
    previous = Signal()
    undo = Signal()
    quit = Signal()
    google_api_not_understand = Signal()
    google_api_request_failure = Signal(str)
    voice_command = Signal(str)
    start_processing_request = Signal()
    end_processing_request = Signal()

    def __init__(self, config):
        """
        Construct the service.
        Configuration must contain
        porcupine dynamic library path:
            Porcupine/lib/<operating_system>/<processor_type>/<library_file>
        porcupine model file path:
            Porcupine/lib/common/porcupine_params.pv
        porcupine keyword file(s):
            Porcupine/resources/keyword_files/<operating_system>/<keyword>
        optional:
        google credentials file: json file with google cloud api credentials
        timeout for command: default None,
        """
        LOGGER.info("Creating Voice Recognition Service")
        # Need this for SignalInstance
        super(VoiceRecognitionService, self).__init__()

        self.timeout_for_command = config.get("timeout for command", None)

        library_path = config.get("porcupine dynamic library path", None)
        if library_path is None:
            raise KeyError("Config must contain porcupine dynamic",
                           " library path")

        model_file_path = config.get("porcupine model file path", None)
        if model_file_path is None:
            raise KeyError("Config must contain porcupine model file path")

        keyword_file_paths = config.get("porcupine keyword file", None)
        if keyword_file_paths is None:
            raise KeyError("Config must contain porcupine keyword file")

        sensitivities = config.get("sensitivities", [1.0])
        self.interval = config.get("interval", 10)

        self.handle = Porcupine(library_path,
                                model_file_path,
                                keyword_file_paths=keyword_file_paths,
                                sensitivities=sensitivities)
        audio = pyaudio.PyAudio()
        self.audio_stream = audio.open(rate=self.handle.sample_rate,
                                       channels=1,
                                       format=pyaudio.paInt16,
                                       input=True,
                                       frames_per_buffer=self.handle
                                       .frame_length)

        #  this is to add the credentials for the google cloud api
        #  set the environment variable GOOGLE_APPLICATION_CREDENTIALS
        #  to the path  of your json file with credentials
        key_file_path = config.get('google credentials file', None)
        self.credentials = None
        if key_file_path is not None:
            with open(key_file_path, 'r') as file:
                self.credentials = file.read()

                #r aises a ValueError if the credential file isn't a valid json
                json.loads(self.credentials)

        # Creating timer later, in the context of the running thread.
        self.timer = None

        LOGGER.info("Created Voice Recognition Service")

    def run(self):
        """
        Entry point for the QThread which starts the timer to listen in the
        background
        """
        LOGGER.info("run method executed")

        # Creating the timer in the context of the running thread.
        self.timer = QTimer()
        self.timer.setInterval(self.interval)
        self.timer.timeout.connect(self.listen_for_keyword)
        self.stop_timer.connect(self.__stop)

        #  start the timer to start the background listening
        self.timer.start()

    def request_stop(self):
        """
        Called by external client to stop timer.
        """
        LOGGER.info("Requesting VoiceRecognitionService to stop timer.")
        self.stop_timer.emit()
        QThread.msleep(self.interval * 3)
        while self.timer.isActive():
            QThread.msleep(self.interval * 3)
        LOGGER.info("Requested VoiceRecognitionService to stop timer.")

    @Slot()
    def __stop(self):
        LOGGER.info("Stopping VoiceRecognitionService timer.")
        self.timer.stop()
        QThread.msleep(self.interval * 3)
        LOGGER.info("Stopped VoiceRecognitionService timer.")

    def listen_for_keyword(self):
        """
        This method is called every 100 milliseconds by the QThread running and
        listens for the keyword
        """
        pcm = self.audio_stream.read(self.handle.frame_length)
        pcm = struct.unpack_from("h" * self.handle.frame_length, pcm)
        result = self.handle.process(pcm)
        if result:
            #  when the keyword gets detected, the user can input a command
            LOGGER.info('[%s] detected keyword', str(datetime.now()))
            self.start_listen.emit()
            self.listen_to_command()

    def listen_to_command(self):
        """
        This method gets called when a specific command is said.
        It then listens for specific commands and converts them to QT Signals
        """
        recognizer = sr.Recognizer()
        #  listen to a single command
        with sr.Microphone() as source:
            audio = recognizer\
                .listen(source, phrase_time_limit=self.timeout_for_command)
        try:
            #  convert command to string,
            #  this string should later be used to fire a certain GUI command
            self.start_processing_request.emit()
            words = recognizer.\
                recognize_google_cloud(audio,
                                       credentials_json=self.credentials)
            self.end_processing_request.emit()
            #  convert the spoken input in a signal
            #  for next, quit, previous and undo there are specific signals
            #  if none of them is said, a generic signal is emitted, containing
            #  the string of the spoken input
            if words == "next ":
                self.next.emit()
            elif words == "quit ":
                self.quit.emit()
            elif words == "previous ":
                self.previous.emit()
            elif words == "undo ":
                self.undo.emit()
            else:
                self.voice_command.emit(words)
        except sr.UnknownValueError:
            self.google_api_not_understand.emit()
        except sr.RequestError as exception:
            self.google_api_request_failure.emit(str(exception))
