from bs4 import BeautifulSoup
import re
from pprint import pprint

url = '/home/binpngnbn/Downloads/1112.html'
page = open(url)
soup = BeautifulSoup(page.read(), "html.parser")
tables = soup.findAll('table') #get tables


# 1y1s - tables[2]
# 1y2s - tables[3]
# 1yss - tables[4]
# 2y1s - tables[5]
# 2y2s - tables[6]
# 2yss - tables[7]
# 3y1s - tables[8]
# 3y2s - tables[9]
# 3yss - tables[10]
# 4y1s - tables[11]
# 4y2s - tables[12]
# 4yss - tables[13]
# 5y1s - tables[14]
# 5y2s - tables[15]
# 5yss - tables[16]

for x in range(2,int(len(tables))): #run through tables from tables[2]
    table = tables[x]
    trs = table.findAll('tr')       #get table rows

    for y in range(1, int(len(trs))): #run through table rows from rows[1]
        try:
            code = trs[y].findAll('td')[0].contents #get course code
            strcode = ''.join(code)
        except:
            code = 'None'
        try:
            description = trs[y].findAll('td')[3].contents #get course description
            strdesc = ''.join(description)
        except:
            description = 'None'
        try:
            lec_hours = trs[y].findAll('td')[4].contents #get lecture hours
            strlec = ''.join(lec_hours)
        except:
            lec_hours = 'None'
        try:
            lab_hours = trs[y].findAll('td')[5].contents #get lab hours
            strlab = ''.join(lab_hours)
        except:
            lab_hours = 'None'
        
        
        pprint(f'{strcode} - {strdesc} - {strlab} - {strlec}')


# table = tables[2]
# trs = table.findAll('tr')
# pprint(len(trs))
# # pprint(trs)
# try:
#     td = trs[1].findAll('td')[5].contents
# except:
#     td = 'None'
# pprint(td)

