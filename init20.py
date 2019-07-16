# Based on: https://github.com/Arthur-Milchior/anki-correct-due
# Modified version by lovac42 for Anki 2.0 (untest on 2.1)

# Anki's due time is 32bit, but the due field on new cards also
# allows negative numbers. To prevent overflow, during db checkup,
# it is capped at a safe limit of 1,000,000 or about 22bits.

# PSEUDOCODE:
# foreach card in whole_collection {
#    card.due = min(1000000, card.due)
# }

# All cards affected by this will loose their sorting during review.
# This addon repositions the due numbers before the checkup.


# =====================================

# This also removes toolbar menu item.
AUTOMATIC_SCAN_BEFORE_DB_CHECKUP = False

# Priority: due, creation time
REORDER_BY="due,id"

# REORDER_BY="id" #default in Anki API

# =====================================

import anki, random
from anki.hooks import wrap
from aqt.qt import QAction
from aqt import mw
from aqt.utils import tooltip
from anki.utils import ids2str, intTime


NEW_CARDS_RANDOM = 0

SEGMENT = 10001


def redue(col):

    # Save time
    if not col.db.scalar("select id from cards where type=0 and due>=666000"):
        return

    #Doesn't show up on small db
    tooltip(_("found cards with large dues count, repositioning now."), period=2000)
    mw.progress.start()


    #Foreach deck option group
    for dconf in col.decks.dconf.values():

        str_dids = ids2str(col.decks.didsForConf(dconf))

        #Skip small decks
        girth=col.db.scalar(
        """select max(due)+1 from cards
           where type=0 and did in %s"""%str_dids) or 0
        if girth<666000: continue


        #deck conf = "show new cards in randomize order"
        shuffle = dconf['new']['order'] == NEW_CARDS_RANDOM

        redline = col.db.scalar(
        """select max(due)+1 from cards
           where due<666000 and type=0
           and did in %s"""%str_dids) or SEGMENT

        # We use this custom code to avoid sorting by id as users
        # may have customized orders in the due field.
        customSortCards(col, str_dids, start=redline, shuffle=shuffle)


    # Reset pos counter
    col.conf['nextPos'] = col.db.scalar(
        "select max(due)+1 from cards where type = 0") or 0

    mw.progress.finish()




if AUTOMATIC_SCAN_BEFORE_DB_CHECKUP:
    anki.collection._Collection.fixIntegrity = wrap(anki.collection._Collection.fixIntegrity,redue,"before")
else:
    action = QAction(mw)
    action.setText("Clean bulky dues")
    mw.form.menuTools.addAction(action)
    action.triggered.connect(lambda:redue(mw.col))






############################################
##  UTILS.py
###########################################

def customSortCards(col, str_dids, start=1, shuffle=False):
    now = intTime()

    if start <= 65536: #16bits
        limit = "and due>666000 "
        due = start
    else: #reserve the top 0-10k for user custom dues
        limit = "and due>10000 "
        due = SEGMENT

    query = """select id from cards where type=0 %s
               and did in %s order by %s"""

    cids = col.db.list(query%(limit, str_dids, REORDER_BY))
    if shuffle:
        random.shuffle(cids)

    d = []
    for id in cids:
        d.append(dict(now=now, due=due, usn=col.usn(), cid=id))
        due+=1

    col.db.executemany(
        "update cards set due=:due,mod=:now,usn=:usn where id=:cid", d)
