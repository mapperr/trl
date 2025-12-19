# trl

A dumb trello cli with shortcuts .


## Setup

Get the repo and run `uv venv` in it .

You don't have `uv` installed?

([Here](https://docs.astral.sh/uv/getting-started/installation/)
is how you can get it)

Authenticate yourself by putting these variables in you environment:

    export TRELLO_API_KEY=<api_key>
    export TRELLO_TOKEN=<your_token>

Go get them on [trello](https://trello.com/app-key)!

Now link the `trl` script in your `PATH`.
It's a bash script that wraps the underneath python call.
Feel free to hack it or use something else.

Aaaand, that's it, you are good to go.


## Usage

As for now you can do basic stuff.

Here is the usage (check `trl -h` too):

    trl o
        opens trello home in your browser
        or it opens the currently selected board in browser

    trl b [<board_shortcut>]
        shows the boards you can access
        with board_shortcut you can select the board you want to work with

    trl l [<list_shortcut> [<list_shortcut>]]
        shows lists and cards in the board you have currently selected
        with list_shortcut you can show cards of a single list

    trl l n <list_name> [<after_list_shortcut>]
        create a new list on the board; position after the specified list

    trl ll
        shows only the board's lists

    trl lb
        shows the board's labels

    trl bm
        shows the board's members

    trl c <card_shortcut> [o | m <list_shortcut> | e | co [<comment>]]
        shows the card infos
        with o it opens the card shortUrl with your default browser
        with m and a target list you can move the card to that list
        with e you can edit the card title and description in your $EDITOR
        with co you can post a comment to the card (if omitted, opens your $EDITOR)

    trl c n <list_shortcut>
        pops your $EDITOR to create a new card in the list specified by list_shortcut

    trl api <method_or_path> [<path>]
        make a direct api call adding auth params automatically (for debugging/hacking purpose)
        method can be get/post/put/delete (default: get)
        Cf. [REST API reference](https://developer.atlassian.com/cloud/trello/rest)

## Shortcuts

Shortcuts are derived from:

- boards names and short urls
- cards names and short urls
- lists names and ids (lists does not have short urls)

So to move the card *Architecture design* to the list *Done*
you get something like this:

    trl c arch m done


## Notes

I know, It's nothing fancy, I just started because I have to use Trello
and I wanted to check some stuff directly from the terminal, and eventually
edit them or open them in the browser.

