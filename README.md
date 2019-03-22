# MemeHut-Bot
A discord bot for Minehut developers to control their servers.

## Usage
To add the bot to your server go to our official site and follow the instructions there.
https://memehut.github.io/bot/authorization

After adding the bot to your server, run the command !help and you will get a full list of commands. And your done! It's as simple as that.

## Login Policy
In order to add your Minehut server to our bot, we must ask you for your Minehut login credentials. Don't worry, we dont stors your email and password. You can view the source code for the bot on this site. I am going to walk you through the entire login process so that you don't have to worry. 

1. You run the !setup. ommand in your server and we add your user ID to an array of users setting up their accounts.
2. We send you a direct message and wait for your response with your email and password. 
3. When you enter your email, we store it in another array with your user ID, we then wait for your password reply.
4. As soon as we recieve this information it is sent to Minehut's API in an HTTP POST request, so that we can recieve information about your servers.
5. We then remove your email from the previous array, your password was never stored. We store your authorization token for Minehut as well as some other data that will be used to communicate with your server.
6. Thats it! None of your personal information is ever permanently stored on our servers.

Remember you can view the code for this process right here on GitHub.
