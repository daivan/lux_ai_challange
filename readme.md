# Lux AI Challange 2021
The competition runs until December 6th 2021  
This code base is for the https://github.com/Lux-AI-Challenge/Lux-Design-2021 challange.

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

# The code
We are using python to send in our submission  
You will spend most of your time coding in the agent.py file
This is our reference https://www.youtube.com/watch?v=6_GXTbTL9Uc

To get all the API https://github.com/Lux-AI-Challenge/Lux-Design-2021/tree/master/kits

# Debugging
To try and understand what happen, try and add log entries in different places
```
with open(logfile,"a") as f:
    f.write(f"Enter log text or {variableArray['key']} here \n")
```
It should be printed in the agent.log file.

# Submit your bot
When you are ready to submit, just compress your bot with this simple command:
```
tar -czvf daivanbot.tar.gz *
```
You should now have a file called daivanbot.tar.gz

Go to the website https://www.kaggle.com/c/lux-ai-2021  
Make sure you are logged in and have a verified account.  

Click [Submit Agent]
Go to the site https://www.kaggle.com/c/lux-ai-2021/submit

## Follow the steps:
You can submit as many agents as you want.  
Follow these instructions to submit a new agent

### Step 1 
Upload submission file. Here you want to attach the recently zipped tar.gz file.

### Step 2
Write a description of what is new with the bot from your previous iterations.

### Step 3
Click on submit and just wait.  
After a few minutes you will see your new entry in the [My submissions](https://www.kaggle.com/c/lux-ai-2021/submissions) page.
