# bot_transport
System with abstract class transport handlers. Include Redis for queues on receive, send methods. Packed in docker instances. 

## How to run

1. Install docker engine and compose
2. Create .env from exapmle_env and put your keys
3. Run commands 
    - `docker compose build --no-cache`
    - `docker compose up` or `docker compose up -d`

## Architecture
## Project Structure

Here's a brief overview of the project structure and what each part is responsible for:

### /app

- **Dockerfile**: Docker configuration for the app service.
- **abc_handler**: Abstract Base Classes for handling messages and connections.
    - **__init__.py**: Initialization file for the Python package.
    - **abstract_connector.py**: Defines the `AbstractConnector` class for all connectors.
    - **handlers.py**: Contains handler classes for processing messages.
- **bot_logic.py**: The main logic for bot operation.
- **example_env**: An example environment file outlining required environment variables.

### /discord

- **Dockerfile**: Docker configuration for the Discord bot service.
- **abc_handler**: Different to `/app/abc_handler`, have some modifications, contains abstract classes and handlers.
- **discord_transport.py**: Entry point for the Discord transport service.
- **sender.py**: Handles sending messages back to the Discord server.
- **supervisord.conf**: Configuration for supervisord to manage multiple processes.
- **example_env**: Example environment variables specific to Discord service.

### /telegram

- **Dockerfile**: Docker configuration for the Telegram bot service.
- **abc_handler**: Different to `/app/abc_handler`, have some modifications, contains abstract classes and handlers.
- **example_env**: Example environment variables specific to Telegram service.
- **exithooks.py**: Utility file for clean exits in the application.
- **run_bot.py**: (If applicable) A separate runner for the Telegram bot.
- **sender.py**: Handles sending messages back to the Telegram server.
- **supervisord.conf**: Configuration for supervisord to manage multiple processes.
- **telegram_transport.py**: Entry point for the Telegram transport service.
