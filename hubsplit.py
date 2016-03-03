#!/usr/bin/env python

def main(infile):
    print "analyzing %s"%infile
    print "-"*80
    f = file(infile,"rb")
    rawdata = f.read()
    print "filesize %i bytes"%len(rawdata)
    f.close()

    # ok so we look for 1x0B "Sample Bankbanknk" 13x00

    idstring = "\x0B"+"Sample Bankbanknk"+("\x00"*13)

    poss_found = []
    pos_found = -1
    while True:
        pos_found = rawdata.find(idstring,pos_found+1)
        if pos_found == -1:
            poss_found.append(len(rawdata))
            break
        poss_found.append(pos_found)
        
        print poss_found
        
    startnumber = 30

    # write out files
    for i in range(0,len(poss_found)-1):
        start, end = poss_found[i],poss_found[i+1]
        print "saving part %i from %i to %i"%(i,start,end)

        out_file = file("%02i_user_%02i.pcm"%(i+startnumber,i+1),"wb")
        out_file.write(rawdata[start:end])
        out_file.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        for entry in sys.argv[1:]:
            main(entry)
    else:
        print "this.py infile.hh"



