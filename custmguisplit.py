#!/usr/bin/env python

def main(infile):
    samplenames = ["HardBD","909BD","SubBD","JungleBD","BlipBD","Hardcore909BD1","Hardcore909BD2","606Snare","JungleSnare","HardSnare","808Snare","Ac.Snare1","Ac.Snare2","909Snare","909Clap","SnapClap","Rimshot","909OpenHH","909ClosedHH","909PedalHH","Ac.OpenHH","Ac.ClosedHH","909Crash","[HipHop]","[FunkyDrummer]","[Giz1]","[Giz2]","[Jungle1]","[Jungle2]"]
    sampleoffsets = [0,25755+45*2,42778,152147,172433,189280,220591,256136,272189,288859,322199,330314,351923,369210,382882,403080,422660,431128,481314,475846,485636,554698,560784,642017,725632,817185,883336,949310,1011933,1074556]

    f = file(infile,"rb")
    rawdata = f.read()
    print "filesize %i bytes"%len(rawdata)
    f.close()


    # write out files
    for i in range(0,len(sampleoffsets)-1):
        start, end = sampleoffsets[i],sampleoffsets[i+1]
        name = samplenames[i]
    
        if start%2 == 1:
            start+=1
        if end%2 == 1:
            end+=1
        
        print "saving part %i from %i to %i as %s"%(i,start,end,name)

        out_file = file("%02i_%s.pcm"%((i+1,name)),"wb")
        out_file.write(rawdata[start:end])
        out_file.close()



if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        for entry in sys.argv[1:]:
            main(entry)
    else:
        print "this.py custmgui.dll"
