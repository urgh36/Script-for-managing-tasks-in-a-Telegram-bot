from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from telegram.ext import ConversationHandler

tasks = []

ADDING_TASK, VIEWING_TASKS, DELETING_TASK = range(3)

# Команда для начала добавления задачи
def start_adding_task(update: Update, context: CallbackContext):
    update.message.reply_text("Введите задачу, которую хотите добавить:")
    return ADDING_TASK

# Функция для обработки добавления задачи
def add_task(update: Update, context: CallbackContext):
    task = update.message.text
    tasks.append(task)
    update.message.reply_text(f"Задача '{task}' успешно добавлена!")
    return ConversationHandler.END

# Команда для просмотра всех задач
def view_tasks(update: Update, context: CallbackContext):
    if tasks:
        tasks_str = '\n'.join(tasks)
        update.message.reply_text(f"Ваши задачи:\n{tasks_str}")
    else:
        update.message.reply_text("У вас пока нет задач.")

# Команда для удаления задачи
def delete_task(update: Update, context: CallbackContext):
    task_index = int(update.message.text) - 1
    if task_index < len(tasks) and task_index >= 0:
        deleted_task = tasks.pop(task_index)
        update.message.reply_text(f"Задача '{deleted_task}' успешно удалена!")
    else:
        update.message.reply_text("Неверный номер задачи.")

def main() -> None:
    updater = Updater('YOUR_BOT_TOKEN')

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addtask', start_adding_task)],
        states={
            ADDING_TASK: [MessageHandler(Filters.text & ~Filters.command, add_task)]
        },
        fallbacks=[]
    )

    dispatcher.add_handler(CommandHandler('viewtasks', view_tasks))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^\d+$'), delete_task))
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()