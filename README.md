# Messy Chat

A small webapp chat designed for use on LANs.

## The Legend of Messy

Once upon a time, in a student dormitory where IOI 2018 contestants were staying, WiFi was so disgraceful that two brave knights had to use their legendary swords -- FrontEnd and BackEnd -- to fight the dragon of loneliness and disconnection. They melted the steel of their swords to create out of them **one** -- the *Messy sword*.

The battle did not last long... Soon enough, the merciless dragon has been defeated. Happiness and smile was all that persisted. The only thing Nation wanted to know is the names of those brave knights. Well, let me tell you: their names were [Martin](https://github.com/1c7718e7) and [Viktor](https://github.com/sharpvik). The only thing people asked from them is to share the *Messy sword* with the public so that everyone will be protected from the flames of this ancient dragon of disconnection.

And thus, we share it with *you*. Remember, this weapon is deadly -- use it wisely and with great respect!

## How to Use

In a terminal, run `python3 server.py` from the root folder to start the server. As soon as the server is running, there are two options as to how to use the Chat:

1. Use Messy via some WiFi network
2. Use Messy via your own WiFi hotspot

### WiFi Network

If you have at your disposal a WiFi network that does not prohibit its IPs from sending direct messages to each other, you can use it to run Messy as follows:

1. Find your device's IP address given to it by the WiFi router
2. Share it will all of your friends
3. To make it work, they will have to be connected to the same WiFi and type your IP + `:80` in an address bar in their browser

Example:

```txt
192.168.0.5:80/

Here, 192.168.0.5 is your IP address on the network.
Just add :80 to it and you are good to go.
```

### WiFi Hotspot

If your device is capable of hosting its own WiFi hotspot, you can use it to run Messy when no other WiFi networks are available. It is always better to use your computer as a WiFi hotspot since mobile devices usually have a limit of around 8 connections for their WiFi hotspot; yet, if you really want to run Messy on your mobile phone, you will need to have this [QPython](https://www.qpython.com/) app (only for Android).

With QPython you can run Python scripts as though it was your PC. As soon as you run *server.py* and your WiFi hotspot is activated, the rest of the process is very similar to what we have covered above.

1. Tell your friends to connect to your WiFi hotspot
2. Find your device's IP
3. Share it with your friends
4. To make it work, they will have to type your IP + `:80` in an address bar in their browser

## Dependencies

+ [python3](https://www.python.org/downloads/release/python-370/) standard library
+ [QPython](https://www.qpython.com/) app *to run on Android mobile devices*