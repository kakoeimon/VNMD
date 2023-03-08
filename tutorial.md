# VNMD TUTORIAL

Let's create a vary simple VNMD game that will explore all the VNMD functionality.

Open the file novel\script\main.scr

This is your main script it is the script that VNMD requires and the first script your game will run.

Delete everything and write.

    bgload black
this will load and display the black.jpg located in novel\background

novel\background is the place where you will get all your backgrounds.

black.jpg is special, because it contains the size of the images and it is going to be used by the python scripts to know the scale of the foregrounds. The backgrounds will be scaled to fit the size defined in the novel.ini but for the foregrounds we need another way and this way is the size of the black.jpg

Now write:

    text Hello VNMD.
this is just a text that will be displayed on scree.

Try it out.
Type in the terminal

    make_all.bat

This batch file will run the the python scripts in the right order to build the game.
But you will have to edit it so it contains the paths to the emulator etc.
For example
change line

    c:\RetroArch-Win64\retroarch.exe -L c:\RetroArch-Win64\cores\blastem_libretro.dll out\rom.bin

with the paths and the commands of the emulator of your choice to run the out\rom.bin

If everything goes as expected then the emulator will run and you will see a black screen at the top and at the bottom text writing

        Hello VNMD

Now create another script named inventory.scr in the directory novel\script

write there :

    text You have nothing.

return to the main file and write at the bottom.

    jump inventory.scr



This will make the game to jump to the inventory script.

You can also just write

    jump inventory

VNMD even thought it started as a VNDS clone, it contains extra functionality that it is not VNDS compatible.

In this case it does not requires the file extensions.

Run make_all and see that it jumps to the inventory file as you will get after the Hello VNMD the text You have nothing.

Let's make it a choice to jump to the inventory.

Delete everything in the main script and write.

    bgload black 60
    text It was too dark to see anything.
    label make_a_choice
    choice Look around.|Inventory
    if selected == 1:
        text He tried to see, but darness prevailed.
        goto make_a_choice
    fi
    if selected == 2:
        jump inventory
        text So you have nothing.
    fi

make_all

Many new things were introduced here but let's examine them one by one.

<b>label</b> is just that a label inside the script. The purpose of a label is to mark a position inside the script and use the label to jump there with the goto command or the jump command.

<b>choice</b> is the way to create options in the game. The vertical column <b>|</b> separates the options from each other.

<b>if</b> is used to make comparisons and to create roots and actions in the game. In this example it checks if the variable selected is equal to 1.
selected is var that exists in every VNMD game and is the var that changes when choices are made. So 1 is for the first choice and 2 is for the second one.

<b>fi</b> is where the if closes. Every if must contains a fi afterwards to know where the if branch is ending. You can have nested ifs. Also the : is ignored when it is at the end of the line. This is a VNMD only future cause it makes branching much easier as the vscode reacts like it is a python script and you can have easy tabbing this way.

<b>goto</b> is used to jump to a label of the file. So when this line is reached the game will go to the label line and continue from there. In this case we will have to make the choice again.


make_all and play the game.
You will see that if you go to the inventory, that even without a jump command the game returns to the main. This is cause if a script comes to an end without a jump then the game resets. We can change that with a jump command.

Go to the inventory.scr and write at the bottom

    jump main make_a_choice

This will make the script to jump to the main.scr but to the label make_a_choice. So if you run this you will not see the text It was too dark to see anything. cause the game will not reset but will return to the main and to the label specified.

We do not want to make the inventory to return to the main every time so we can change this by using string vars.
String vars only function with labels and script files.
so at the top of the main write

    setvar retfile = "main.scr"
    setvar retlabel = make_a_choice

script vars like retfile in this case must contain a script file inside "" otherwise it will not work.
labels can be putted inside a var but only the label in the same script.

Now go to the inventory file and change the jump line to

    jump $retfile $retlabel

this way the jump will jump to the file and label that the variables contain.

This way you can return to any file from the inventory.

make_all and see that it is like before.

If you use this for an inventory soon you will realize that setting retfile and relabel and the labels is quite boring.
For this reason the external function ret_jump_store can be use.

In the main.scr write above the jump inventory this:

    ret_jump_store

This is an external function that can be found in scr\novel_external_functions.c
This will store the script file in retfile var and the position of the novel plus the size of the jump command to the retlabel. This means that when the jump in the inventory runs it will return immediately after the jump in the main.

make_all and test.

Now at the bottom of main.scr wite

    setimg character 128 0

this will display the character.png located in the novel\foreground and it will have x = 180 and y = 0

Then write

    text Ha... you have nothing!
    bgload black
    text and it is dark again.


This will display the text and then display the black.png again and the other text.

If you run this you will see that when the black.png is loaded and displayed again the character will disappear.

This is cause this is the way VNDS functions.
Every background removes every foreground.

But because this is error prone VNMD have another external function for this.
Replace bgload black with fr_clear

This will just reload the background for you.

I think that this along with the script_format.txt covers the functionality of the VNMD but there is something else that I believe can be very helpful.

## Create string vars for your locations.

If you are going to make a visual novel like an choose you own adventure game then you are all ready good to go.

But if you want to create something like a JAdventure (like Snatchers) then you will need and a little bit of a trick to make your life easier.

In JAdventures many times you move from one place to another and as the progress goes on several events are happening in those places.

One way to do this is by just using the if branching but soon becomes clear that writing a game like this is quite more difficult from what it seems.

So one way of not getting to many nested ifs to accomplish this is by setting string variables that contain the the files for each location.

For example let's say we have a place that it is supposed to be the office.
At the main.scr write something like this.

    setvar office_file = "office.scr"

Put inside the office.scr what ever you think is the default office location.

Then when you need an event to be placed in there just change the office_file with another file that contains the event.

Then use the jump when ever you want to go to the office like this

jump $office_file

You can also create a movement.scr and have the basic traveling around organized in there.

For example:

    label corridor
    choice Enter the Office|Go outside
    if selected == 1:
        jump $office_file
    fi
    if selected == 2:
        jump $outside_file
    fi

This way when you are writing the corridor file and you want the movement choices for the corridor to be displayed you can just write

    jump movement corridor

Simple tricks but helped me a lot when I was making the Mansion of Sadness.

Hope to hear back from you and play your games.
Good luck.
