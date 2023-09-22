class RsiAccount:
    def __init__(self, organization):
        self.organization = organization


class Profile:
    def __init__(
            self,
            badge,
            badgeImage,
            bio,
            display,
            enlisted,
            fluency,
            handle,
            id,
            image,
            page,
            website):
        self.badge = badge,
        self.badgeImage = badgeImage,
        self.bio = bio,
        self.display = display,
        self.enlisted = enlisted,
        self.fluency = fluency,
        self.handle = handle,
        self.id = id,
        self.image = image,
        self.page = page,
        self.website = website


class Page:
    def __init__(self, title, url):
        self.title = title,
        self.url = url


class Organization:
    def __init__(self, image, name, rank, sid, stars):
        self.image = image,
        self.name = name,
        self.rank = rank,
        self.sid = sid,
        self.stars = stars


class User:
    def __init__(self, Id, DiscordHandle, ResiHandle):
        self.Id = Id
        self.DiscordHandle = DiscordHandle
        self.RsiHandle = ResiHandle
