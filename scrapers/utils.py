from fake_useragent import UserAgent

ua = UserAgent()

def get_random_user_agent() -> str:
    """Returns a random user agent string to mimic real browsers."""
    try:
        return ua.random
    except Exception:
        # Fallback if fake-useragent fails
        return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
