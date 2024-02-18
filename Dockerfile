FROM 	--platform=linux/amd64 python:latest
ENV     \
        PLEX_TOKEN="" \
        PLEX_URL="http://localhost:32400"
COPY    ./requirements.txt ./
RUN     pip install --no-cache-dir -r requirements.txt
COPY    PlexPreferNonForcedSubs.py .
CMD     [ "python", "./PlexPreferNonForcedSubs.py" ]
