from pydantic import BaseModel

class TextInput(BaseModel):
    message_input: str
    client_id: str