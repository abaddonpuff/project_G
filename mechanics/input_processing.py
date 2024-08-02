import marvin
import json
import os
from enum import Enum

# from pydantic import BaseModel
# from textblob import TextBlob
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# ENVIRONMENT
OAI_KEY = os.getenv("OPEN_AI_API_KEY")
npc_settings = Path.cwd() / "characters" / "npc" / "npc_settings.json"
marvin.settings.openai.api_key = OAI_KEY

# class MessagePersonality():
# "Intelligence": 17,
#             "Honesty": 97,
#             "Patience": 35,
#             "Humor": 66,
#             "Ambition": 66,
#             "Affection": 0,
#             "Confidence": 23,
#             "Adventurousness": 87,
#             "Empathy": 25


class ResponseValues(Enum):
    BLUNT = 0
    NEUTRAL = 1
    EXCITED = 2


def generate_response(npc_personality: dict, user_input: str) -> str:
    message_sentiment = marvin.classify(
        user_input, labels=["friendly", "unfriendly", "neutral"]
    )
    message_type = marvin.classify(
        user_input, labels=["greeting", "farewell", "request", "question", "message"]
    )
    top_values = [
        element[0]
        for element in (
            sorted(npc_personality.items(), key=lambda item: item[1], reverse=True)[:2]
        )
    ]
    message_values = json.loads(
        marvin.cast(
            user_input,
            target=str,
            instructions="Get how much Intelligence, Honesty, Patience, Humor, Ambition, Affection, Confidence, Adventurousness or Empathy the message has; classify in a scale of 0-100",
        )
    )

    response = evaluate_response(
        message_sentiment,
        message_type,
        npc_personality,
        top_values,
        message_values,
        user_input,
    )
    return response


def response_semantics(
    npc_values: list, msg_type: str, user_input: str, sentiment: str
) -> str:
    specifics = " and ".join(npc_values)
    instructions = (
        f"Respond this {msg_type} with a {sentiment} message that express {specifics}"
    )
    print(instructions)
    response = marvin.cast(user_input, target=str, instructions=instructions)

    return response


def evaluate_response(
    sentiment: str,
    msg_type: str,
    npc_personality: dict,
    npc_values: list,
    message_values: dict,
    user_input: str,
) -> str:
    higher_values = 0
    # Check the message to not be neutral so the player tries to win.
    print(f"Values of the message {message_values}")
    if msg_type != "greeting" or msg_type != "farewell":
        if sentiment == "unfriendly":
            response_sentiment = "angry"
        else:
            for value in npc_values:
                print(
                    f"Comparing message: {message_values[value]} agains NPC: {npc_personality[value]}"
                )
                if message_values[value] > npc_personality[value]:
                    higher_values += 1
            print(f"Matching values: {higher_values}")
            if higher_values == ResponseValues["BLUNT"].value:
                response_sentiment = "blunt"
            elif higher_values == ResponseValues["NEUTRAL"].value:
                response_sentiment = "neutral"
            elif higher_values == ResponseValues["EXCITED"].value:
                response_sentiment = "excited"
        return response_semantics(npc_values, msg_type, user_input, response_sentiment)
    else:
        response_sentiment = "neutral"
        return response_semantics(npc_values, msg_type, user_input, response_sentiment)


def main():
    with open(str(npc_settings), "r") as npc:
        npc_personality = json.load(npc)
    user_input = "Hi! How are you today?"
    print(generate_response(npc_personality["npc9"]["attributes"], user_input))


if __name__ == "__main__":
    main()
