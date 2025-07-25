from agents import function_tool

@function_tool
def get_flights(destination: str) -> str:
    return f"Flights found to {destination}: PKR 45,000 - PKR 70,000."

@function_tool
def get_hotels(destination: str) -> str:
    return f"Hotels available in {destination}: Pearl Continental, Marriot, Local Guest Houses."