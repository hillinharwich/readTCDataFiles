#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 16 21:19:18 2017

@author: stephen-hill9
"""

import matplotlib.pyplot as plt
import struct
#import numpy as np

#def class Peak:
#    __init__(self, )


def positionInFile(file):
    return file.tell()

def readPnwString(file):
    """
        readPnwString reads in a string stored in RAW or RST files
        Recieves: an open file object
        Returns: string
        
        Strings are stored in RAW and RST files by starting with an Int32 containing the length of the string
        The function reads this, and then adds further bytes so that the length is divisible by 4
        The function then reads in each character and adds it to the string, ignoring the padding bytes
    """
    thisString = ""
    bits = file.read(4)
    stringlength = int.from_bytes(bits, byteorder='big')
    while stringlength % 4 != 0:
        stringlength += 1
    for chrcounter in range(stringlength):
        thisChr = chr(int.from_bytes(file.read(1), byteorder='big'))
        if thisChr != "" and thisChr != "\x00":
            thisString = thisString + thisChr
    return thisString


def readPnwDouble(x):
    """
        readPnwString reads in a double stored in RAW or RST files
        Recieves: an open file object
        Returns: double
        
        double values are encoded with the following byte order in TotalChrom files: 32107654
    """
    return round(struct.unpack('>d', x[4:] + x[:4])[0], 2)


def readUserData(file, length):
    thisString = ""
    for chrcounter in range(length):
        thisChr = chr(int.from_bytes(file.read(1), byteorder='big'))
        if thisChr != "" and thisChr != "\x00":
            thisString = thisString + thisChr
    return thisString


def readPnwDate(file):
    #file.read(2)
    dateDict = {}
    dateDict["ucttime"] = int.from_bytes(file.read(4), byteorder='big')

    file.read(8)
    
    return dateDict
    
def readFileHeader(file):
    fileheader = {}
    fileheader["signature"] = int.from_bytes(file.read(4), byteorder='big')
    fileheader["tcobjecttype"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    fileheader["filerevisionnumber"] = int.from_bytes(file.read(4), byteorder='big')
    fileheader["technique"] = int.from_bytes(file.read(4), byteorder='big')
    fileheader["auditlog"] = bool.from_bytes(file.read(4), byteorder='big')
    fileheader["esigenabled"] = bool.from_bytes(file.read(4), byteorder='big')
    fileheader["auditoffset"] = int.from_bytes(file.read(4), byteorder='big')
    fileheader["checksum"] = readPnwString(file)
    fileheader["hdrchecksum"] = readPnwString(file)
    return fileheader

def readDataHeader(file):
    dataheader = {}
    dataheader["author"] = readPnwString(file)
    dataheader["authorhost"] = readPnwString(file)
    dataheader["datecreated"] = readPnwDate(file)
    dataheader["editor"] = readPnwString(file)
    dataheader["editorhost"] = readPnwString(file)
    dataheader["lasteditdate"] = readPnwDate(file)
    dataheader["siteid"] = readPnwString(file)
    dataheader["numberofedits"] = int.from_bytes(file.read(4), byteorder='big')
    dataheader["editflags"] = int.from_bytes(file.read(4), byteorder='big')
    dataheader["description"] = readPnwString(file)
    return dataheader

def readAdHeader(file):
    adheaderdict = {}
    adheaderdict["instnumber"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["startdatetime"] = readPnwDate(file)
    adheaderdict["channelnumber"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["operatorinitials"] = readPnwString(file)
    adheaderdict["filepath"] = readPnwString(file)
    adheaderdict["sequenceentry"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["autosampler"] = readPnwString(file)
    adheaderdict["rack"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["vial"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["runtime"] = readPnwDouble(file.read(8))
    adheaderdict["datamax"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["datamin"] = int.from_bytes(file.read(4), byteorder='big')
    adheaderdict["interfaceserial"] = readPnwString(file)
    adheaderdict["dataconvfactor"] = readPnwDouble(file.read(8))
    adheaderdict["dataoffset"] = readPnwDouble(file.read(8))
    adheaderdict["numberdatapoints"] = int.from_bytes(file.read(4), byteorder='big')
    return adheaderdict

def readSeqDescription(file):
    seqdescription = {}
    file.read(8)
    seqdescription["injsite"] = readPnwString(file)
    seqdescription["racknumber"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["vialnumber"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["replicatenumber"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["studyname"] = readPnwString(file)
    seqdescription["samplename"] = readPnwString(file)
    seqdescription["samplenumber"] = readPnwString(file)
    seqdescription["rawfilename"] = readPnwString(file)
    seqdescription["rstfilename"] = readPnwString(file)
    seqdescription["modifiedrawfilename"] = readPnwString(file)
    seqdescription["baselinefilename"] = readPnwString(file)
    seqdescription["instrumentmethod"] = readPnwString(file)
    seqdescription["processmethod"] = readPnwString(file)
    seqdescription["samplemethod"] = readPnwString(file)
    seqdescription["reportformat"] = readPnwString(file)
    seqdescription["printer"] = readPnwString(file)
    seqdescription["plotter"] = readPnwString(file)
    seqdescription["sampleamount"] = readPnwDouble(file.read(8))
    seqdescription["istdamount"] = readPnwDouble(file.read(8))
    seqdescription["volume"] = readPnwDouble(file.read(8))
    seqdescription["dilutionfator"] = readPnwDouble(file.read(8))
    seqdescription["multiplier"] = readPnwDouble(file.read(8))
    seqdescription["divisor"] = readPnwDouble(file.read(8))
    seqdescription["addend"] = readPnwDouble(file.read(8))
    seqdescription["normalizationfactor"] = readPnwDouble(file.read(8))
    seqdescription["calibratonreport"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["calibrationlevel"] = readPnwString(file)
    seqdescription["updaterettimes"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["sampleid"] = readPnwString(file)
    seqdescription["taskid"] = readPnwString(file)
    seqdescription["seqentrytype"] = int.from_bytes(file.read(4), byteorder='big', signed=True)
    seqdescription["programname"] = readPnwString(file)
    seqdescription["programpath"] = readPnwString(file)
    seqdescription["commandline"] = readPnwString(file)
    seqdescription["userdata1"] = readUserData(file, 44)
    return seqdescription
    

def readRawDataHeader(file):
    rawDataHeaderDict = {}
    rawDataHeaderDict["dataheader"] = readDataHeader(file)
    rawDataHeaderDict["filecompflag"] = int.from_bytes(file.read(4), byteorder='big')
    rawDataHeaderDict["runlog"] = readPnwString(file)
    return rawDataHeaderDict


def readResultHeader(file):
    resultFileHeader = {}
    resultFileHeader["dataheader"] = readDataHeader(file)
    resultFileHeader["rawfilename"] = readPnwString(file)
    resultFileHeader["totalpeakarea"] = readPnwDouble(file.read(8))
    resultFileHeader["totalpeakheight"] = readPnwDouble(file.read(8))
    resultFileHeader["maxpeakarea"] = readPnwDouble(file.read(8))
    resultFileHeader["maxPeakHeight"] = readPnwDouble(file.read(8))
    resultFileHeader["complistflag"] = bool.from_bytes(file.read(4), byteorder='big')
    resultFileHeader["syssuitabilitymthd"] = readPnwString(file)
    resultFileHeader["limsannotation"] = readPnwString(file)
    return resultFileHeader

def readGroupDescriptors(file):
    file.read(4)
    groupDescriptorList = []
    bits = file.read(4)
    numberofgroupdescriptors = int.from_bytes(bits, byteorder='big')
    for counter in range(numberofgroupdescriptors):
        groupDescriptor = {}
        groupDescriptor["name"] = readPnwString(file)
        groupDescriptor["type"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["complete"] = bool.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["rettime"] = readPnwDouble(file.read(8))
        groupDescriptor["area"] = readPnwDouble(file.read(8))
        groupDescriptor["height"] = readPnwDouble(file.read(8))
        groupDescriptor["maxarea"] = readPnwDouble(file.read(8))
        groupDescriptor["maxheight"] = readPnwDouble(file.read(8))
        groupDescriptor["retentionrefindex"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["istdindex"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["componentindex"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["areapercent"] = readPnwDouble(file.read(8))
        groupDescriptor["rawamount"] = readPnwDouble(file.read(8))
        groupDescriptor["result"] = readPnwDouble(file.read(8))
        groupDescriptor["istdresponseratio"] = readPnwDouble(file.read(8))
        groupDescriptor["istdamountratio"] = readPnwDouble(file.read(8))
        groupDescriptor["voltagerange"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["calrange"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptor["numpeaks"] = int.from_bytes(file.read(4), byteorder='big')
        groupDescriptorList.append(groupDescriptor)
    return groupDescriptorList

def readPeakDescriptors(file, numberofpeakdescriptors):
    peakDescriptorList = []
    for counter in range(numberofpeakdescriptors):
        peakDescriptor = {}
        peakDescriptor["startindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["middleindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["endindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["startvalue"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["middlevalue"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["endvalue"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["starttime"] = readPnwDouble(file.read(8))
        peakDescriptor["rettime"] = readPnwDouble(file.read(8))
        peakDescriptor["endtime"] = readPnwDouble(file.read(8))
        peakDescriptor["area"] = readPnwDouble(file.read(8))
        peakDescriptor["height"] = readPnwDouble(file.read(8))
        peakDescriptor["overlap"] = bool.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["baselinecode"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["front"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["crest"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["back"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["resultchar"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["char"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["innamedgroup"] = bool.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["intimmedgroup"] = bool.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["expskimoffset"] = readPnwDouble(file.read(8))
        peakDescriptor["expdecay"] = readPnwDouble(file.read(8))
        peakDescriptor["name"] = readPnwString(file)
        peakDescriptor["refpeakindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["istdpeakindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["componentindex"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["deltartpercent"] = readPnwDouble(file.read(8))
        peakDescriptor["areapercent"] = readPnwDouble(file.read(8))
        peakDescriptor["rawamount"] = readPnwDouble(file.read(8))
        peakDescriptor["result"] = readPnwDouble(file.read(8))
        peakDescriptor["istdresponseratio"] = readPnwDouble(file.read(8))
        peakDescriptor["istdamountratio"] = readPnwDouble(file.read(8))
        peakDescriptor["voltagerangeflag"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["calibrationrangeflag"] = int.from_bytes(file.read(4), byteorder='big')
        peakDescriptor["relretentiontime"] = readPnwDouble(file.read(8))
        file.read(40)
        peakDescriptorList.append(peakDescriptor)
    return peakDescriptorList

def readRawData(file, numberofpoints):
    #file.seek(814)
    numberlist = []
    counter = 0
    while counter < (numberofpoints):
    #while counter < (100000):
        numberbytes = file.read(4)
        integer = int.from_bytes(numberbytes, byteorder='big')
        counter += 1
        numberlist.append(integer)
    return numberlist


def readRAWFile(file):
    rawFileDict = {}
    rawFileDict["fileheader"] = readFileHeader(file)
    rawFileDict["dataheader"] = readRawDataHeader(file)
    rawFileDict["adheader"] = readAdHeader(file)
    rawFileDict["seqdesc"] = readSeqDescription(file)
    rawFileDict["datapoints"] = readRawData(file, rawFileDict["adheader"]["numberdatapoints"])
    #rawFileDict["datapoints"] = readRawData(file)
    return rawFileDict

def readRSTFile(file):
    rstFileDict = {}
    rstFileDict["fileheader"] = readFileHeader(file)
    rstFileDict["resultheader"] = readResultHeader(file)
    rstFileDict["adheader"] = readAdHeader(file)
    rstFileDict["seqdesc"] = readSeqDescription(file)
    rstFileDict["groupdescriptors"] = readGroupDescriptors(file)
    numberofpeakdescriptors = int.from_bytes(file.read(4), byteorder='big')
    rstFileDict["numberofpeaks"] = numberofpeakdescriptors
    rstFileDict["peakdescriptors"] = readPeakDescriptors(file, numberofpeakdescriptors)
    return rstFileDict
