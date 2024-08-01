import marvin
import json
import os

# from pydantic import BaseModel
# from textblob import TextBlob
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

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


def generate_response(npc_personality: dict, user_input: str) -> str:
    message_sentiment = marvin.classify(
        user_input, labels=["friendly", "unfriendly", "neutral"]
    )
    message_type = marvin.classify(
        user_input, labels=["greeting", "farewell", "request", "question", "other"]
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
):
    specifics = ", ".join(npc_values)
    instructions = f"Respond this {msg_type} with a {sentiment} message highlighting the following values: {specifics} without giving away the value names"
    # print(instructions)
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
    if sentiment != "neutral" and msg_type == "other":
        for value in npc_values:
            if message_values[value] > npc_personality[value]:
                higher_values += 1
        if higher_values == 0:
            sentiment = "boring"
        if higher_values == 1:
            sentiment = "neutral"
        if higher_values == 2:
            sentiment = "excited"
    else:
        return response_semantics(npc_values, msg_type, user_input, sentiment)

    return response_semantics(npc_values, msg_type, user_input, sentiment)


def main():
    with open(str(npc_settings), "r") as npc:
        npc_personality = json.load(npc)
    user_input = "Hi"
    print(generate_response(npc_personality["npc9"]["attributes"], user_input))


if __name__ == "__main__":
    main()
