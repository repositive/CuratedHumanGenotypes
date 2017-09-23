#!/usr/bin/env python

import os, sys, argparse, urllib2

maxNumTries = 3

#------------------------------------------------------------------------------

def processArgs():

    parser = argparse.ArgumentParser(description = 'download 23andMe')
    parser.add_argument('--urlFile', dest = 'urlFilePath')
    parser.add_argument('--downloadBaseDir', dest = 'downloadBaseDirPath')
    parser.add_argument('--numToSkip', dest = 'numToSkip')
    args = parser.parse_args()

    return args

#------------------------------------------------------------------------------

def download23AndMe(args):

    urlFile = open(args.urlFilePath)

    numLeftToSkip = 0 if (args.numToSkip is None) else int(args.numToSkip)
    
    for urlLine in urlFile:
        urlLine = urlLine.strip()

        if ((urlLine == '') or (urlLine[0] == '#')):
            continue

        if (numLeftToSkip > 0):
            print 'SKIPPING ' + urlLine
            numLeftToSkip = numLeftToSkip - 1
            continue

        (uniqId, url) = urlLine.split(' ')
        (shortName, externalId) = uniqId.split(':')
        print '%s %s : %s' % (shortName, externalId, url)

        cleanUrl = url

        if (cleanUrl[-1] == '/'):
            cleanUrl = cleanUrl[:-1]
            
        urlParts = cleanUrl.split('/')
        fileName = urlParts[-1]
        print 'fileName %s' % fileName
        
        sourceBaseDirPath = os.path.join(args.downloadBaseDirPath, shortName)
        
        if (not os.path.exists(sourceBaseDirPath)):
            os.makedirs(sourceBaseDirPath)

        datasetDirPath = os.path.join(sourceBaseDirPath, externalId)
            
        if (not os.path.exists(datasetDirPath)):
            os.makedirs(datasetDirPath)

        tryInd = 0

        while (tryInd < maxNumTries):
            try:
                response = urllib2.urlopen(url, timeout = 10)
                content = response.read()
                outFilePath = os.path.join(datasetDirPath, fileName)

                print 'Writing %s' % outFilePath

                outFile = open(outFilePath, 'w')
                outFile.write(content)
                outFile.close()
                break
            except urllib2.URLError as err:
                tryInd += 1
                print type(err)
            
        # raise Exception('DEBUG Early exit')
    
#------------------------------------------------------------------------------

if (__name__ == '__main__'):
    args = processArgs()

    download23AndMe(args)
    
#------------------------------------------------------------------------------
