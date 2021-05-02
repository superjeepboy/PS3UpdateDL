import os
import xml.etree.ElementTree as etree
import requests
import sys
import warnings
from tqdm import tqdm

#just so requests doesn't bug me for using an insecure connection
warnings.filterwarnings("ignore")

#remove last temp file
if os.path.exists("temp.xml"):
    os.remove("temp.xml")

#template url links to any serial
template = 'https://a0.ww.np.dl.playstation.net/tpl/np/{serial}/{serial}-ver.xml'

#format url to game serial
gameId = str(input("Enter game ID: "))
url = template.format(serial = gameId)

#request xml
print("current link: " + url)
conn = requests.get(url, verify=False)

#write get contents to gameupdatexml.xml
with open('temp.xml', 'wb') as f:
        f.write(conn.content)
        f.close()

#open file up
xml = open('temp.xml', 'r')

#construct element tree of xml file
try:
    tree = etree.parse(xml)
except Exception:
    print("invalid xml, aborting")
    exit()
    
#get the first tag in the xml tree
root = tree.getroot()

#loop through tags until package tag is found, then download that file
for tag in root.findall('./tag/package'):
    #get file data
    downloadUrl = tag.get('url')
    version = tag.get('version')
    shaSum = tag.get('sha1sum')
    print("patch found, downloading")
    print("Version: " + version)
    print("SHA1sum: " + shaSum)
    #open stream to file
    conn2 = requests.get(downloadUrl, verify=False)
    #split URL into link for file
    splitIndex = downloadUrl.rsplit('/')
    #get the last entry in the list for the filename
    fullFileName = splitIndex[len(splitIndex)-1]
    #get size of file
    total_size = int(conn2.headers['content-length'])
    #write contents
    with open(fullFileName, 'wb') as f:
        for data in tqdm(iterable = conn2.iter_content(chunk_size = 1024), total = total_size/1024, unit = 'MB'):
            f.write(conn2.content)
        f.close()
        print("download done! exiting")
