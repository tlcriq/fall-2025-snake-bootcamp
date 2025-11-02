import asyncio
import time
import socketio
from aiohttp import web
from typing import Any, Dict


#from model import DQN
from game import Game


# TODO: Create a SocketIO server instance with CORS settings to allow connections from frontend
# Example: sio = socketio.AsyncServer(cors_allowed_origins="*")
# TODO: Create a web application instance
# Example: app = web.Application()
# TODO: Attach the socketio server to the web app
# Example: sio.attach(app)
sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)


# Basic health check endpoint - keep this for server monitoring
async def handle_ping(request: Any) -> Any:
    """Simple ping endpoint to keep server alive and check if it's running"""
    return web.json_response({"message": "pong"})


# TODO: Create a socketio event handler for when clients connect
@sio.event
async def connect(sid: str, environ: Dict[str, Any]) -> None:
    """Handle client connections - called when a frontend connects to the server"""
    # TODO: Print a message showing which client connected
    # TODO: You might want to initialize game state here
    print("Connecting to:", sid)
    await start_game(sid, environ)
    pass


# TODO: Create a socketio event handler for when clients disconnect
@sio.event
async def disconnect(sid: str) -> None:
    """Handle client disconnections - cleanup any resources"""
    # Print a message showing which client disconnected
    # TODO: Clean up any game sessions or resources for this client
    print(sid, "has disconnected.")
    update_game(sid)
    try:
        await sio.save_session(sid, {})
    except Exception as e:
        print("couldn't end session for",sid)


# TODO: Create a socketio event handler for starting a new game
@sio.event
async def start_game(sid: str, data: Dict[str, Any]) -> None:
    """Initialize a new game when the frontend requests it"""
    # TODO: Extract game parameters from data (grid_width, grid_height, starting_tick)
    # TODO: Create a new Game instance and configure it
    width = int(data.get("grid_width", 29))
    height = int(data.get("grid_height", 19))
    tick = int(data.get("starting_tick", time.time()))
    game = Game()

    game.grid_width = width
    game.grid_height = height
    game.last_tick = tick

    # TODO: If implementing AI, create an agent instance here
    # TODO: Save the game state in the session using sio.save_session()
    # TODO: Send initial game state to the client using sio.emit()
    # TODO: Start the game update loop

    sio.save_session(sid, game.send())
    sio.emit("start_game",game.send(),sid)

    update_game(sid)


# TODO: Optional - Create event handlers for saving/loading AI models


# TODO: Implement the main game loop
async def update_game(sid: str) -> None:
    """Main game loop - runs continuously while the game is active"""
    # TODO: Create an infinite loop
    # TODO: Check if the session still exists (client hasn't disconnected)
    # TODO: Get the current game and agent state from the session
    # TODO: Implement AI agentic decisions
    # TODO: Update the game state (move snake, check collisions, etc.)
    # TODO: Save the updated session
    # TODO: Send the updated game state to the client
    # TODO: Wait for the appropriate game tick interval before next update
    while True:
        if not sio.connected:
            break
        session = sio.get_session(sid)
        
        snake = session["snake"]
        snake.move()

        sio.save_session(sid, session)
        sio.emit("start_game", session, sid)

        update_game(sid)
        



# TODO: Helper function for AI agent interaction with game
async def update_agent_game_state(game: Game, agent: Any) -> None:
    """Handle AI agent decision making and training"""
    # TODO: Get the current game state for the agent
    # TODO: Have the agent choose an action (forward, turn left, turn right)
    # TODO: Convert the agent's action to a game direction
    # TODO: Apply the direction change to the game
    # TODO: Step the game forward one frame
    # TODO: Calculate the reward for this action
    # TODO: Get the new game state after the action
    # TODO: Train the agent on this experience (short-term memory)
    # TODO: Store this experience in the agent's memory
    # TODO: If the game ended:
    #   - Train the agent's long-term memory
    #   - Update statistics (games played, average score)
    #   - Reset the game for the next round
    game.step()
    if not game.running():
        game.reset()


# TODO: Main server startup function
async def main() -> None:
    """Start the web server and socketio server"""
    # TODO: Add the ping endpoint to the web app router
    # TODO: Create and configure the web server runner
    # TODO: Start the server on the appropriate host and port
    # TODO: Print server startup message
    # TODO: Keep the server running indefinitely
    # TODO: Handle any errors gracefully
    app.router.add_get("/ping", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()



if __name__ == "__main__":
    asyncio.run(main())
