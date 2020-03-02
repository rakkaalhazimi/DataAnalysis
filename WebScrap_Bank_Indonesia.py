import bs4, requests

link = "https://www.bi.go.id/id/Default.aspx"

web = requests.get(link)
soup = bs4.BeautifulSoup(web.content, "html.parser")

indikator = []
nilai = []
count = 0

# Scraping the web data
for data in soup.findAll('div', {'class':'bi-rate noindex'}):
    if count == 5:
        break
    name = data.find('div', {'class': 'bi-rate-name noindex'})
    value = data.find('div', {'class': 'bi-rate-value noindex'})
    indikator.append(name.text.strip())
    nilai.append(value.text.strip())
    count += 1

# reformat odd text
nilai[2] = nilai[2][0:10]

# loop through the list
for i in range(len(indikator)):
    print('{} : {}'.format(indikator[i], nilai[i]))

