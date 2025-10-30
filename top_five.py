class topFivePost:
    title: str
    description: str
    topFive: list[str]

    def __init__(self, title: str, description: str, topFive: list[str]):
        self.title = title
        self.description = description
        self.topFive = topFive

    def displayPost():
        print(f"{title}")
        print(f"{description}")
        print(f"My top 5 are: {topFive}")
        for i in range(5):
            print(f"# {i+1}: {topFive[i]} ")