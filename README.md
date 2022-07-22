So! Fun idea. A Discord bot and web page 

Bot side:

Features:
- [X] Connect to configured channel and server
- [X] Scan configured channel for past, missed votes
- [X] Handle !watchwith message
- [X] If movie suggestion rejected, suggest another for the same group
- [ ] Handle !remove movie
- [ ] Watch configured channel for new suggestions and votes
- [ ] Show image from Wikipedia for show
- [ ] Show description from Wikipedia for show
- [ ] Show Rotten Tomatoes scores


Web side:
- [ ] Option to vote on shows
- [ ] Option to choose show by clicking avatars

Build procedure:
Note, at the moment this is a personal project, and is not simple to build or use. There are hardcoded channel IDs and stuff like that. Really not ready for use yet by anyone but me. And since I'm the main target for this application, it may never be. You have been warned :)

0. Create a virtual environment, install everything using `pip install -r requirements.txt`
1. Updated the `config.yml` file with your database connection info
2. Build the updated wheel using `python -m build`
3. Make sure the Dockerfile contains the path to the just built wheel
4. Build the docker image using `docker build .`
5. Run the built using docker image using the following command:
```
docker run \
 -d \
 --name moviebot \
 --restart unless-stopped \
 --network=host \
 moviebot
```