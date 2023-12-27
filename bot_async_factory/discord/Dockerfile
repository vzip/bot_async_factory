FROM python:3.11-slim

# Install dependencies
#RUN apt-get update && apt-get install -y supervisor
RUN pip install discord.py redis python-dotenv loguru

# Copy the Discord bot file
COPY discord_client.py .env /app/
COPY ./abc_handler /app/abc_handler
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set the working directory
WORKDIR /app

# Run the bot logic
CMD ["python", "discord_client.py"]

# Run supervisord
# CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

