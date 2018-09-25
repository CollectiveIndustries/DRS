from lib import com
from prettytable import PrettyTable


class TextMenu(object):
    """Defines a Text Menu Object"""
    _items_ = {}
    def __init__(self,_items_=None, ColHeaders=[]):
        self._menu_ = PrettyTable()
        self.Headers = ColHeaders
        if _items_ is None:
            self._items_ = {}
            _menu_.field_names = []
        else:
            self._menu_.field_names = ColHeaders
            for option, text in _items_.items():
                self._menu_.add_row([option]+ text)

    def Align(self, header="", alignment="l"):
        """Aligns a menu col
        possible values are l, c, r"""
        self._menu_.align[header] = alignment

    def Confirm(prompt="", option=""):
        """Confirm dialog"""
        confirm = "{}{}{} {} Are you sure (y/n)? "
        answer = input(confirm.format(com.color.WARNING, prompt, com.color.END, option)).lower()
        if answer == "y":
            return True
        else:
            return False

    def GetInputNonEmpty(promt):
        """Refuse empty answers"""
        option = None
        while True:
            option = input("{}{}:{} [ ] ".format(com.color.HEADER,promt, com.color.END))
            if option != "":
                return option
            option = None
            print("{}{} cannot be empty!{}".format(com.color.FAIL,promt,com.color.END))
    
    def GetDefaults(prompt, defval):
        """Gets data from user providing a defualt option"""
        formatstr = "{}{}:{} [ {} ] " # Header color prompt with defualt in [ ]
        response = input(formatstr.format(com.color.HEADER,prompt, com.color.END, defval))
        if response == "":
            return defval
        else:
            return response

    def Print(self):
        """Print Multichoice menu"""
        print(self._menu_)
