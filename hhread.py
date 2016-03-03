#!/usr/bin/env python



def main(infile,outfile=False):
    data = readhh(infile)
    if outfile:
        savejs(data,outfile)

def savejs(data,outfile):

    import json

    f = file(outfile,"w")
    f.write(json.dumps(data,sort_keys=True,indent=4))
    f.close()

    return

def readhh(infile):
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


    x_config = []



    total = ord(configuration[0])
    print "total=%i"%total

    x_config.append(total)


    channels = []
    for i in range(0,6):
        length = 8 * 16

        startpos = i*(length)
        channels.append( notes[startpos:startpos+length] )


    x_channels = []
    for channel in channels:
        l = ""
        x_channel = []
        for note in channel:
            x_channel.append(ord(note))

            if ord(note)==100:
                l+="#"
            else:
                l+="-"
        x_channels.append(x_channel)
        print l



    x_instruments = []

    instruments = configuration[1:7]
    volumes = configuration[8:14]
    reverses = configuration[14:20]
    distortions = configuration[20:26]
    for i in range(0,6):
        print "inst %i voice %i volume %i rev %i dis %i"%(i+1,ord(instruments[i]),ord(volumes[i]),ord(reverses[i]),ord(distortions[i]))
        x_instrument = [i+1,ord(instruments[i]),ord(volumes[i]),ord(reverses[i]),ord(distortions[i])]
        x_instruments.append(x_instrument)



    # ON/OFF???
    # TEMPO???
    # SHUFFLE???
    # DISTORTION???
    # FEEDBACK???
    # OVERALL VOLUME???


    # add them to x_config
    x_config.append(125) # BPM / tempo

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



    return [x_config, x_instruments, x_channels]


if __name__ == "__main__":
    import sys
    if len(sys.argv)==2:
        main(sys.argv[1])
    elif len(sys.argv)==3:
        main(sys.argv[1],sys.argv[2])
    else:
        print "this.py infile.hh (outfile.json)"


