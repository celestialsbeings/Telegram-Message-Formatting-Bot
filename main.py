from datetime import date
from urllib.parse import urlparse
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# User data file
USER_DATA_FILE = "user_data.txt"

# Function to shorten URLs with HTML formatting


def is_user_registered(user_id):
    users = load_user_data()
    return user_id in users


def shorten_url(url, custom_text=None):
    url_parts = urlparse(url)
    base_url = f"{url_parts.scheme}://{url_parts.netloc}"
    path = url_parts.path
    if len(path) > 30:
        path = path[:30] + "..."
    if custom_text:
        shortened_url = f'<a href="{url}">{custom_text}</a>'
    else:
        shortened_url = f'<a href="{url}">{base_url}{path}</a>'
    return shortened_url


# Function to format text with HTML tags
# Telegram bot handlers
def start(update, context):
    users = load_user_data()
    user_count = len(users)
    user_id = update.effective_user.id
    user_name = update.effective_user.name
    if not is_user_registered(user_id):
        save_user_data(user_id, user_name)
    message = (
        "👋 Hi there! I'm your friendly URL shortener and text formatter bot. "
        "Send me some text with HTML tags, and I'll make it look stylish for you. 💫\n\n"
        "Here's what I can do for you:\n"
        "➡️ Shorten your URLs\n"
        "➡️ Apply basic text formatting\n"
        "➡️ For more info send /cmds\n\n"
        f"Current Users: {user_count}\n\n"
        "Ready to give it a try?")
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=message,
                             parse_mode='HTML')


def cmds(update, context):
    keyboard = [[
        InlineKeyboardButton("Bold", callback_data='bold_data'),
        InlineKeyboardButton("Underline", callback_data='underline_data')
    ],
                [
                    InlineKeyboardButton("Italic",
                                         callback_data='italic_data'),
                    InlineKeyboardButton("Link Shortner",
                                         callback_data='link_shrink_data')
                ],
                [InlineKeyboardButton("Raw HTML", callback_data='html_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose your command :',
                              reply_markup=reply_markup)


def bold_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text('Example: <code>/bold Your text</code>',
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML)


def underline_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text('Example: <code>/underline Your text</code>',
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML)


def html_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text('Example: html tags <code>Your text</code>',
                            reply_markup=reply_markup)


def italic_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text('Example: <code>/italic Your text</code>',
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML)


def shrink_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back_data')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text(
        'Example: <code>/shrink Your_link Your Coustimise Text</code>',
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML)


def back_callback(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [[
        InlineKeyboardButton("Bold", callback_data='bold_data'),
        InlineKeyboardButton("Underline", callback_data='underline_data')
    ],
                [
                    InlineKeyboardButton("Italic",
                                         callback_data='italic_data'),
                    InlineKeyboardButton("Link Shortner",
                                         callback_data='link_shrink_data')
                ],
                [InlineKeyboardButton("Raw HTML", callback_data='html_data')]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.edit_text('Please choose your command :',
                            reply_markup=reply_markup,
                            parse_mode=ParseMode.HTML)


def button_click(update, context):
    query = update.callback_query
    data = query.data

    # Edit the message to display the text based on the button clicked
    if data == 'bold_data':
        bold_callback(update, context)
    elif data == 'italic_data':
        italic_callback(update, context)
    elif data == 'underline_data':
        underline_callback(update, context)
    elif data == 'link_shrink_data':
        shrink_callback(update, context)
    elif data == 'back_data':
        back_callback(update, context)
    elif data == 'html_data':
        html_callback(update, context)


def format_handler(update, context):
    text = update.message.text
    formatted_text = text
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=formatted_text,
                             parse_mode=ParseMode.HTML)


def bold_handler(update, context):
    text = ' '.join(context.args)
    bold_text = f"<b>{text}</b>"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=bold_text,
                             parse_mode=ParseMode.HTML)


def italic_handler(update, context):
    text = ' '.join(context.args)
    italic_text = f"<i>{text}</i>"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=italic_text,
                             parse_mode=ParseMode.HTML)


def underline_handler(update, context):
    text = ' '.join(context.args)
    underline_text = f"<u>{text}</u>"
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=underline_text,
                             parse_mode=ParseMode.HTML)


def shorten(update, context):
    args = context.args
    if len(args) < 1:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please provide a URL to shorten.")
        return
    url = args[0]
    if len(args) > 1:
        custom_text = ' '.join(args[1:])
        shortened_url = shorten_url(url, custom_text)
    else:
        shortened_url = shorten_url(url)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=shortened_url,
                             parse_mode=ParseMode.HTML)


def broadcast(update, context):
    user_id = update.effective_user.id
    if user_id != 5308059847:  # Replace with your desired admin user ID
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="You are not authorized to use this command.")
        return

    if len(context.args) < 1:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please provide a message to broadcast.")
        return

    message = ' '.join(context.args)
    users = load_user_data()
    for user_id, user_name in users.items():
        try:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Message from admin:\n\n<b>{message}</b>",
                parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Error sending message to user {user_id}: {e}")


def save_user_data(user_id, user_name):
    with open(USER_DATA_FILE, "a") as file:
        file.write(f"{user_id},{user_name}\n")


def load_user_data():
    users = {}
    try:
        with open(USER_DATA_FILE, "r") as file:
            for line in file:
                user_id, user_name = line.strip().split(",")
                users[int(user_id)] = user_name
    except FileNotFoundError:
        pass
    return users


def main():
    updater = Updater(token='6713741076:AAGnXknRCDWOOblqIvMAJW3v5aMSZBP21W8',
                      use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(CommandHandler('cmds', cmds))
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, format_handler))
    dispatcher.add_handler(CommandHandler('bold', bold_handler))
    dispatcher.add_handler(CommandHandler('italic', italic_handler))
    dispatcher.add_handler(CommandHandler('shrink', shorten))
    dispatcher.add_handler(CommandHandler('underline', underline_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(button_click))
    dispatcher.add_handler(CommandHandler('brd', broadcast))
    updater.start_polling()


if __name__ == '__main__':
    main()
