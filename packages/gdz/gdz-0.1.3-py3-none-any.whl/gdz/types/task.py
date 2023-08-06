from pydantic import BaseModel


class Task(BaseModel):
    title: str
    title_short: str
    description: str
    youtube_video_id: str
    url: str
