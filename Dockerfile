FROM python:3

COPY src/main.py ./

RUN pip3 install discord
RUN pip3 install aiohttp
RUN pip3 install asyncio

CMD ["python3", "main.py"]

