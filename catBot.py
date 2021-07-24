import logging
import pafy
import vlc
import time
from random import random

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

token = "[INSERT_TOKEN_HERE]"

todoList = {}

seconds = 0
minutes = 0
id = [0]
currentWorkingTask = ""
workDone = False

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    userID = update.message.chat_id
    id[0] = userID
    update.message.reply_text(f"""Hi {user.first_name} {user.last_name}! \n
          Welcome to Study Buddy Bot! \n
          Here are my available commands: \n
          1. /add : Add a task to schedule \n
          2. /view : View all current tasks \n
          3. /begin [taskname] : Begins a task \n 
          4. /end : End working on your current task \n
          5. /done : marks a task as done \n
          6. /delete [taskname] : deletes a task. \n
          If you tell me something else I cannot understand, I am just going to echo it back to you:) """)
    todoList[userID] = {}

def echo(update: Update, _: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(f"you said {update.message.text}")


def add(update: Update, _: CallbackContext) -> None:
    userID = update.message.chat_id
    all_words = update.message.text
    todo = all_words.split(" ", 1)[1]
    todoList[userID][todo] = 0
    update.message.reply_text(f"The following task has been added to the list: {todo}")
    #add new todo item together with total time taken = 0


def view(update: Update, _: CallbackContext) -> None:
    userID = update.message.chat_id
    todos = "You have the following tasks in your list: "
    for todo in todoList[userID].keys() :
      todos +="\n" + todo
    update.message.reply_text(todos)



def workDoneAlarm(_: CallbackContext) -> None:
    _.bot.send_message(id[0], text='You have worked for long enough, time to take a break!\nHere is something to make up your day! https://www.youtube.com/watch?v=4uYvm4wHFoQ')

def restDoneAlarm(_: CallbackContext) -> None:
    _.bot.send_message(id[0], text='That\'s enough rest! Begin another task and get back to work again!')


def begin(update: Update, _: CallbackContext) -> None:

    userID = update.message.chat_id
    all_words = update.message.text
    todo = all_words.split(" ", 1)[1]
    currentWorkingTask = todo

    minutes = todoList[userID][todo]
    currentWorkingTask = todo

    print(id[0])

    update.message.reply_text(f"Now beginning on the following task: {todo}")
    _.job_queue.run_once(workDoneAlarm, 15, name = str(userID) + "work")
    _.job_queue.run_once(restDoneAlarm, 20, name = str(userID) + "rest")


def terminateTask(name: str, _: CallbackContext) -> bool:
    currentlyWorking = _.job_queue.get_jobs_by_name(name)
    print(currentlyWorking)
    if len(currentlyWorking) == 0:
        return False
    for task in currentlyWorking:
        task.schedule_removal()
    return True


def end(update: Update, _: CallbackContext) -> None:
    userID = update.message.chat_id
    todoList[userID][currentWorkingTask] = minutes
    workStopped = terminateTask(str(userID) + "work", _)
    restStopped = terminateTask(str(userID) + "rest", _)
    text = 'You have stopped on your current task' if workStopped or restStopped else 'You are not currently working on any task'
    update.message.reply_text(text)


def delete(update: Update, _: CallbackContext) -> None:
    userID = update.message.chat_id
    all_words = update.message.text
    todo = all_words.split(" ", 1)[1]
    del todoList[userID][todo]
    update.message.reply_text(f"The following task has been removed from your list: {todo}")

def done(update: Update, _: CallbackContext) -> None:
    userID = update.message.chat_id
    all_words = update.message.text
    todo = all_words.split(" ", 1)[1]
    todoList[userID][todo + "(done)"] = 0
    todoList[userID].pop(todo)
    update.message.reply_text(f"Great job! You've finished the following task: {todo}")



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("view", view))
    dispatcher.add_handler(CommandHandler("begin", begin))
    dispatcher.add_handler(CommandHandler("end", end))
    dispatcher.add_handler(CommandHandler("delete", delete))
    dispatcher.add_handler(CommandHandler("done", done))


    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
