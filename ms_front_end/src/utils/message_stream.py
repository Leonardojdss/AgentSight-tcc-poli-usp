import time
import numpy as np
import pandas as pd

class MessageStreamComportment:
    
    @staticmethod
    def stream_data(response_agent: str):
        
        for word in response_agent.split(" "):
            yield word + " "
            time.sleep(0.02)