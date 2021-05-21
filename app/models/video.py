class Video():
    
    def __init__(self):
        self.id = 0
        self.title = ""
        self.description = ""
        self.published_at = ""
        self.thumbnail_url = ""

    def __init__(self, id, title, description, published_at, thumbnail_url):
        self.id = id
        self.title = title
        self.description = description
        self.published_at = published_at
        self.thumbnail_url = thumbnail_url
