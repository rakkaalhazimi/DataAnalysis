from tkinter import *
import requests, bs4
import webbrowser

#webbrowser.open('https://anoboy.video/', new=1)

class AnimeListbox(Frame):
    def __init__(self, animelist, urllist=None, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.urlist = urllist
        self.makeListBox(animelist)

    def makeListBox(self, animelist):
        sbar = Scrollbar(self)
        list = Listbox(self, width=100, relief=SUNKEN)
        sbar.config(command=list.yview)
        list.config(yscrollcommand=sbar.set)
        sbar.pack(side=RIGHT, fill=Y)
        list.pack(side=LEFT, expand=YES, fill=BOTH)

        for index, anime in enumerate(animelist):
            list.insert(index, anime)
        list.config(selectmode=SINGLE, setgrid=1)
        list.bind('<Double-1>', self.selectAnime)
        self.animelist = list

    def selectAnime(self, event):
        index = self.animelist.curselection() # double click
        index = index[0]
        self.openBrowser(self.urlist[index])

    def openBrowser(self, url):
        webbrowser.open(url, new=1)


def htmlParser():
    url = 'https://anoboy.video'
    link = requests.get(url)
    soup = bs4.BeautifulSoup(link.content, 'html.parser')

    animeminer = soup.find_all('div', {'class':'amvj'})
    animelist = []
    for anime in animeminer:
        animelist.append(anime.get_text())

    urlminer = soup.find_all('a', {'title':[animelist]})
    urlist = []
    for url in urlminer:
        x = url.get('href')
        urlist.append(x)

    return animelist, urlist

if __name__ == '__main__':
    win = Tk()
    win.title('Anime List Schedule 2020')
    Label(win, text='Source: Anoboy.Video').pack()
    animelist, urlist = htmlParser()
    AnimeListbox(animelist, urlist, parent=win).mainloop()