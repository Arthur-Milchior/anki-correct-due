# Correct new card ordering, clean due number
## Rationale
This add-on solve a problem related to the order of new card. This
problem only appear when the collection is quite big (I had more than
100,000 cards before the problem started to occur), and if you play a
lot with the configuration, trying things. Note that this add-on only
have to be used once, and the bug will be corrected on ankiweb,
ios, ankidroid and any other computer.

More precisely, anki is supposed to show you all new cards of a note
before showing you cards of another note. There are exceptions to this
rules. For example, when you see a card, you may bury its siblings. In
which case the card which should have been shown today is not shown
and another card must be selected. But the main idea is that, if a
note have a few cards, you'll discover all of those cards near in the
same week, or at worst in the same month.

However, it may occurs that suddenly, anki decides to show you the
first card of each note before showing you the second card of any
note. Depending on how you use anki, it may be a real problem, and
there is virtually no way to correct it by yourself. This is why this
add-on is here.

You can see whether you need this add-on by opening a browser, and
searching "due>=1000000". If you see any card it means that this
add-on may help you. Otherwise, this add-on won't hurt, and won't
change anything.

## Usage
In the main window, select "Tools>clean due". And that's it.

## Warning
I can't imagine how this add-on could break anything. I hope this
means warning is useless. However, better be safe, and be sure to make
a back up before trying the add-on.

## Internal
This add-on does not change any method.

Here is the explanation of the cause of the bug, and of the solution.

When selecting a new card in a deck `d`, anki selects the card in `d`,
which is new, not suspended, not buried, and whose `due` value is
minimal. This mean that the only purpose of the `due` value of new
card is to decide in which order new cards will be shown. Intuitively,
the `due` value is a computation, done in advance, to find new cards
quickly. Which means that if this computation had an error, new cards
will be found in the wrong order.

The `due` value of a new note is chosen to be the greatest due value
of the collection, plus one. Which means that the due given to cards
always increase. However, for technical reason, the due is capped at
1,000,000 (this ensures that the due value holds on 32 bits, i.e. on
an int). It is usually not a problem since most collection does not
have a million note. However, if for some reason you have any card
whose `due` value is 1,000,000, all cards will then have this `due`
value. And suddenly `due` does not means anything anymore.

Thus, this add-on recompute the due value of ALL new cards. Hence, if
you have `n` new cards, the due values will be from 0 to `n`. It will
then randomize the order of new cards when the card is in a deck whose
option requires it.


### Possible cause of the problem
The trouble being that, if you change a deck's
option, and choose to see new cards in random order/order of creation,
then anki will give a new due value to each card in decks having this
deck option.

The bug mentionned above is caused by the fact that the due number of
each card is always incremented and never decremented. However

The problem may also occur if, in the browser, you select
`Cards>Reposition` and choose a value at least equal to 1,000,000.

## Version 2.0
Port by [lovac42](https://github.com/lovac42/anki-correct-due)

## Links, licence and credits

Key         |Value
------------|-------------------------------------------------------------------
Copyright   | Arthur Milchior <arthur@milchior.fr>
Based on    | Anki code by Damien Elmes <anki@ichi2.net>
License     | GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
Source in   | https://github.com/Arthur-Milchior/anki-correct-due
Addon number| [127334978](https://ankiweb.net/shared/info/127334978)
Support me on| [![Ko-fi](https://ko-fi.com/img/Kofi_Logo_Blue.svg)](Ko-fi.com/arthurmilchior) or [![Patreon](http://www.milchior.fr/patreon.png)](https://www.patreon.com/bePatron?u=146206)
