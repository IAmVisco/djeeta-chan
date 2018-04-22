# Djeeta-chan
Multipurpose GBF oriented bot for discord servers. Written using [discordbot.py](https://github.com/rauenzi/discordbot.py) which is an extension of a [discord.py lib](https://github.com/Rapptz/discord.py). Any ideas/bugs/issues are welcomed. You can drop me a message in Discord in that case ```IAmVisco#7099``` or use issues tab here, on GitHub.

## Installing
Djeeta bot is currently not avaible for inviting and runs privatly on few servers I am on. She is not really designed for multi server work yet, so if you want to use it you will have to deploy it manually on your machine or server. [Heroku](heroku.com) suits perfectly for this, quick deploy button coming soon.

Just fill the fields in the ```settings.json``` and launch ```start.bat``` (you might need to change it to ```python3 main.py``` in case you have both Python 2 and 3 installed). Also repository has all needed files to deploy on heroku, you can clone/fork this one and set up auto deploy from master branch of your repository.

#### Requirements
Same as for [discord.py lib](https://github.com/Rapptz/discord.py):

- Python 3.4.2+
- `aiohttp` library
- `websockets` library
- `PyNaCl` library (optional, for voice only)
    - On Linux systems this requires the `libffi` library. You can install in
      debian based systems by doing `sudo apt-get install libffi-dev`.

