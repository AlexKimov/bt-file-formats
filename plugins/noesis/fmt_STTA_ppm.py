from inc_noesis import *


def registerNoesisTypes():
    handle = noesis.register("Starship Troopers Terran Ascendancy texture", ".ppm")
    noesis.setHandlerTypeCheck(handle, STTACheckType)
    noesis.setHandlerLoadRGBA(handle, STTALoadRGBA)

    return 1
       
  
class STTAImage:
    def __init__(self, reader):
        self.filereader = reader
        self.width = 0
        self.height = 0
        self.format = ""
        self.size = ""
        self.data = None
 
    def parseHeader(self):
        self.format = self.filereader.readline()[:-1]       
        self.str = self.filereader.readline()
        if "#" in self.str:
            size = self.filereader.readline()
        else:
            size = self.str
        
        self.width, self.height  = [int(x) for x in size[:-1].split(" ")]
        self.filereader.seek(4, NOESEEK_REL)
        
        return 0            

    def getImageData(self):
        if self.format == "P7":
            size = self.width * self.height * 4
            format = "r8g8b8a8"
        else:
            size = self.width * self.height * 3
            format = "r8g8b8"
          
        data = self.filereader.readBytes(size)
        self.data = rapi.imageDecodeRaw(data, self.width, self.height, format)
                               
    def read(self):
        self.parseHeader() 
        self.getImageData()
        
    
def STTACheckType(data):

    return 1  


def STTALoadRGBA(data, texList):
    #noesis.logPopup() 
    image = STTAImage(NoeBitStream(data))       
    image.read() 
         
    texList.append(NoeTexture("STTAtex", image.width, image.height, image.data, noesis.NOESISTEX_RGBA32))
        
    return 1
