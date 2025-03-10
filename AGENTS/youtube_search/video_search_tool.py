import asyncio
import aiohttp
from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime
import os


# Pydantic models for the results
class VideoSearchResults(BaseModel):
    id: str
    title: str
    channel_id: str
    channel_title: str
    days_since_published: int = Field(..., gt=0, description="Number of days since the video was published")

    @validator('days_since_published')
    def validate_days(cls, v):
        if v <= 0:
            raise ValueError('Days since published must be a positive number.')
        return v


class VideoDetails(BaseModel):
    video_string: str
    title: str
    view_count: int = Field(..., gt=0)
    like_count: int = Field(..., ge=0)
    comment_count: int = Field(..., ge=0)
    subscriber_count: int = Field(..., ge=0)
    score: float = Field(..., ge=0)


# Function to get user input asynchronously
async def get_input(question: str) -> str:
    return input(question)


async def get_topic() -> str:
    return await get_input("Enter a topic to search for: ")


async def get_details(topic: str) -> str:
    return await get_input(f"Enter a description for the video on {topic}: ")


# Function to search videos using YouTube API
async def video_search_tool(topic: str, max_results: int = 5) -> List[VideoSearchResults]:
    results = []
    topic_encoded = topic.replace(' ', '+')  # Manually encoding for simplicity
    # api_key = os.getenv('YOUTUBE_API_KEY')  # Using environment variable for API key
    api_key ="AIzaSyCRRhxYPi_6xTFYa5_D88f9o6myX5GLsYY"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={topic_encoded}&type=video&key={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

            if 'items' in data:
                for item in data['items']:
                    video_id = item['id']['videoId']
                    title = item['snippet']['title']
                    channel_id = item['snippet']['channelId']
                    channel_title = item['snippet']['channelTitle']
                    published_at = item['snippet']['publishedAt']
                    days_since_published = (datetime.utcnow() - datetime.strptime(published_at[:10], "%Y-%m-%d")).days

                    result = VideoSearchResults(
                        id=video_id,
                        title=title,
                        channel_id=channel_id,
                        channel_title=channel_title,
                        days_since_published=days_since_published
                    )
                    results.append(result)

    return results


# Function to get video details
async def video_details_tool(video: VideoSearchResults) -> VideoDetails:
    # api_key = os.getenv('YOUTUBE_API_KEY')
    api_key = "AIzaSyCRRhxYPi_6xTFYa5_D88f9o6myX5GLsYY"
    video_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video.id}&key={api_key}"
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={video.channel_id}&key={api_key}"

    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as video_response, session.get(channel_url) as channel_response:
            video_data = await video_response.json()
            channel_data = await channel_response.json()

            video_item = video_data['items'][0]
            channel_item = channel_data['items'][0]

            title = video_item['snippet']['title']
            view_count = int(video_item['statistics']['viewCount'])
            like_count = int(video_item['statistics']['likeCount'])
            comment_count = int(video_item['statistics']['commentCount'])
            subscriber_count = int(channel_item['statistics']['subscriberCount'])

            video_string = (
                f"   - Title: {title}\n"
                f"   - Channel: {video.channel_title}\n"
                f"   - View Count: {view_count:,}\n"
                f"   - Days Since Published: {video.days_since_published}\n"
                f"   - Likes: {like_count:,}\n"
                f"   - Subscriber Count: {subscriber_count:,}\n"
                f"   - Video URL: https://www.youtube.com/watch?v={video.id}\n"
            )

            score = ((view_count / max(subscriber_count, 1)) * 0.4 +
                     (like_count / max(view_count, 1)) * 0.3 +
                     (comment_count / max(view_count, 1)) * 0.2) * (1 / max(video.days_since_published, 1))

            return VideoDetails(
                video_string=video_string,
                title=title,
                view_count=view_count,
                like_count=like_count,
                comment_count=comment_count,
                subscriber_count=subscriber_count,
                score=score
            )


# Example usage
async def main():
    topic = await get_topic()
    search_results = await video_search_tool(topic)

    if search_results:
        video = search_results[0]  # Process the first result for simplicity
        details = await video_details_tool(video)
        print(details.video_string)
        print(f"Score: {details.score}")


# For running the async functions
if __name__ == "__main__":
    asyncio.run(main())
