import wikipedia as wk


def checkTopic(title):
    search = wk.search(title, results=3)
    if len(search) > 0:
        if search[0].lower() == title.lower():
            return 1
        else:
            raise KeyError("Unclear topic, choose one of these:", search)
    elif len(search) == 0:
        raise KeyError("No text was found!")


class TextFetcher:
    def __init__(self, title):
        wk.set_lang("en")
        search = wk.search(title, results=3)
        if len(search) > 0:
            if search[0].lower() == title.lower():
                try:
                    self.text = wk.page(title).summary
                except Exception:
                    raise KeyError("Sorry, an error occurred while fetching text")
            else:
                raise KeyError("Unclear topic, choose one of these:", search)
        elif len(search) == 0:
            raise KeyError("No text was found!")

    def getText(self):
        return self.text

