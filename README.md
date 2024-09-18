# Negotiation Chatbot with Gemini AI and Sentiment Analysis

## Project Overview

This project is a negotiation chatbot that simulates price discussions between a user and a seller. It uses the **Gemini AI** language model for generating conversational responses and **RoBERTa** for sentiment analysis. Depending on the sentiment of the user's message (polite, neutral, or negative), the chatbot provides dynamic responses, including counteroffers or rejecting/accepting the user's offer.

## Features

- **Sentiment Analysis**: Detects the user's tone using RoBERTa (polite, neutral, negative).
- **Price Extraction**: Automatically extracts price offers from the user's message.
- **AI-powered Responses**: Uses Gemini AI to simulate human-like price negotiation conversations.
- **Dynamic Counteroffers**: Suggests counteroffers based on user sentiment and the price gap.

## Technologies Used

- **FastAPI**: Framework for building the API.
- **Gemini AI**: Google’s generative AI model for conversation.
- **RoBERTa**: Hugging Face model for sentiment analysis.
- **Regex**: For extracting price from user messages.
- **Python**: Programming language.

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/negotiation-chatbot.git
