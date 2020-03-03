from django.core.files.storage import FileSystemStorage
from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES [ 'file' ] :
        myfile = request.FILES [ 'file' ]
        fs = FileSystemStorage ( )
        filename = fs.save ( myfile.name , myfile )
        uploaded_file_url = fs.url ( filename )
        data = convert_pdf_to_txt ( filename )
        print ( "--------------------" )
        print ( data )
        fs.delete ( filename )
   return render(request, 'pages/base.html')


from pdfminer.pdfinterp import PDFResourceManager , PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt ( filename ) :
    path = './file/' + filename
    rsrcmgr = PDFResourceManager ( )
    retstr = StringIO ( )
    laparams = LAParams ( )
    device = TextConverter ( rsrcmgr , retstr , laparams = laparams )
    fp = open ( path , 'rb' )
    interpreter = PDFPageInterpreter ( rsrcmgr , device )
    password = ""
    maxpages = 0
    caching = True
    pagenos = set ( )

    for page in PDFPage.get_pages ( fp , pagenos , maxpages = maxpages , password = password , caching = caching ,
                                    check_extractable = True ) :
        interpreter.process_page ( page )

    text = retstr.getvalue ( )
    print ( "==============" )
    print ( text )
    fp.close ( )
    device.close ( )
    retstr.close ( )
    return text
