"""Small helpers for generating unique test data (avoids collisions on the
shared public demo site when running tests that create accounts/data)."""

import random
import string
import time


def unique_email(prefix="qa.portfolio"):
    suffix = f"{int(time.time())}{random.randint(100, 999)}"
    return f"{prefix}.{suffix}@example.com"


def random_string(length=10):
    return "".join(random.choices(string.ascii_lowercase, k=length))
