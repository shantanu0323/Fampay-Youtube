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

    def show_info(self):
        print("*" * 40)
        print(f"{self.id} -> {self.title}")
        print(f"{(self.description)[:100]}")
        print(f"{(self.thumbnail_url)}")
        print(f"{self.published_at}")