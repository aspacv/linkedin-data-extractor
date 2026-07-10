import random
import time

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

def clean_text(text):
    return text.strip().replace("\n", " ").replace("\r", "")
