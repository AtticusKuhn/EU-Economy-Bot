# EU-Economy-Bot
This is an economy bot for the EU discord server, but its
features are so flexible as to be applicable to any economy or roleplay discord server.





# Inspiration

I wanted a Purely Economic bot for my EU simulator server. I tried to use premade bots, such as tip.cc or unbelieveabot, but they did not suit my criterion. For each I found that many bots rely too much on gambling and games, which I did not want in the EU server. Thus I decided to build a new bot that purely focuses on economics without any games.
This bot focuses on flexability and freedom, allowing
members and admins to bring the most customizability to any discord server.

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
- $stats (wallet)- See stats on the economy of the server, such as inflation, GDP, and M0.
- $smart-contract (trigger) (code) - set up a smart contract
- $send-each (condition) (amount) - send money to each person who satisfies that condition
- $whois (condition) - returns which people satisfy condition. Useful for send-each




# Wallets explained

Wallets are where money is stored. Each person has a personal wallet
and each roles has a communal wallet. Anyone with the role can access the role wallet.
People with the role "taxation" can access any wallet below them in the role heirarchy.

# Smart Contracts

What sets this bot apart from all other economy bots is smart contracts, allowing for
more complex transactions. Let's look at an example:

$smart-contract message 
```
output = send(message.guild,"<@464954455029317633>",message,author.mention,"1")
```

This smart contract will send $1 from my personal account to the person who sent the message.
Each person can only have 3 smart contracts, and if a smart contract encounters an error, then it is automatically annuled.


# Alternate currencies/items

If your server wants multiple currencies or items to be supported, then we have you covered. Add a - and the name of the currency
afterwards, as an example, $set-balance @euler 1-peso will set the peso balance of me to 1.


# Conditions
Commands such as send-each use conditions to allow you to send to each person who satisfies a condition. 
The currently availiable keywords for conditions are `not, and, or, everyone, online, offline, bot`.
You can see which people satisfy a condition with whois.


# Invite link

You can invite this bot to any server with the link https://discord.com/api/oauth2/authorize?client_id=716434826151854111&permissions=268503104&scope=bot
