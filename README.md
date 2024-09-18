# Negotiation Chatbot with Pre-trained AI (Gemini) and Sentiment Analysis

## Overview
This project involves building a negotiation chatbot using a pre-trained AI model (Gemini 1.5 Flash) and sentiment analysis (RoBERTa). The chatbot provides dynamic responses based on the user's sentiment during a product price negotiation.

## Objective
The API enables users to input price offers for a product, and the chatbot responds based on the sentiment of the user’s message (polite, neutral, or negative). The chatbot either accepts the offer, makes a counteroffer, or rejects the offer.

## Features
- **Dynamic Pricing Logic**: Adjusts responses based on the user’s price offer compared to the product price.
- **Sentiment Analysis**: The chatbot's response adapts based on the user's tone (polite, neutral, or negative).
- **Pre-trained AI Integration**: Uses the Gemini 1.5 Flash model for generating responses and RoBERTa for sentiment analysis.
- **Price Extraction**: Automatically extracts the offered price from user input.

## System Components
- **RoBERTa Sentiment Analysis**: Determines if the user is polite, neutral, or negative.
- **Gemini AI Model**: Generates human-like responses based on sentiment and extracted user price.
- **Price Handling**: Logic to suggest counteroffers based on the user's input and sentiment.

## API Endpoints
- **POST /negotiate/**: Takes the product price and user message, extracts the offered price, evaluates sentiment, and returns a response.
- **GET /**: Returns a welcome message to check the API status.

## How to Run
1. Clone the repository:
    ```bash
    git clone https://github.com/Kamalesh-Vijayakumar/Negotiation-Chatbot-with-Pre-trained-AI-Gemini-and-Sentiment-Analysis.git
    cd Negotiation-Chatbot-with-Pre-trained-AI-Gemini-and-Sentiment-Analysis
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your Gemini API key:
    ```
    GEMINI_API_KEY=your_api_key_here
    ```

4. Run the FastAPI server:
    ```bash
    uvicorn app:app --reload
    ```

5. Test the API at `http://127.0.0.1:8000/negotiate/` using tools like Postman.

## Example Request (POST /negotiate/)
```json
{
  "product_price": 1000,
  "user_message": "This product is overpriced! I can only pay $200."
}
```

## Example Response 
```json
{
  "sentiment": "negative",
  "gemini_response": "I understand you're looking for a great deal, but unfortunately, $200 is far below the value of this product. It's priced at $1000. To make this work, we'd need a significantly higher offer. How about starting with $800?"
}
```

## Thankyou 
