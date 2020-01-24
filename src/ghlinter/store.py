from ghlinter import config_manager

#### GLOBAL User Variables
## available user variables when creating commands and responses
##
## author:      author of the given issue or pull request
## number:      number of the given issue or pull request
## assignees:   list of users assigned to given issue or pull request
## unassignee:  user unassigned from given issue or pull request (only available on unassigned events)
## bot_name:    name of the bot (ghlint-bot)
class Store:
    def __init__(self):
        self.author = ''
        self.number = 0
        self.assignees = []
        self.unassignee = ''

    def format_string(self, string: str) -> str:
        return string.format(
        author = self.author, 
        number=self.number, 
        assignees=self.assignees, 
        unassignee=self.unassignee, 
        bot_name=config_manager.bot_name()
    )

store: Store = Store()