import requests
import json
import sys

# Your n8n Test Webhook URL
WEBHOOK_URL = "http://localhost:5678/webhook-test/ask-groq"

def main():
    print("=========================================")
    print("🧠 n8n Agent Testing Interface")
    print("Type 'exit' to quit. Type '/reset' to wipe memory.")
    print("=========================================\n")

    # Establish the user identity for this testing session
    chat_id = input("Enter Session ID (e.g., user_47, user_99): ").strip()
    if not chat_id:
        chat_id = "default_user"
    
    print(f"\n✅ Session locked to: {chat_id}")
    print("-----------------------------------------")

    while True:
        # Get user input
        question = input("\nYou: ").strip()

        if question.lower() == 'exit':
            print("Shutting down test engine.")
            sys.exit(0)

        if not question:
            continue

        # Build the JSON payload exactly as n8n expects it
        payload = {
            "question": question,
            "chatId": chat_id
        }

        try:
            # Fire the request to n8n
            response = requests.post(WEBHOOK_URL, json=payload)
            response.raise_for_status() # Check for HTTP errors
            
            # Print the AI's response cleanly
            print(f"\n🤖 Agent: {response.text}")
            
        except requests.exceptions.ConnectionError:
            print("\n❌ ERROR: Could not connect to n8n. Is your n8n Docker container running?")
            print(f"Attempted URL: {WEBHOOK_URL}")
        except Exception as e:
            print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()