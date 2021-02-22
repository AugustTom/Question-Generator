import wikipedia as wk
# import pathlib

# TODO add topic checker to make sure it picks one
class TextFetcher:
    def __init__(self, title):
        # p = pathlib.Path('./Texts/{}.txt'.format(title))
        # if p.is_file():
        #     print("File is already present. Reading from the file")
        #     self.text = open(p).read()
        # else:
        self.text = wk.page(title).summary
        # file = open(p, "w")
        # file.write(self.text)
        # file.close()


    def getText(self):
        return self.text

