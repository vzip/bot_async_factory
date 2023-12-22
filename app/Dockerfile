FROM python:3.9-slim

# Install dependencies
RUN pip install redis loguru python-dotenv

# Copy the bot logic files
COPY bot_logic.py /app/bot_logic.py
COPY ./abc_handler /app/abc_handler

# Set the working directory
WORKDIR /app


# Run the bot logic
CMD ["python", "bot_logic.py"]
