# trl

A dumb trello cli with shortcuts.


## Setup

Get the repo and run `pipenv install` in it.

Yeah, I know you want a binary, I will package this thing, bear it for now.

Authenticate yourself:

    export TRELLO_API_KEY=<api_key>
    export TRELLO_TOKEN=<your_token>

Go get them on [trello](https://trello.com/app-key) now!

And, that's it, you are good to go.


## Usage

As for now,
the workflow is: select a board, view things, edit cards in your browser.

Here is the usage:

    b [<board_shortcut>]
        shows the boards you can access
        with board_shortcut you can select the board you want to work with

    l [<list_shortcut>]
        shows the board you have currently selected
        with list_shortcut you can show a single list

    c <card_shortcut> [o | m <list_shortcut> | e]
        shows the card infos
        with o it opens the card shortUrl with your default browser
        with m and a target list you can move the card to that list
        with e you can edit the card title and description in your editor

    c n <list_shortcut>
        create a new card in the list specified by list_shortcut

    g <api_path>
        make a direct api call adding auth params automatically (for debugging/hacking purpose)


## Notes

I know, It's nothing fancy, I just started it to check some trello stuff
directly in the terminal, and eventually edit them.

