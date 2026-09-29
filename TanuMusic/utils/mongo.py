from motor.motor_asyncio import AsyncIOMotorClient as MongoCli

from config import MONGO_DB_URI

mongo = MongoCli(MONGO_DB_URI)
db = mongo.TanuMusic

coupledb = db.couple
afkdb = db.afk
nightmodedb = db.nightmode
notesdb = db.notes
filtersdb = db.filters
