class topFivePost:
    title: str
    description: str
    topFive: list[str]

    def __init__(self, title: str, description: str, topFive: list[str]):
        self.title = title
        self.description = description
        self.topFive = topFive