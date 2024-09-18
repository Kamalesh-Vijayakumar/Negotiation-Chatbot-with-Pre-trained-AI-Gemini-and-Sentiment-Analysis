import re
import os
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import pipeline

# Load environment variables
load_dotenv()

# Configure the Gemini LLM API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model generation configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Function to create the generative model instance with improved prompt engineering
def create_gemini_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=(
            "Respond to a user's price offer for a product by assuming the role of an expert negotiator. You are provided with:\n\n"
            "{price}: The original price of the product.\n{user_price}: The user's offered price.\n{sentiment}: User's emotional sentiment, as assessed through sentiment analysis.\n\n"
            "Objective:\n"
            "1. Acknowledge both the original price and the user's offer.\n"
            "2. Adjust the counteroffer based on the user's sentiment:\n"
            "   - Polite: Decrease the original price by some as a concession.\n"
            "   - Neutral: Propose a price between 80% to 90% of the original price if the user's offer is reasonable. If the user's offer is too low, politely but firmly explain why it is unacceptable.\n"
            "   - Negative: Reject the user's low offer and propose a price closer to the original, signaling that the user must increase their offer.\n"
            "3. If the user offers an extremely low price (e.g., below 30% of the original price), reject the offer firmly, explain why, and propose a realistic counteroffer that is much closer to the original price, typically reducing by no more than 5% to 10% of the product price.\n"
            "4. Suggest a compromise that could facilitate a mutually agreeable resolution but ensure the final price remains within a reasonable range based on market value.\n\n"
            "Do not offer a counter that exceeds the user's budget in unrealistic terms (e.g., avoid significant concessions for very low offers).\n"
            "use different types of words for each customer"
            "5. Dynamic Response Variability:\n"
            "   - Use different phrasing and counteroffer approaches depending on how far the user's offer is from the original price.\n"
            "   - If the gap is large (more than 30% lower), reject the offer firmly and propose only minor concessions (no more than 5-10%).\n"
            "   - Offer flexible but realistic prices. Propose varying counteroffers based on the gap between {user_price} and {price}. The larger the gap, the firmer you should be.\n"
            "6. Respond differently each time based on the offer:\n"
            "   - Use different phrases like 'I appreciate your interest', 'Let's see if we can find some middle ground', or 'Unfortunately, I can't go that low'.\n"
            "   - Use randomized counteroffers based on percentages. For example, reduce the price by 5-15% for polite requests or offer a larger discount if the sentiment is positive.\n"
        )
    )

# RoBERTa-based sentiment analysis using a pre-trained model from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

# Function to extract the price from the user's message
def extract_user_price(user_message: str) -> float:
    # Use regex to extract the first number in the message
    price_match = re.search(r"\d+(?:\.\d{1,2})?", user_message)
    if price_match:
        return float(price_match.group())
    return None  # Return None if no price is found

def analyze_sentiment(user_input: str) -> str:
    # Run sentiment analysis with RoBERTa
    sentiment_result = sentiment_pipeline(user_input)[0]
    label = sentiment_result['label']
    
    # Map the RoBERTa labels to our custom sentiment categories
    if label == "LABEL_2":  # LABEL_2 is usually positive in this model
        return "polite"
    elif label == "LABEL_0":  # LABEL_0 is usually negative in this model
        return "negative"
    return "neutral"  # LABEL_1 is usually neutral

# Function to start a chat session and get the response from Gemini LLM
# Function to start a chat session and get the response from Gemini LLM
async def get_gemini_response(product_price: float, user_message: str):
    # Extract the user price from the message
    user_price = extract_user_price(user_message)
    
    if user_price is None:
        return "Could not extract the user price from the message."

    # Analyze sentiment of the user message
    sentiment = analyze_sentiment(user_message)

    # Create a prompt based on the sentiment
    if sentiment == "polite":
        prompt = f"The user was very polite and respectful in their request to offer ${user_price}. They expressed interest in buying the product at ${user_price}. Please respond in a polite manner by offering a small discount or other concessions."
    elif sentiment == "neutral":
        prompt = f"The user made a neutral offer of ${user_price} for a product priced at ${product_price}. Please respond with a fair counteroffer, balancing the original price and the user's offer."
    else:  # sentiment == "negative"
        prompt = f"The user was a bit negative in their request, offering ${user_price}, which is significantly lower than the product price of ${product_price}. Respond firmly, signaling that the user needs to raise their offer for the deal to proceed."

    # Create the model
    model = create_gemini_model()

    # Start a chat session with the model, using the prompt
    chat_session = model.start_chat(
        history=[{
            "role": "user",
            "parts": [
                f"price: ${product_price}\nuser_price: ${user_price}\nsentiment: \"{sentiment}\"",
            ],
        }]
    )

    # Send the message to the chat session, using the dynamic prompt
    response = chat_session.send_message(prompt)

    # Return the response text and sentiment separately (avoiding duplication)
    return {
        "sentiment": sentiment,
        "gemini_response": response.text
    }
