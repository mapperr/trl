import attr


@attr.s(auto_attribs=True)
class TConfig:
    selected_board_filepath: str
