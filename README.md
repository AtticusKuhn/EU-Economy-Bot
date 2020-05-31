# EU-Economy-Bot
This is an economy bot for the EU discord server


# Commands that will be added

- $help - shows all commands
- $send (ping person) (wallet name) (amount) - sends an amount to a person from that wallet
- $request (ping person) (amount) - requests some money from a person which her or she can accept or deny
- $tax (ping person) (amount) (wallet name) - if you have the role "taxation" take that amount of money from the person and put it in the wallet
- $print (wallet name) (amount) - creates an amount of money in that wallet if you have the role "printer"
- $burn (wallet name) (amount) - deletes that much money from a wallet
- $balance (wallet name) - returns the amount of money in the wallet
- $config (config option) (config setting) - if you have the admin role, configure the bot. 
    * Earn method - can be message send, time online, length sent, or none.
    * Earn amount - how much money will be earned when someone earns money



# Wallets explained

Wallets are where money is stored. Each person has a personal wallet
and each roles has a communal wallet. Anyone with the role can access the role wallet.
People with the role "taxation" can access any wallet below them in the role heirarchy.




# Errors

- args error - you did not provide the correct amount of arguments
- value error - you do not have enough money
- name error - either the name of a wallet or the name of a person does not exist


# Invite link

You can invite this bot to any server with the link https://discord.com/oauth2/authorize?scope=bot&client_id=716434826151854111