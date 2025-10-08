import httpx
from groq import Groq, DefaultHttpxClient
from . import config

# --- The Master Fix: A Robust, Resilient API Client ---

# 1. Define a longer timeout. The default is too short for real-world internet.
# We'll set it to 30 seconds.
timeout = httpx.Timeout(30.0, connect=10.0)

# 2. Configure automatic retries. If a request fails due to a network error
# or a rate limit (429), it will automatically wait and try again.
transport = httpx.HTTPTransport(retries=3)

# 3. Create a custom, production-ready httpx client instance
custom_httpx_client = DefaultHttpxClient(
    timeout=timeout,
    transport=transport,
)

# 4. Initialize the Groq client with our new, robust settings.
# This single change will make every API call in your entire project more stable.
client = Groq(
    api_key=config.GROQ_API_KEY,
    http_client=custom_httpx_client,
)

print("Initialized a robust, production-ready API client with increased timeouts and automatic retries.")