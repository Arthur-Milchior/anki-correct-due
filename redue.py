from aqt import mw
from aqt.qt import QAction

CARD_NEW = 0
NEW_CARDS_RANDOM = 0

def redue():
    col = mw.col
    sched = col.sched
    
    cids = mw.col.db.list(f"select id from cards where type = {CARD_NEW} and due > 1000000 order by id")
    sched.sortCards(cids)
    col.conf['nextPos'] = col.db.scalar(
        f"select max(due)+1 from cards where type = {CARD_NEW}") or 0

    dconfs = col.decks.dconf

    random_dconfs = [dconf for dconf in dconfs.values() if dconf["new"]['order'] == NEW_CARDS_RANDOM]
    for dconf in random_dconfs:
        sched.resortConf(dconf)



action = QAction(mw)
action.setText("Clean due")
mw.form.menuTools.addAction(action)
action.triggered.connect(redue)
