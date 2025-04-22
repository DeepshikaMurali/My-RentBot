import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class ChatbotModel:
    def __init__(self):
        # Get API key from environment variables
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
        
        # Default model - you can change this to any model on Hugging Face
        self.model = "facebook/blenderbot-400M-distill"
        # self.model = "google/flan-t5-xl"
        # self.model = "tiiuae/falcon-7b-instruct"
        # self.model = "bigscience/bloomz-7b1"
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Add a system prompt that defines the chatbot's role and behavior
        self.system_prompt = """
        You are RentBot, Your job is to address issues
        - Maintenance requests (leaks, electrical issues, etc.)
        - Rent and lease questions
        - Neighbor complaints
        """
        
        # You are RentBot, a property management assistant with a slightly sassy but helpful personality.
        # Your job is to help tenants with:
        # - Maintenance requests (leaks, electrical issues, etc.)
        # - Rent and lease questions
        # - Neighbor complaints
        # When responding:
        # - Be professional, but use a touch of humor
        # - Ask for specific details when tenants report problems
        # - Give realistic timeframes for repairs and next steps
        # - End with a helpful follow-up question

        # You should always respond according to the user's situation and give them the right advice. 
        
        
        # Keep a conversation history for context
        self.conversation_history = []
        self.max_history_length = 2  # Keep last 4 exchanges for context
        
    def get_response(self, user_message):
        """Get a response from the model for the user's message"""
        # Add the new message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Trim history if needed
        if len(self.conversation_history) > self.max_history_length * 2:  # *2 because each exchange has 2 messages
            self.conversation_history = self.conversation_history[-self.max_history_length * 2:]
        
        # Create a well-structured prompt with context
        prompt = self._create_prompt(user_message)

        #  # TEMP: Just test with a basic prompt to isolate the issue
        # prompt = f"The tenant says: {user_message}\nRentBot:"
        
        # ⚠️ Check if model is ready
        status = requests.get(self.api_url, headers=self.headers).json()
        if status.get("error"):
            print("Model not ready:", status["error"])
            return "RentBot's coffee machine isn't working. Give it a moment ☕"
        
        # Prepare the payload
        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}  # Wait if the model is busy
        }
        
        try:
            # Make a POST request to the Hugging Face API
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload
            )
            
            # ✅ Print raw response for debugging
            # print("Raw response from HF:", response.json())


            # Check if request was successful
            if response.status_code == 200:
                # Parse and return the response
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    # Most models return a list of responses
                    bot_response = result[0].get("generated_text", "I don't know how to respond to that.")
                else:
                    bot_response = result.get("generated_text", "I don't know how to respond to that.")
                
                # Add bot response to history
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                return bot_response
            else:
                print(f"Error: {response.status_code}, {response.text}")
                return "Whoops! The AI tripped over its own thoughts. Please try again!"
                
        except Exception as e:
            print(f"Error calling Hugging Face API: {str(e)}")
            return "Looks like my systems are under maintenance too - ironic, right? Let's try again. What can I help with today?"
    
    def _create_prompt(self, user_message):
        """Create a prompt with system instructions and history."""
        prompt = self.system_prompt.strip() + "\n\n"
        
        # Add chat history
        for msg in self.conversation_history:
            role = "Tenant" if msg["role"] == "user" else "RentBot"
            prompt += f"{role}: {msg['content']}\n"
        
        prompt += f"Tenant: {user_message}\nRentBot:"
        return prompt