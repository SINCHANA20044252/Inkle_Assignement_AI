"""
Test script for the Multi-Agent Tourism System
Tests the system with example queries from the assignment
"""
from agents import TourismAIAgent
import os
from dotenv import load_dotenv

load_dotenv()


def test_examples():
    """Test the system with the example queries from the assignment"""
    
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return
    
    print("=" * 60)
    print("Testing Multi-Agent Tourism System")
    print("=" * 60)
    
    agent = TourismAIAgent()
    
    # Example 1: Places only
    print("\n" + "=" * 60)
    print("Example 1: Places query")
    print("=" * 60)
    query1 = "I'm going to go to Bangalore, let's plan my trip."
    print(f"\nInput: {query1}")
    print("\nProcessing...")
    response1 = agent.process_query(query1)
    print(f"\nOutput:\n{response1}")
    
    # Example 2: Weather only
    print("\n" + "=" * 60)
    print("Example 2: Weather query")
    print("=" * 60)
    query2 = "I'm going to go to Bangalore, what is the temperature there"
    print(f"\nInput: {query2}")
    print("\nProcessing...")
    response2 = agent.process_query(query2)
    print(f"\nOutput:\n{response2}")
    
    # Example 3: Both weather and places
    print("\n" + "=" * 60)
    print("Example 3: Weather and Places query")
    print("=" * 60)
    query3 = "I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?"
    print(f"\nInput: {query3}")
    print("\nProcessing...")
    response3 = agent.process_query(query3)
    print(f"\nOutput:\n{response3}")
    
    # Test error handling
    print("\n" + "=" * 60)
    print("Example 4: Error handling (non-existent place)")
    print("=" * 60)
    query4 = "I'm going to go to XyzAbc123, let's plan my trip."
    print(f"\nInput: {query4}")
    print("\nProcessing...")
    response4 = agent.process_query(query4)
    print(f"\nOutput:\n{response4}")
    
    print("\n" + "=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_examples()



