# trl

A dumb trello cli with shortcuts.


## Setup

Get the repo and run `pipenv install` in it

You don't have pipenv installed? Shame on you.\
([Here](https://pipenv.readthedocs.io/en/latest/install/#pragmatic-installation-of-pipenv)
is how to can get it, but usually is a `pip install --user pipenv`)

Yeah, I know you want a binary, I will package this thing, bear it for now.

Authenticate yourself by putting these variables in you environment:

    export TRELLO_API_KEY=<api_key>
    export TRELLO_TOKEN=<your_token>

Go get them on [trello](https://trello.com/app-key)!

Aaaand, that's it, you are good to go.


## Usage

As for now you can do basic stuff.

Here is the usage (check `trl -h` too):

    trl b [<board_shortcut>]
        shows the boards you can access
        with board_shortcut you can select the board you want to work with

    trl l [<list_shortcut>]
        shows lists and cards in the board you have currently selected
        with list_shortcut you can show cards of a single list

    trl ll
        shows only the board's lists

    trl c <card_shortcut> [o | m <list_shortcut> | e]
        shows the card infos
        with o it opens the card shortUrl with your default browser
        with m and a target list you can move the card to that list
        with e you can edit the card title and description in your editor

    trl c n <list_shortcut>
        create a new card in the list specified by list_shortcut

    trl g <api_path>
        make a direct api call adding auth params automatically (for debugging/hacking purpose)

## Shortcuts

Shortcuts are derived from boards and cards short urls and from lists ids
(lists does not have short urls) and are as short as possible.

So to move a card to a list you get something like this:

    trl c j0 m e

`j0` is the card shortcut and `e` is the list shortcut

Oh, everything is kept lowercase, holding shift is a pain in the ass.


## Notes

I know, It's nothing fancy, I just started it to check some trello stuff
directly in the terminal, and eventually edit them.

