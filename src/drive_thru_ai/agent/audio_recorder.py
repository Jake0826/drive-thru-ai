import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from io import BytesIO
import os
import logging
import queue
import threading
import time
from elevenlabs.client import ElevenLabs

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class AudioRecorder:
    def __init__(self, elevenlabs_client):
        """Initialize the audio recorder with ElevenLabs client."""
        self.client = elevenlabs_client
        self.sample_rate = 44100
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.recording_thread = None
        self.transcription_queue = queue.Queue()
        
        # Tunable parameters
        self.chunk_duration = 2.0  # Duration in seconds for each audio chunk
        self.silence_threshold = 0.005  # Threshold for silence detection (lowered)
        self.min_audio_level = 0.008  # Minimum audio level for speech detection (lowered)
        self.min_transcription_interval = 0.8  # Minimum time between transcriptions
        self.silence_counter = 0
        self.max_silence_chunks = 3  # Number of silent chunks before stopping
        
        # Echo cancellation settings
        self.is_system_speaking = False  # Flag to indicate when the system is speaking
        self.cooldown_period = 1.0  # Time in seconds to wait after system stops speaking
        
        # Feedback loop prevention
        self.last_system_response = ""  # The last response from the system
        self.similarity_threshold = 0.6  # Threshold for similarity detection
        
        # Stream and thread
        self.stream = None
        self.last_transcription_time = 0
        self.last_transcription = ""
        
        # Status tracking
        self.status_lock = threading.Lock()
        self.status = "idle"

    def is_speech(self, audio_data):
        """Check if the audio data contains speech"""
        if len(audio_data) == 0:
            return False
            
        rms = np.sqrt(np.mean(np.square(audio_data)))
        return rms > self.min_audio_level

    def audio_callback(self, indata, frames, time, status):
        """Callback function for continuous recording"""
        if status:
            logging.warning(f"Status: {status}")
        self.audio_queue.put(indata.copy())

    def process_audio_chunk(self):
        """Process audio chunks and transcribe them"""
        while self.is_recording:
            try:
                # Skip processing if the system is currently speaking
                if self.is_system_speaking:
                    time.sleep(0.2)  # Short sleep to avoid busy-waiting
                    
                    # Clear the audio queue to prevent backlog during speech
                    while not self.audio_queue.empty():
                        try:
                            self.audio_queue.get_nowait()
                        except queue.Empty:
                            break
                    
                    continue
                
                # Collect audio data for chunk_duration seconds
                audio_data = []
                start_time = time.time()
                
                # Set status to listening
                with self.status_lock:
                    self.status = "listening"
                
                # Collect audio for chunk_duration
                while time.time() - start_time < self.chunk_duration and self.is_recording:
                    try:
                        # Check if system started speaking while collecting
                        if self.is_system_speaking:
                            audio_data.clear()  # Clear collected data
                            break
                            
                        data = self.audio_queue.get(timeout=0.1)
                        audio_data.append(data)
                    except queue.Empty:
                        continue

                if not audio_data or not self.is_recording or self.is_system_speaking:
                    continue

                # Combine audio chunks
                audio_array = np.concatenate(audio_data, axis=0)

                # Check if the audio contains speech
                if not self.is_speech(audio_array):
                    self.silence_counter += 1
                    logging.debug(f"Silence detected (counter: {self.silence_counter})")
                    if self.silence_counter < self.max_silence_chunks:
                        continue
                    else:
                        # Reset counter but continue processing
                        self.silence_counter = 0
                else:
                    self.silence_counter = 0

                # Check if enough time has passed since last transcription
                current_time = time.time()
                if current_time - self.last_transcription_time < self.min_transcription_interval:
                    continue

                # Set status to transcribing
                with self.status_lock:
                    self.status = "transcribing"
                
                # Save to temporary file with unique name to avoid conflicts
                temp_filename = f"temp_recording_{current_time}.wav"
                try:
                    wav.write(temp_filename, self.sample_rate, audio_array)
                
                    # Transcribe the audio
                    with open(temp_filename, "rb") as audio_file:
                        audio_data = BytesIO(audio_file.read())
                        
                        # Set status to processing
                        with self.status_lock:
                            self.status = "processing"
                            
                        transcription = self.client.speech_to_text.convert(
                            file=audio_data,
                            model_id="scribe_v1",
                        )

                        if transcription and hasattr(transcription, 'text'):
                            # Only process if it's not just noise or music
                            text = transcription.text.strip()
                            if text and len(text) > 1 and not text.startswith('(') and not text.endswith(')'):
                                logging.info(f"Transcription: {text}")
                                self.last_transcription = text
                                self.transcription_queue.put(text)
                                self.last_transcription_time = current_time
                                
                                # Set status back to listening
                                with self.status_lock:
                                    self.status = "listening"
                except Exception as e:
                    logging.error(f"Error during transcription: {e}")

                finally:
                    # Clean up temporary file
                    if os.path.exists(temp_filename):
                        try:
                            os.remove(temp_filename)
                        except Exception as e:
                            logging.warning(f"Could not remove temp file: {e}")

            except Exception as e:
                logging.error(f"Error processing audio chunk: {e}")

    def start_recording(self):
        """Start continuous recording"""
        if self.is_recording:
            logging.warning("Recording already in progress")
            return
            
        self.is_recording = True
        self.last_transcription_time = 0
        self.silence_counter = 0

        try:
            # Start the recording stream
            self.stream = sd.InputStream(
                channels=1,
                samplerate=self.sample_rate,
                callback=self.audio_callback
            )
            self.stream.start()

            # Start the processing thread
            self.recording_thread = threading.Thread(
                target=self.process_audio_chunk)
            self.recording_thread.daemon = True  # Make thread exit when main thread exits
            self.recording_thread.start()

            logging.info("Started continuous recording")
        except Exception as e:
            logging.error(f"Error starting recording: {e}")
            self.is_recording = False

    def stop_recording(self):
        """Stop the recording"""
        if not self.is_recording:
            return
            
        self.is_recording = False
        
        # Stop the stream
        if self.stream is not None:
            try:
                self.stream.stop()
                self.stream.close()
            except Exception as e:
                logging.error(f"Error closing stream: {e}")
                
        # Wait for thread to join
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=1.0)
            
        logging.info("Stopped recording")

    def _calculate_similarity(self, text1, text2):
        """Calculate simple similarity between two texts"""
        # Convert to lowercase for comparison
        text1 = text1.lower()
        text2 = text2.lower()
        
        # Simple word overlap calculation
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return 0.0
            
        overlap = len(words1.intersection(words2))
        total = min(len(words1), len(words2))
        
        return overlap / total if total > 0 else 0.0
    
    def set_last_system_response(self, response):
        """Set the last system response for feedback loop detection"""
        self.last_system_response = response

    def get_transcription(self):
        """Get the latest transcription if available"""
        try:
            transcription = self.transcription_queue.get_nowait()
            
            # Check if this is similar to the last system response
            if transcription and self.last_system_response:
                similarity = self._calculate_similarity(transcription, self.last_system_response)
                logging.info(f"Similarity with last response: {similarity}")
                
                if similarity > self.similarity_threshold:
                    logging.warning("Detected feedback loop! Ignoring transcription.")
                    return None
                    
            return transcription
        except queue.Empty:
            return None
            
    def get_status(self):
        """Get the current status of the recorder"""
        with self.status_lock:
            return self.status