Text-based dungeon-crawler-like adventure game.
Basically a maze of rooms.
as you travel between rooms, your life points go away.

To traverse through certain rooms, one must play a challenge. These challenges get harder and different as you move along.

The game has a life-points system, as you move on you drain lifepoints, but you can also gain them as well.

The timing factor is mainly implemented as simple sleep timers between events.

To play the game, you must traverse between rooms by using the north/south/east/west commands.
Other commands:
help <- lists commands and what they do
map <- draws a map of the level
exit <- quits the game.

1.Playing the game should require some skill (math, memory, typing speed, or something)
-> game has challenges that get harder as you move along.

2.The game should end when a maximum number of lives (tries) has been used up.
-> User starts with a fixed amount of lifepoints, they drain as you go along, or are replenished as you beat challenges.

3.The difficulty should increase as the game, or life, goes on
-> difficulty increases as you get closer to finish

4.The game should have some element of timing, either by limiting the time allowed for an answer, move, input, etc, or by limiting the time that the question, sequence, or whatever is displayed. 
Update: Since this can be difficult to achieve in a terminal application, you may satisfy this requirement by using time.sleep() to add appropriate dramatic pauses in your game.  This could be done, for example, when the game starts, when the player advances to the next level, when the player loses a life, and so on.
-> various time.sleep() functions for better usability

5.It should do input validation and error recovery.  The game should not crash because the user made an incorrect input (though the user may lose a life)
-> done. Usually try-catch.