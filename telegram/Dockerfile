FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y supervisor
RUN pip install python-telegram-bot redis asyncio creart python-dotenv requests loguru

# Copy the Telegram bot file
COPY telegram_transport.py sender.py run_bot.py exithooks.py /app/
COPY ./abc_handler /app/abc_handler
COPY .env /app/
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# Set the working directory
WORKDIR /app

# Run the bot
# CMD ["python", "telegram_transport.py"]

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]