FROM python:3.11-slim

# Install dependencies
RUN apt-get update
RUN pip install python-telegram-bot \
redis \
asyncio \
python-dotenv \
loguru

# Copy app files
COPY telegram_client.py .env /app/
COPY ./abc_handler /app/abc_handler
# Set the working directory
WORKDIR /app

# Run the bot logic
CMD ["python", "telegram_client.py"]
