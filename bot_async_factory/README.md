
# Bot Async Factory: 
Example bot factory include discord, telegram and an app logic where showing how utilize async abstract transport based on abc_handler module.
**link on module**: https://github.com/vzip/async_abc_transport

**Project Structure**:
    - app/
    - discord/
    - telegram/
    - docker-compose.yml

## How to run

1. Install docker engine and compose
2. Create .env from exapmle_env and put your keys
3. Run commands 
    - `docker compose build --no-cache`
    - `docker compose up` or `docker compose up -d`

**Architecture**
All app's import `abc_handler` module directory.

**app/**

- **Dockerfile**: Docker configuration for the app service.
- **abc_handler/**: Module directory of original abc_handler for handling messages and connections.
    - **config_queue.py**: Defined sources names of queues `['discord', 'telegram']` to listen in the `AbstractConnectorAsync` class.
- **bot_logic.py**: The main logic for bot operation. 
    - `get_message` from all queues 
    - get source from message 
    - do logic for that source type, 
    - change source name in message object to `source`_send
    - `push_message` send finally message to queue, on other side reciever will pickup message and delivery by messanger bot client

**discord/**

- **Dockerfile**: Docker configuration for the Discord bot service.
- **abc_handler**: Module directory of original abc_handler for handling messages and connections.
     - **config_queue.py**: Defined sources names for queues `['discord_send']` to listen in the `AbstractConnectorAsync` class.
- **discord_client.py**: Entry point for the Discord transport service.


**telegram/**

- **Dockerfile**: Docker configuration for the Telegram bot service.
- **abc_handler**: Module directory of original abc_handler for handling messages and connections.
     - **config_queue.py**: Defined sources names for queues `['telegram_send']` to listen in the `AbstractConnectorAsync` class.
- **telegram_client.py**: Entry point for the Telegram transport service.




