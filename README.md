# EU-Economy-Bot
This is an economy bot for the EU discord server



# Inspiration

I wanted a Purely Economic bot for my EU simulator server. I tried to use premade bots, such as tip.cc or unbelieveabot, but they did not suit my criterion. For each I found that many bots rely too much on gambling and games, which I did not want in the EU server. Thus I decided to build a new bot that purely focuses on economics without any games.

# Commands that will be added

- $help - shows all commands
- $send (ping person) (wallet name) (amount) - sends an amount to a person from that wallet
- $request (ping person) (amount) - requests some money from a person which her or she can accept or deny
- $tax (ping person) (amount) (wallet name) - if you have the role "taxation" take that amount of money from the person and put it in the wallet
- $print (wallet name) (amount) - creates an amount of money in that wallet if you have the role "printer"
- $burn (wallet name) (amount) - deletes that much money from a wallet
- $balance (wallet name) - returns the amount of money in the wallet
- DEPRECATED $config (config option) (config setting) - if you have the admin role, configure the bot. 
    * Earn method - can be message send, time online, length sent, or none.
    * Earn amount - how much money will be earned when someone earns money
- $stats - See stats on the economy of the server, such as inflation, GDP, and M0.
- $smart-contract (trigger) (code) - set up a smart contract 


# Wallets explained

Wallets are where money is stored. Each person has a personal wallet
and each roles has a communal wallet. Anyone with the role can access the role wallet.
People with the role "taxation" can access any wallet below them in the role heirarchy.

# Smart Contracts

What sets this bot apart from all other economy bots is smart contracts, allowing for
more complex transactions. Let's look at an example:

$smart-contract message 
```
if(message.content == "I love eu-economy-bot"):
    send(message.author.mention, 10)
    annul()
```

Each person can only have 3 smart contracts, and if a smart contract encounters an error, then it is automatically annuled.


# Errors

- args error - you did not provide the correct amount of arguments
- value error - you do not have enough money
- name error - either the name of a wallet or the name of a person does not exist


# Invite link

You can invite this bot to any server with the link https://discord.com/oauth2/authorize?scope=bot&client_id=716434826151854111
