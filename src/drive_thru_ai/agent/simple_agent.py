import json
import os
from typing import Dict, List, Optional
import logging
from io import BytesIO
import time
import threading
from openai import OpenAI
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

# Import menu items from your package
from drive_thru_ai.menu import Fries, Drink, DrinkType, FountainFlavor, MilkshakeFlavor, Size

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class SimpleDriveThruAgent:
    def __init__(self):
        """Initialize the AI agent with OpenAI API key."""
        # Initialize API clients
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.elevenlabs_client = ElevenLabs(
            api_key=os.getenv('ELEVENLABS_API_KEY'))

        # Initialize order tracking
        self.current_order = []
        
        # Initialize audio playback flag
        self.is_playing_audio = False
        self.audio_lock = threading.Lock()

    def text_to_speech_stream(self, text: str) -> BytesIO:
        """Convert text to speech and return audio stream."""
        try:
            response = self.elevenlabs_client.text_to_speech.convert(
                voice_id="3l9iCMrNSRR0w51JvFB0",
                output_format="mp3_22050_32",
                text=text,
                model_id="eleven_flash_v2_5",
                voice_settings=VoiceSettings(
                    stability=0.0,
                    similarity_boost=1.0,
                    style=0.0,
                    use_speaker_boost=True,
                    speed=1.0,
                ),
            )

            audio_stream = BytesIO()
            for chunk in response:
                if chunk:
                    audio_stream.write(chunk)

            audio_stream.seek(0)
            return audio_stream
        except Exception as e:
            logging.error(f"Error in text_to_speech_stream: {e}")
            return None

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the AI."""
        return """You are a friendly and efficient drive-thru order taker. 
        You only handle orders for:
        1. Fries (small, medium, large)
        2. Fountain Drinks (Coke, Diet Coke) in small, medium, or large
        3. Milkshakes (Vanilla, Chocolate, Strawberry) in small, medium, or large

        When responding to customers:
        1. Be friendly and conversational
        2. Confirm their order details
        3. Ask for any missing information
        4. Use natural language, not technical terms
        5. End your response with a JSON object containing the order details

        Example responses:
        Customer: "I'd like a large fries and a medium coke"
        Assistant: "I'll get that for you! One large fries and a medium Coke coming right up. Is there anything else you'd like today?
        {
            "fries": [{"size": "large", "quantity": 1}],
            "fountain_drinks": [{"flavor": "coke", "size": "medium", "quantity": 1}]
        }"

        Customer: "Can I remove one of the large fries?"
        Assistant: "Of course! I'll take one large fries off your order. Is there anything else you'd like to change?
        {
            "fries": [{"size": "large", "quantity": -1}]
        }"

        Remember to:
        1. Always provide a friendly, natural response first
        2. Include the JSON object at the end of your response
        3. Use negative quantities for removals
        4. Only include items that were ordered or removed
        5. If no quantity is specified, assume quantity of 1
        """

    def process_customer_input(self, customer_input: str, recorder=None) -> str:
        """Process customer input and generate appropriate response.
        
        Args:
            customer_input: The customer's input text
            recorder: Optional AudioRecorder instance for feedback loop prevention
        """
        # Create messages for OpenAI API
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": customer_input}
        ]

        try:
            # Get response from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )

            # Extract the response
            ai_response = response.choices[0].message.content

            # Log the AI response
            logging.info(f"AI Response: {ai_response}")

            # Parse the order from the response
            try:
                order_json = self._extract_json_from_response(ai_response)
                if order_json:
                    self._process_order_json(order_json)
            except Exception as e:
                logging.error(f"Error processing order: {e}")

            # Strip out the JSON part before returning to user
            json_start = ai_response.find('{')
            if json_start != -1:
                user_response = ai_response[:json_start].strip()
            else:
                user_response = ai_response.strip()
            
            # Store the response in the recorder for feedback loop prevention
            if recorder is not None:
                recorder.set_last_system_response(user_response)

            return user_response
            
        except Exception as e:
            logging.error(f"Error in process_customer_input: {e}")
            return "I'm sorry, I couldn't process your order. Could you please repeat that?"

    def _extract_json_from_response(self, response: str) -> Optional[Dict]:
        """Extract JSON from the AI response."""
        try:
            # Find the JSON part in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                return None

            json_str = response[start_idx:end_idx]
            return json.loads(json_str)
        except Exception as e:
            logging.error(f"Error extracting JSON: {e}")
            return None

    def _process_order_json(self, order_json: Dict) -> None:
        """Process the order JSON and add/remove items from the current order."""
        # Process fries
        if "fries" in order_json:
            for fries_order in order_json["fries"]:
                size = Size[fries_order["size"].upper()]
                quantity = fries_order.get("quantity", 1)

                # Handle negative quantities (removing items)
                if quantity < 0:
                    # Remove the specified number of items
                    items_to_remove = abs(quantity)
                    items_removed = 0
                    self.current_order = [
                        item for item in self.current_order
                        if not (isinstance(item, Fries) and item.size == size and items_removed < items_to_remove and (items_removed := items_removed + 1))
                    ]
                else:
                    # Add new items
                    for _ in range(quantity):
                        self.current_order.append(Fries(size))

        # Process fountain drinks
        if "fountain_drinks" in order_json:
            for drink_order in order_json["fountain_drinks"]:
                size = Size[drink_order["size"].upper()]
                flavor = FountainFlavor[drink_order["flavor"].upper()]
                quantity = drink_order.get("quantity", 1)

                # Handle negative quantities (removing items)
                if quantity < 0:
                    # Remove the specified number of items
                    items_to_remove = abs(quantity)
                    items_removed = 0
                    self.current_order = [
                        item for item in self.current_order
                        if not (isinstance(item, Drink) and
                                item.drink_type == DrinkType.FOUNTAIN and
                                item.size == size and
                                item.flavor == flavor and
                                items_removed < items_to_remove and
                                (items_removed := items_removed + 1))
                    ]
                else:
                    # Add new items
                    for _ in range(quantity):
                        self.current_order.append(
                            Drink(DrinkType.FOUNTAIN, flavor, size))

        # Process milkshakes
        if "milkshakes" in order_json:
            for shake_order in order_json["milkshakes"]:
                size = Size[shake_order["size"].upper()]
                flavor = MilkshakeFlavor[shake_order["flavor"].upper()]
                quantity = shake_order.get("quantity", 1)

                # Handle negative quantities (removing items)
                if quantity < 0:
                    # Remove the specified number of items
                    items_to_remove = abs(quantity)
                    items_removed = 0
                    self.current_order = [
                        item for item in self.current_order
                        if not (isinstance(item, Drink) and
                                item.drink_type == DrinkType.MILKSHAKE and
                                item.size == size and
                                item.flavor == flavor and
                                items_removed < items_to_remove and
                                (items_removed := items_removed + 1))
                    ]
                else:
                    # Add new items
                    for _ in range(quantity):
                        self.current_order.append(
                            Drink(DrinkType.MILKSHAKE, flavor, size))

    def get_current_order(self) -> List:
        """Get the current order."""
        return self.current_order

    def clear_order(self) -> None:
        """Clear the current order."""
        self.current_order = []

    def get_order_total(self) -> float:
        """Calculate the total price of the current order."""
        return sum(item.get_price() for item in self.current_order)

    def play_audio(self, audio_stream: BytesIO, recorder=None):
        """Play the audio stream with proper initialization and completion handling.
        
        Args:
            audio_stream: The audio stream to play
            recorder: Optional AudioRecorder instance to notify about playback
        """
        if audio_stream is None:
            logging.error("Cannot play None audio stream")
            return
            
        with self.audio_lock:
            self.is_playing_audio = True
        
        # Notify recorder if provided
        if recorder:
            recorder.is_system_speaking = True
            
        try:
            import pygame
            if not pygame.mixer.get_init():
                pygame.mixer.init()
                
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            # Add cooldown after playback finishes
            if recorder:
                time.sleep(recorder.cooldown_period)
                
        except Exception as e:
            logging.error(f"Error playing audio: {e}")
        finally:
            with self.audio_lock:
                self.is_playing_audio = False
            
            # Reset recorder flag after playback
            if recorder:
                recorder.is_system_speaking = False