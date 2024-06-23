class Bot(object):
    def __init__(self, name: str = "bot") -> None:
        """
        Init the bot.
        Make sure to pass vals from config class.
        """
        self.name: str = name

    def run(self) -> None:
        """
        Bot mainloop.
        """
        print(f"Hi! I am {self.name}")
        # while True:
        #    ...
    
    def __str__(self) -> str:
        """
        String Representation
        """
        string: str = "{\n"
        for k, v in self.__dict__.items():
              string += f"\t{k}: {v}\n"

        string += "}"

        return string

