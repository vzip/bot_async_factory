FROM python:3.11-slim

# Install dependencies
RUN pip install redis \
asyncio \
python-dotenv \
loguru

# Copy the bot logic files
COPY bot_logic.py .env /app/
COPY ./abc_handler /app/abc_handler

# Set the working directory
WORKDIR /app


# Run the bot logic
CMD ["python", "bot_logic.py"]
