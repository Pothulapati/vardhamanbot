from tinydb import TinyDB, Query
from tools.scraper import Scraper

async def reply(activity, bot, data):
    print(data.get_entities())
    credentials = activity.text.split(" ")
    rollno = credentials[0]
    wak = credentials[1]
    if len(wak) > 5:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")
        return
    scraper = Scraper()
    scraper.authenticate(rollno,wak)
    if scraper.authenticated:
        query = Query()
        db = TinyDB('./db.json')
        result = db.search(query.userid == activity.from_property.id)
        if len(result) > 0:
            db.update({'rollno': rollno, 'wak' : wak}, query.userid == activity.from_property.id)
            await bot.send_text_activity(activity, "Authentication Successful!")
        else:
            db.insert({'userid': activity.from_property.id, 'rollno':  rollno, 'wak': wak})
            await bot.send_text_activity(activity, "Authentication Successful!")
    else:
        await bot.send_text_activity(activity, "Please check your roll no. and web access key again.")
        await bot.send_text_activity(activity, "Enter roll no. and web access key seperated by a single space.")