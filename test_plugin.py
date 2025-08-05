import llm
import traceback

def test_plugin():
    try:
        model = llm.get_model("openrouter/openai/gpt-4o")
        response = model.prompt("Get the latest news from Hacker News")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        print("Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_plugin()