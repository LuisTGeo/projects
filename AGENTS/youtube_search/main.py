import asyncio
import aiohttp
import json
import os
from pydantic import BaseModel
from typing import List
from dirtyjson import loads as djson_parse
from video_search_tool import get_topic, get_details, video_search_tool, video_details_tool
from prompts import titleprompt, descriptionprompt, announcementprompt
import ollama


# Pydantic models
class VideoDetails(BaseModel):
    video_string: str
    title: str
    view_count: int
    like_count: int
    comment_count: int
    subscriber_count: int
    score: float


# Function to sort videos by score
def sort_videos_by_score(videos: List[VideoDetails]) -> List[VideoDetails]:
    return sorted(videos, key=lambda x: x.score, reverse=True)[:15]


# Function to display videos with scores
def display_videos(videos: List[VideoDetails]):
    for index, video in enumerate(videos):
        print(f"Video {index + 1}: {video.score}")
        print(video.video_string)


# Function to generate content using Ollama
def generate_with_ollama(model: str, system_prompt: str, prompt: str, format_type: str = "json") -> dict:
    response = ollama.generate(
        model=model,
        system=system_prompt,
        format=format_type,
        prompt=prompt
    )
    return json.loads(response['response'])


async def main():
    # Static topic and details for testing
    topic = "ai models local ollama"
    details = ("You are going to create a new model for ollama. "
               "Use the modelfile to create an AI model in creative ways "
               "and do interesting things using parameters, system prompt, and more.")

    # Fetch video search results and their details
    videos = await video_search_tool(topic, max_results=5)
    scored_videos = []

    for video in videos:
        video_details = await video_details_tool(video)
        scored_videos.append(video_details)

    # Sort videos by score and select top 15
    top_videos = sort_videos_by_score(scored_videos)
    display_videos(top_videos)

    # Prepare titles using Ollama
    template = "{titles: ['title1', 'title2']}"
    title_prompt = f"topic: {topic}\nDescription: {details}\nSuccessful titles:\n{''.join([video.title for video in top_videos])} Output as JSON, using this template: {template} "
    title_list = generate_with_ollama(model="llama3.2", system_prompt=titleprompt, prompt=title_prompt)
    formatted_titles = "\n".join([f"- {title}" for title in title_list.values()])
    formatted_titles = "\n".join([f"- {title}" for title in title_list.values()])
    print(f"{formatted_titles}\n")

    # Prepare new description using Ollama
    description_prompt = f"topic: {topic}\nDescription: {details}\nOutput as JSON, using this template: {{'output': 'description of the video'}}"
    new_description = generate_with_ollama("llama3.2", descriptionprompt, description_prompt)
    parsed_description = new_description['output']
    print(f"Description for the video based on: {details}\n{parsed_description}")

    # Prepare email announcement using Ollama
    email_prompt = f"topic: {topic}\nDescription: {parsed_description}\nOutput as JSON, using this template: {{'output': 'text of the email'}}"
    email =  generate_with_ollama("llama3.2", announcementprompt, email_prompt)
    parsed_email = email['output']
    print(f"Email for the video based on the generated description: \n{parsed_email}")


if __name__ == "__main__":
    asyncio.run(main())
