from PIL import Image
import numpy
import sys

def bin2img(bfilename, ofilename, format="RGBA"):
    print "Reading %s for input" % bfilename
    bfile = open(bfilename, "rb")
    barray = numpy.frombuffer(bfile.read(), dtype=numpy.uint8)

    if format == "RGBA":
        width = 4
    elif format == "RGB":
        width = 3
    else:
        raise ValueError("Only RGB and RGBA are accepted formats")

    barray = barray[:(barray.shape[0]/width) * width]
    bstack = numpy.dstack(tuple(barray[width-i::width] for i in range(width,0,-1)))[0]

    good_sqrt = int(numpy.sqrt(bstack.shape[0]))
    bstack = bstack[:good_sqrt*good_sqrt].reshape((good_sqrt,good_sqrt,width))
    im = Image.fromarray(bstack, mode=format)
    print "Saving image to %s" % ofilename
    im.save(ofilename, format="jpeg")

def main():
    import optparse
    usage = """
Create a JPEG image from a binary file

%prog [options] <binary file> <output name>"
"""
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("--rgb", default=False, dest="rgb", action="store_true",
            help="Use RGB formatting")
    parser.add_option("--rgba", default=True, dest="rgba", action="store_true",
            help="Use RGBA formatting (default)")
    options,args = parser.parse_args()

    if len(args) != 2:
        parser.print_usage()
        return -1

    bfilename = args[0]
    ofilename = args[1]
    if options.rgb:
        format = "RGB"
    else:
        format = "RGBA"

    bin2img(bfilename, ofilename, format=format)
    return 0

if __name__ == "__main__":
    sys.exit(main())

