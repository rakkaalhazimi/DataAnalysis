"""
This is my simple project to scrap anime names into a list and embed its url links.
You can double-click the anime name to redirect your web browser to its url.
How this program work:
1. First it create list-box GUI for anime names container
2. Then, parse html from specific website (not stable)
3. Html parser produce two result: anime names and its urls and pass it to the GUI

Any suggestion please consider email to rakkakeren@gmail.com, cc: project name
"""

from tkinter import *
import requests, bs4
import webbrowser


class AnimeListbox(Frame):
    """Set up list-box GUI that contains anime names"""
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
    """Parse html on website (website dependent)"""
    url = 'https://otakudesu.org/'
    link = requests.get(url)
    soup = bs4.BeautifulSoup(link.content, 'html.parser')

    animeminer = soup.find_all('h2', {'class':'jdlflm'})
    animelist = []
    for anime in animeminer:
        animelist.append(anime.get_text())

    urlminer = soup.find_all('a')
    urlist = []
    for url in urlminer:
        x = url.get('href')
        urlist.append(x)

    return animelist[:10], urlist[12:22]

if __name__ == '__main__':
    win = Tk()
    win.title('List of On-going Anime Schedule in 2020')
    Label(win, text='Source: Otakudesu.org').pack()
    animelist, urlist = htmlParser()
    AnimeListbox(animelist, urlist, parent=win).mainloop()
