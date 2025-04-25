import asyncio
import json
import sys
from dotenv import load_dotenv
import os


async def test_server():
    # Load environment variables
    load_dotenv()

    # Create a JSON-RPC request
    request = {
        "jsonrpc": "2.0",
        "method": "search",
        "params": {"query": "What is the main class of our application?"},
        "id": "1",
    }

    # Send the request to stdout
    print(json.dumps(request))
    sys.stdout.flush()

    # Wait for response
    while True:
        try:
            response = await asyncio.get_event_loop().run_in_executor(None, input)
            if response:
                print(f"Received response: {response}", file=sys.stderr)
                break
        except EOFError:
            break


if __name__ == "__main__":
    asyncio.run(test_server())
