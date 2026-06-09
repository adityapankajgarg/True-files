import os
from groq import Groq
from dotenv import load_dotenv
from search_tool import search_claim

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_agent(claim):

    results = search_claim(claim)

    # If nothing useful was found
    if len(results) == 0:
        return {
            "verdict": "UNVERIFIED",
            "confidence": 0,
            "summary": "I couldn't find reliable information about this claim online.",
            "supporting": [],
            "contradicting": [],
            "sources": [],
            "ask_for_source": True
        }

    evidence = "\n".join(
        [
            f"Title: {r.get('title', '')}\n"
            f"Content: {r.get('content', '')}\n"
            f"URL: {r.get('url', '')}\n"
            for r in results
        ]
    )

    prompt = f"""
You are a fact-checking assistant.

A user wants to verify this claim:

"{claim}"

Based ONLY on the evidence below, determine whether the claim is:

TRUE
FALSE
MISLEADING
UNVERIFIED

Return your answer STRICTLY in this JSON format:

{{
    "verdict": "TRUE/FALSE/MISLEADING/UNVERIFIED",
    "confidence": number between 0 and 100,
    "summary": "brief explanation",
    "supporting": ["point1", "point2"],
    "contradicting": ["point1", "point2"]
}}

Evidence:

{evidence}
"""

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        import json

        result = json.loads(answer)

        result["sources"] = [
            {
                "title": r.get("title", "Source"),
                "url": r.get("url", "#")
            }
            for r in results[:4]
        ]

        result["ask_for_source"] = False

        return result

    except Exception as e:

        print(e)

        return {
            "verdict": "UNVERIFIED",
            "confidence": 0,
            "summary": "Something went wrong while analyzing the claim.",
            "supporting": [],
            "contradicting": [],
            "sources": [],
            "ask_for_source": False
        }