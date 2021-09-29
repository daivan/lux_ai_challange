# Lux AI Challange
This code base is for the https://github.com/Lux-AI-Challenge/Lux-Design-2021 challange

# The code
We are using python to send in our submission

# Prerequisite
You need to install the npm package for lux
```
npm install -g @lux-ai/2021-challenge@latest
```

We are also on Python 3.9

While in the directory you just run:
```
lux-ai-2021 path/to/botfile path/to/otherbotfile
```
In our case it would be:
```
lux-ai-2021 main.py main.py
```

You should see this as a result:
```
[INFO] (match_BGqqWZ6SCUkM) - Design: lux_ai_2021 | Initializing match - ID: BGqqWZ6SCUkM, Name: match_BGqqWZ6SCUkM
{
  ranks: [
    { rank: 1, agentID: 0, name: 'main.py' },
    { rank: 1, agentID: 1, name: 'main.py' }
  ],
  replayFile: 'replays\\1632943472589_BGqqWZ6SCUkM.json',
  seed: 664779212
}
````
Also a replay file should have been created in the replays folder


# To view the replay
Once you have the replay, to view it you can just upload the file here: 

https://2021vis.lux-ai.org/