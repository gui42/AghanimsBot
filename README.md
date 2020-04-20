<h1>Aghanim's Bot</h1>

  <h2>What does it do?</h2>
  <p>First, aghanim's bot is a work in progress, I'm still learning how this works
 
  The <a href='https://telegram.org/'>telegram</a> bot <a href='https://telegram.me/AghanimsBot'>AghanimsBot</a> is able to get information
  available on <a href='https://www.opendota.com/'>OpenDota</a> and send it
  back to users on the telegram app.
 </p>
 <h2>How can I use the bot?</h2>
 
 <p>You just add <a href='https://telegram.me/AghanimsBot'>@AghanimsBot</a> to a group or start a chat with it</p>
 
 <h2>Commands</h2>
 
 <h3>Flip</h3>
 Returns Heads or Tails, like flipping a coin
 <h3>Dotapos</h3>
 Will return a random dota position to play [Safe lane, Mid lane, Offlane, Soft Support, Hard Support]
 
 <h3>Roll</h3>
 Return a random number, between 1 and 100

<h3>Match</h3>
 Followed by a match id brings back a summary of the game, with the duration, score, and some trivia about the match

<h3>Player</h3>
Followed by the stem32 id of a player, gives a summary of the player profile, with rank, user name, win rate, total games and
the 5 most played heroes.

<h3>Lastmatch</h3>
Using it again followed by the steam32 id of the player.

The bot will send the last game of the player, with focus on the player's hero.

<h3>Help</h3>
The bot will send a list of commands and basic help on how to use them.

<h2>What was used so far</h2>

<a href='https://python-telegram-bot.org/'>Python Telegram Bot</a>

<a href='https://www.opendota.com/'>OpenDota API</a>

<a href='https://github.com/marcusmunch/ranktier'>Ranktier</a>

<a href='https://core.telegram.org/bots/api'>Telegram Bot API</a>
