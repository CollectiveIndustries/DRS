from lib import com



class TextMenu(object):
    """Defines a Text Menu Object"""

    _menuformatstring_ = "[{}] {} - {}"
    _items_ = {}

    def __init__(self,_items_=None):
        if _items_ is None:
            self._items_ = {}
        else:
            self._items_ = _items_

    def Confirm(prompt, option):
        """Confirm dialog"""
        confirm = "{}{}{} \"{}\" Are you sure (y/n)?"
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
    
    def Print(self):
        """Print Multichoice menu"""
        for option, text in self._items_.items():
            if option != "-1":
                print(self._menuformatstring_.format(option,text[0],text[1]))
            else:
                print(text[0])