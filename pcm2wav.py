#!/usr/bin/env python

def pcm2wav(infile,outfile):
    import struct
    print "pcm2wav:  %s --> %s"%(infile,outfile)

    # this follows https://de.wikipedia.org/wiki/RIFF_WAVE


    file_in = file(infile,"rb")
    file_out = file(outfile,"wb")




    fmt_length = 16
    format_tag = 1 # PCM; now I understand why Bram Bos did not wat to support .wav ;)
    channels = 1
    sample_rate = 44100
    bits_sample = 16
    framesize = channels * int((bits_sample + 7)/8)
    bytes_sec = sample_rate * framesize
    block_align = framesize

    #4 4 2 2 4 4 2 2

    fmt = struct.pack("ccccIhhIIhh",'f','m','t',' ',fmt_length, format_tag, channels, sample_rate, bytes_sec, block_align, bits_sample)

    

    raw_data = file_in.read()

    data_length = len(raw_data)
    data = struct.pack("ccccI",'d','a','t','a',data_length)

    filesize = len(raw_data) + len(data) + len(fmt) + 12 - 8 # size of all, including len(riff_header) - 4 (propably "RIFF"
    riff_header = struct.pack('ccccIcccc','R','I','F','F',filesize,'W','A','V','E')




    file_out.write(riff_header)
    file_out.write(fmt)
    file_out.write(data)
    file_out.write(raw_data)

    file_in.close()
    file_out.close()

    return



if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        pcm2wav(sys.argv[1],sys.argv[2])
    else:
        print "this.py in.pcm out.wav"
