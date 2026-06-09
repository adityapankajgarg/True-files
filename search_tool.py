import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_claim(claim):
    try:
        response = client.search(
            query=claim,
            max_results=5
        )

        return response.get("results", [])

    except Exception as e:
        print("Search error:", e)
        return []