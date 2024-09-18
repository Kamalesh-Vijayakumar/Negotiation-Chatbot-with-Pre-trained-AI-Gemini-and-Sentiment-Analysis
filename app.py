import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import get_gemini_response, analyze_sentiment

# Load environment variables
load_dotenv()

app = FastAPI()

# Price negotiation model with only product_price and user_message
class NegotiationInput(BaseModel):
    product_price: float  # Base price of the product
    user_message: str  # User's message for sentiment analysis

# API endpoint for negotiation
@app.post("/negotiate/")
async def negotiate(input: NegotiationInput):
    # Extract the sentiment from the user's message
    sentiment = analyze_sentiment(input.user_message)
    
    # Call the get_gemini_response function from utils.py
    gemini_response = await get_gemini_response(input.product_price, input.user_message)

    if not gemini_response:
        raise HTTPException(status_code=500, detail="Error communicating with Gemini LLM")

    # Return both the sentiment and Gemini response
    return gemini_response

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Gemini LLM Negotiation Chatbot!"}
