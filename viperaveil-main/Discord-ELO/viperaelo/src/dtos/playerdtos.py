from datetime import datetime
import json
class PlayerDto:
    def __init__(self, name, id_user):
        self.userId = id_user
        self.name = name
        self.wins = 0
        self.losses = 0
        self.matchesplayed = 0
        self.winloassratio = 0
        self.elo = 1000
        self.highestelo = 0
        self.longestwinstreak = 0
        self.longestlossstreak = 0
        self.currentwinstreak = 0
        self.currentlossstreak = 0
        self.SelectedModes = []

        import json

class PlayerDtoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PlayerDto):
            return {
                "userId": obj.userId,
                "name": obj.name,
                "wins": obj.wins,
                "losses": obj.losses,
                "matchesplayed": obj.matchesplayed,
                "winloassratio": obj.winloassratio,
                "elo": obj.elo,
                "highestelo": obj.highestelo,
                "longestwinstreak": obj.longestwinstreak,
                "longestlossstreak": obj.longestlossstreak,
                "currentwinstreak": obj.currentwinstreak,
                "currentlossstreak": obj.currentlossstreak,
                "SelectedModes": obj.SelectedModes
            }
        return super().default(obj)
