from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class GeolocationRequest(Model):
    address: str

class GeolocationResponse(Model):
    latitude: float
    longitude: float

AGENT_MAILBOX_KEY = "25eb6f8b-7a5b-448e-b88d-b3104156f5f8"

agent = Agent(
    name="user",
    seed = 'geolocation seed 2024 again',
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
    port = 8001
)

AI_AGENT_ADDRESS = "agent1qvnpu46exfw4jazkhwxdqpq48kcdg0u0ak3mz36yg93ej06xntklsxcwplc"

GOOGLE_MAPS_POI_AGENT_ADDRESS = "agent1qwzl3gekyh3034ynqz5e0jem35wszgjp69wxk68yavsuagqapdxjktfv0e9"

address = "Munich, Germany"

@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=address))
    ctx.logger.info(f"Sent address to Geolocation agent: {address}")


@agent.on_message(model=GeolocationResponse)
async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")
    
    await ctx.send(GOOGLE_MAPS_POI_AGENT_ADDRESS, GeolocationResponse(latitude = msg.latitude, longitude = msg.longitude))


if __name__ == "__main__":
    agent.run()
