
import http.client
import time
import sys

_sizeChunk = 512
_connection = None

def GetUrlFromCommandString():
    url = sys.argv[1]
    return url

def GetSiteName(url):
    siteName = url.split('/')[2]
    return siteName

def GetAbsolutePath(url):
    absolutePath = '/'.join(url.split('/')[3:])
    absolutePath = '/' + absolutePath
    return absolutePath

def GetDocumentName(url):
    documentName = url.split('/')[-1]
    return documentName

def GetResponseFromUrl(siteName, absolutePath):
    global _connection
    _connection = http.client.HTTPSConnection(siteName)
    _connection.request('GET', absolutePath)
    response = _connection.getresponse()

    return response

def DownloadFile(responseFromUrl, fileForSave):
    sumReceivedBytes = 0

    chunk = responseFromUrl.read(_sizeChunk)
    realSizeChunk = len(chunk)

    while realSizeChunk > 0:
        sumReceivedBytes += realSizeChunk
        print('Скачено байтов - ', realSizeChunk)
        fileForSave.write(chunk)
        time.sleep(1)

        chunk = responseFromUrl.read(_sizeChunk)
        realSizeChunk = len(chunk)
    
    print('\n////////////////////////////////\n')
    print('Всего скачено байтов - ', sumReceivedBytes)


if __name__ == '__main__':
    url = GetUrlFromCommandString()

    siteName = GetSiteName(url)
    absolutePath = GetAbsolutePath(url)
    documentName = GetDocumentName(url)
    fileForSave = open(documentName, 'wb')

    responseFromUrl = GetResponseFromUrl(siteName, absolutePath)

    DownloadFile(responseFromUrl, fileForSave)

    fileForSave.close()
    _connection.close()