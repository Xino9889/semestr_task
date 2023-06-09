from typing import TypedDict, Union, Optional



class UsersAnswers:
    def __init__(self, LoadDate, Name, ChatId, TotalScore, **kwargs):
        self.LoadDate = LoadDate
        self.Name = Name
        self.ChatId = ChatId
        self.TotalScore = TotalScore
        for key, value in kwargs.items():
            setattr(self, key, value)
