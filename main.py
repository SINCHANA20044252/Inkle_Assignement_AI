"""
Main application for Multi-Agent Tourism System
"""
from agents import TourismAIAgent
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    """Main application loop"""
    print("=" * 60)
    print("Multi-Agent Tourism System")
    print("=" * 60)
    print("\nEnter a place you want to visit, and I'll help you plan your trip!")
    print("You can ask about weather, places to visit, or both.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    # Initialize the tourism agent
    agent = TourismAIAgent()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Tourism System. Have a great trip!")
                break
            
            print("\nProcessing your request...")
            response = agent.process_query(user_input)
            print(f"\nAgent: {response}")
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tourism System. Have a great trip!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")


if __name__ == "__main__":
    main()



