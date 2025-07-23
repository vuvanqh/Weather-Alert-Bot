from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os, pandas, requests, datetime
from weather_alert import data_file, lat, lon

if not os.path.exists(data_file):
    with open(data_file, 'w'):
        pandas.DataFrame(columns=['user_id', 'name', 'lat', 'lon']).to_csv(data_file)

if not os.path.exists('logs.txt'):
    with open('logs.txt', 'w'): pass
#print(response.json()['list'])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    name = user.full_name

    df = pandas.read_csv(data_file)
    if user_id not in df['user_id'].values:
        df = pandas.concat([df, pandas.DataFrame([{'user_id': user_id, 'name': name, 'lat': lat, 'lon': lon}])], ignore_index=True)
        df.to_csv(data_file,index=False)

    await update.message.reply_text(f"Hello {name}!👋\n Thanks for starting the bot.")

#change lat
async def set_latitude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args)!=1:
        await update.message.reply_text("Please provide latitude as a single number, e.g. /setlatitude 52.9")
        return

    try:
        new_lat = float(context.args[0])
    except ValueError:
        await update.message.reply_text("That's not a valid number. Please enter a decimal numer with dot(.) as a floating point number separator, e.g. /setlatitude 52.9")
        return

    df = pandas.read_csv(data_file)
    if user_id in df['user_id'].values:
        df.loc[df['user_id']==user_id,'lat'] = new_lat

    df.to_csv(data_file,index = False)
    await update.message.reply_text(f"Latitude updated to {new_lat}")

#change lon
async def set_longitude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if len(context.args)!=1:
        await update.message.reply_text("Please provide longitude as a single number, e.g. /setlongitude 52.9")
        return

    try:
        new_lon = float(context.args[0])
    except ValueError:
        await update.message.reply_text("That's not a valid number. Please enter a decimal numer with dot(.) as a floating point number separator, e.g. /setlongitude 52.9")
        return

    df = pandas.read_csv(data_file)
    if user_id in df['user_id'].values:
        df.loc[df['user_id']==user_id,'lon'] = new_lon

    df.to_csv(data_file,index = False)
    await update.message.reply_text(f"Longitude updated to {new_lon}")

#main
def main():
    app = ApplicationBuilder().token(os.environ['Terry_tbot_token']).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("setlatitude",set_latitude))
    app.add_handler(CommandHandler("setlongitude", set_longitude))

    print('Bot is running...')
    app.run_polling()

if __name__ == "__main__":
    main()