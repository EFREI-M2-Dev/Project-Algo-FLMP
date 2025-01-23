from pydantic import BaseModel
from typing import List

class TweetsRequest(BaseModel):
    tweets: List[str]