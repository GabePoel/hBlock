# hBlock

A simple command line interface for blocking websites via hosts.

## Installing hBlock

To install just run `sudo sh install.sh`. You might see an error like `ln: failed to create symbolic link '/usr/bin/python': File exists`. But, this isn't a problem. It just means part of the setup is already complete. Here's a command to do everything at once:

```$ git clone https://github.com/GabePoel/hBlock.git && sudo sh hBlock/install.sh && sudo rm hBlock -r```

## Using hBlock

Unfortinately, hblock always needs to be run as root. Don't worry. It doesn't do anything scary. It just needs to always be able to edit your hosts file. (Okay that's a _little_ bit scary. But, not sooooo bad.) You can see all the basic commands by running `sudo hblock help` which should show something like the following.

```
Available commands:
 - active..................................Shows which block lists are active.
 - add [block list] [domains]..............Adds domains to block list.
 - remove [block list] [domains]...........Removes domains from block list.
 - show [block list].......................Shows all the domains in the block list.
 - everything..............................Shows all domains in all block lists.
 - set [block list] [on/off]...............Turns the block list on or off.
 - enable..................................Turns on all block lists.
 - disable.................................Turns off all block lists.
 - new [block list] [domains]..............Makes a new block list with specified domains.
 - delete [block list].....................Deletes block list.
 - rename [block list] [new name]..........Renames block list to the new name.
 - setup...................................Automatically sets up hblock on first install.
 - reset...................................Reset hblock to its default state.
 - update..................................Forces update of hosts file.
 - import [block list] [path]..............Imports block list with specified name.
 - export [block list] [path]..............Exports block list to specified path.
 - help....................................Shows available commands.
```
For example, let's say you want to set up two block lists. One of them is for social media and the other is for other distracting sites. First you want to rename the default block list from `default` to `distractions`.

```
$ sudo hblock rename default distractions
Renamed default to distractions.
```

And now you want to add some distracting websites to it.

```
$ sudo hblock add distractions youtube.com reddit.com memory-alpha.fandom.com
Added 3 domains to distractions.
```

And you also want to make the social media block list. We'll call it `social`.

```
$ sudo hblock new social facebook.com twitter.com discordapp.com discord.com
Created social with 4 domains in it.
```

Now you want to see the block lists you've made.

```
$ sudo hblock everything
Domains in distractions [Disabled]:
 - youtube.com
 - reddit.com
 - memory-alpha.fandom.com
Domains in social [Disabled]:
 - twitter.com
 - discord.com
 - discordapp.com
 - facebook.com
 ```

 As you can see, both lists are marked as `[Disabled]`. Now let's turn them on.

 ```
 $ sudo hblock enable
 All 2 block lists enabled.
 ```

 Now restart your web browser. You shouldn't be able to access any of the specified websites! If you still can, try clearing your DNS cache. There's lots of guides on how to do this. You can also check to see that the block lists are enabled.

 ```
 $ sudo hblock active
 Block lists:
 - distractions............................Enabled
 - social..................................Enabled
 ```
