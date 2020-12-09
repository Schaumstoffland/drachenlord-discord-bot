FROM gorialis/discord.py:minimal

COPY src/ /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]