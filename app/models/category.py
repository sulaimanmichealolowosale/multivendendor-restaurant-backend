from datetime import datetime
from pydantic import BaseModel, Field


class Category(BaseModel):
    value: str
    title: str
    image_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# category_model = {
#     'value': {'type': 'string', 'minlength': 4, 'maxlength': 50},
#     'title': {'type': 'string', 'minlength': 3, 'maxlength': 50},
#     'image_url': {'type': 'string', 'minlength': 3, 'maxlength': 50},
#     'created_at': {'type': 'date', 'default': datetime.utcnow}
# }
