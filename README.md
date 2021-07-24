# Lifehack-2021

**This is the Lifehack 2021 submission for Team LiDeLiGong (Ma Zijian and Huang Che Yen).**

##Statement of choice
As technology rapidly infiltrates the education sector and changes not just the way people learn, but also how people teach, what refreshing ideas do you have to make learning/teaching more safe, exciting, and effective?

##What it does
Our Cat Bot works as a study companion bot. It helps the user to manage a series of academic tasks. Users can choose to add, delete tasks into the list of tasks kept by the bot and view all the tasks as well. When the user wants to work on a specific task, the bot starts timing while the user gets to work, after a pre-set period of time, the bot will send a reminder to take a break. Our team sets the work-rest ratio as 45 minutes : 15 minutes, which is believed to be the perfect work rest cycle. Some source of entertainment will also be sent by the bot together with the break reminder. (Link to video of cute cats, thus the name of our bot)

##Challenges we ran into
One of the major challenges we ran into was to perform specific actions(send reminders) after a specific period of time. We have made attempts in writing functions to manually increase variables(seconds, minutes) to keep track of time, but did not work since the functions were not ran at once per second. (We believe this has to do with the clock speed of the CPU) We then ended up researching online and decided to use the JobQueue class from the telegram bot library to keep track of the amount of time needed for the task.

##Instructions to run bot on your own device
This is required on a machine with python installed

Firstly, make sure that python-telegram-bot is installed This can be done by running the following command: !pip install python-telegram-bot

Next, get your own telegram bot token from BotFather in telegram

Input the token into our source code under the following line: token = "[INSERT_TOKEN_HERE]"

Run the code and your bot should now function! (Tested on Google Colaboratory)
