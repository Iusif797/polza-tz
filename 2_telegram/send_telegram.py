#!/usr/bin/env python3
import argparse
import json
import logging
import os
import sys
import urllib.error
import urllib.request
from typing import Optional

# Setup professional logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


class TelegramNotifier:
    """
    A class-based Telegram integration that is easy to extend for other notification types.
    """
    API_URL_TEMPLATE = "https://api.telegram.org/bot{token}/sendMessage"

    def __init__(self, token: str, chat_id: str):
        self.token = token
        self.chat_id = chat_id

    def send_message(self, text: str) -> bool:
        """Sends a text message to the configured chat."""
        url = self.API_URL_TEMPLATE.format(token=self.token)
        payload = {"chat_id": self.chat_id, "text": text}
        
        try:
            body = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode())
                if result.get("ok"):
                    logger.info("Message successfully sent to Telegram")
                    return True
                else:
                    logger.error(f"Telegram API error: {result.get('description')}")
                    return False
                    
        except urllib.error.URLError as e:
            logger.error(f"Network error while connecting to Telegram: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False


def load_environment() -> None:
    """Loads environment variables from .env if available."""
    if load_dotenv:
        load_dotenv()
        # Look for .env in current dir as well
        if os.path.exists(".env"):
            load_dotenv(".env")


def main() -> int:
    load_environment()
    
    parser = argparse.ArgumentParser(description="Send file content to a Telegram chat via bot.")
    parser.add_argument("file", help="Path to .txt file with message body")
    parser.add_argument("--token", default=os.environ.get("BOT_TOKEN"), help="Bot token (optional if BOT_TOKEN set)")
    parser.add_argument("--chat", default=os.environ.get("CHAT_ID"), help="Chat ID (optional if CHAT_ID set)")
    
    args = parser.parse_args()
    
    token = args.token
    chat_id = args.chat
    
    if not token or not chat_id:
        logger.error("BOT_TOKEN and CHAT_ID must be provided (env or args)")
        return 1

    if not os.path.isfile(args.file):
        logger.error(f"File not found: {args.file}")
        return 1

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            
        if not content:
            logger.warning("The provided file is empty. Nothing to send.")
            return 0
            
        notifier = TelegramNotifier(token, chat_id)
        if notifier.send_message(content):
            return 0
        return 1
        
    except Exception as e:
        logger.error(f"Failed to process file: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
