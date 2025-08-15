
# Import necessary modules for Azure OpenAI client
import os
from openai import AzureOpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


def get_client():
    """Create and return an Azure OpenAI client instance"""
    return AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION",
                              "2024-07-01-preview"),
    )


# Get the model name from environment variable with default fallback
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
