from agents import Agent, RunConfig, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from dotenv import load_dotenv
from travel_tools import get_flights, get_hotels
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KYE")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

destination = Agent(
    name= "DestinationAgent",
    instructions= "You recommend travel destination based on user's mood.",
    model=model,
)

booking_agent = Agent(
    name="BookingAgent",
    instructions= "You give flights and hotels info using tools.",
    model=model,
    tools=[get_flights, get_hotels]
)

explore_agent = Agent(
    name="ExploreAgent",
    instructions= "You suggest food & places to explore in the destination.",
    model=model,
)

def main():
    print("\U0001F3D5 AI Travel Designer Agent \U0001F3D5")
    mood = input(" ✈️  What's your travel mood (relaxing/advanture/etc)? ➡ ")

    result1 = Runner.run_sync(destination, mood, run_config=config)
    dest = result1.final_output.strip()
    print(f"\n📍 Destination Suggested: 🌍 {dest}")

    result2 = Runner.run_sync(booking_agent, dest, run_config=config)
    print(f"\n🛫 Booking Info: 🏨\n{result2.final_output}")

    result3 = Runner.run_sync(explore_agent, dest, run_config=config)
    print(f"\n🍱 Explore Tips: 🗺️\n{result3.final_output}")

if __name__ == "__main__":
    main()