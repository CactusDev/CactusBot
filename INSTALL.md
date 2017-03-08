
## Setup CactusBot:
```
git clone https://github.com/CactusDev/CactusBot
cd CactusBot
pip3 install -r requirements.txt
cp config.template.py config.py
```

Next, open `config.py` with your favorite text editor, and set 
`TOKEN` to the bot's OAuth token, which can be obtained from [Beam's Documentation](https://dev.beam.pro/tutorials/chatbot.html). Then, set `CHANNEL` to your channel's name.

# Usage

## Start RethinkDB:

`rethinkdb`

## Start CactusAPI:

`python run.py`

## Start Sepal:

`npm start`

## Start CactusBot:

`python run.py`
