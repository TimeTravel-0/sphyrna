#!/usr/bin/env python

def main(infile):
    print "analyzing %s"%infile
    print "-"*80
    f = file(infile,"rb")
    rawdata = f.read()
    print "filesize %i bytes"%len(rawdata)
    f.close()


    # now pick it apart
    credit_text_length = ord(rawdata[0])
    credit_text=rawdata[1:(credit_text_length)]
    print credit_text

    notes = rawdata[credit_text_length+1+48:]

    configuration = rawdata[-33:]

    content = rawdata[credit_text_length+1:]



    total = ord(configuration[0])
    print "total=%i"%total


    channels = []
    for i in range(0,6):
        length = 8 * 16

        startpos = i*(length)
        channels.append( notes[startpos:startpos+length] )

    for channel in channels:
        l = ""
        for note in channel:
            if ord(note)==100:
                l+="#"
            else:
                l+="-"
        print l

    instruments = configuration[1:7]
    volumes = configuration[8:14]
    reverses = configuration[14:20]
    distortions = configuration[20:26]
    for i in range(0,6):
        print "inst %i voice %i volume %i rev %i dis %i"%(i+1,ord(instruments[i]),ord(volumes[i]),ord(reverses[i]),ord(distortions[i]))



    # ON/OFF???
    # TEMPO???
    # SHUFFLE???
    # DISTORTION???
    # FEEDBACK???
    # OVERALL VOLUME???


    tval = ""
    for i in range(0,len(rawdata)):
        tval+="%03i "%ord(rawdata[i])
        if len(tval)>4*15:
            print tval
            tval=""
        #print ord(content[i])

#    print content

#    print ord(rawdata[0])

#    print int(rawdata[1])



if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        for entry in sys.argv[1:]:
            main(entry)
    else:
        print "this.py infile.hh"


