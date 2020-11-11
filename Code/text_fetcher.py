import wikipedia as wk


class TextFetcher:
    def __init__(self, title):
        self.text = wk.page(title).summary

    def getText(self):
        return self.text

print(TextFetcher("Oxygen").getText())