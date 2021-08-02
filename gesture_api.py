import keyboard
from win32gui import GetWindowText, GetForegroundWindow


def check_if_teams_in_fg() -> bool:
    curr = GetWindowText(GetForegroundWindow())
    try:
        # for Microsoft teams, when youre in call, Window Text will be something like
        # `Name of the meeting` | Microsoft Teams
        curr_arr = curr.split('|')
        appName = curr_arr[-1]
        if appName.strip() == "Microsoft Teams":
            return True
        else:
            return False
    except:
        return False


def toggle_hand_raise_in_teams() -> bool:
    if check_if_teams_in_fg():
        keyboard.press_and_release('ctrl+shift+k')


def toggle_mute_in_teams() -> bool:
    if check_if_teams_in_fg():
        keyboard.press_and_release('ctrl+shift+m')
