from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
import re

TEMPLATE_CV = ["information",
               "personal details",
               "summary",
               "skills",
               "work experience",
               "experience",
               "employment",
               "study",
               "education",
               "personality",
               "awards",
               "references",
               "interests"]

TEMPLATE_INFORMATION = ["information",
                        "personal details"]

TEMPLATE_SUMMARY = ["summary",
                    "objective"]

TEMPLATE_SKILLS = ["skill",
                   "skills",
                   "personality"] #tinh cach : team-work

TEMPLATE_EXPERIENCE = ["work experience,"
                       "experience",
                       "employment"]

TEMPLATE_EDUCATION = ["study",
                      "education"]

TEMPLATE_AWARDS = ["awards"]

TEMPLATE_REFERENCES = ["references"]

TEMPLATE_INTERESTS = ["interests"]

LIST_SKILLS_1 = ["Java","C","C++","Scala"] #update them
LIST_SKILLS_2 = ["Communication","Presentation","Individual working","Team-work"]
# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES [ 'file' ] :
        myfile = request.FILES [ 'file' ]
        fs = FileSystemStorage ( )
        filename = fs.save ( myfile.name , myfile )
        uploaded_file_url = fs.url ( filename )
        data = read_pdf ( filename ).split("\n")
        temp = getTemp(data)

        res = {
                'information': '',
                'summary': '',
                'skills': '',
                'experience': '',
                'education': '',
                'awards': '',
                'references': '',
                'interests': ''
                }
        for num, i in enumerate(temp, start=0):
            if num < len(temp) - 1 : end = temp[num+1][1]
            else: end = len(temp) - 1
            if(i[0] == 'information'):
                res['information'] = getInfor(data,i[1],end)
            if(i[0] == 'skills'):
                res['skills'] = getSkills(data,i[1],end)
        fs.delete ( filename )
        return JsonResponse(res)
    data = {
        'information': '',
        'summary': '',
        'skills': '',
        'experience': '',
        'education': '',
        'awards': '',
        'references': '',
        'interests': ''
        }
    return JsonResponse(data)


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



from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
import re

def read_pdf(filename):
    path = './file/' + filename
    fp = open(path, 'rb')
  #fp = open('AmazonWebServices.pdf', 'rb')
  #fp = open('hr_phuong.pdf', 'rb')

    rsrcmgr = PDFResourceManager()

    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    pages = PDFPage.get_pages(fp)

    data = ""
    for page in pages:
        print('Processing next page...')
        interpreter.process_page(page)
        layout = device.get_result()
        for lobj in layout:
            if isinstance(lobj, LTTextBox):
              x, y, text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
              a = re.findall(r"""((\w*[\\\/\n:+ .!@#$%^&*()_+=<>,?;"'{[}\]\|-]*)*)""",text)
              b = " ".join(map(str,list(map(''.join, a))))
              data += b
    return data

def getFirstData(t):
    return t[0]

def takeSecond(elem):
    return elem[1]

def getTemp(data):
    arrTemp = []
    for num, i in enumerate(data, start=0):
        a = i.lower().strip()
        if a in TEMPLATE_INFORMATION:
            arrTemp.append(("information",num))
        elif a in TEMPLATE_SUMMARY:
            arrTemp.append(("summary",num))
        elif a in TEMPLATE_SKILLS:
            arrTemp.append(("skills",num))
        elif a in TEMPLATE_EXPERIENCE:
            arrTemp.append(("experience",num))
        elif a in TEMPLATE_EDUCATION:
            arrTemp.append(("education",num))
        elif a in TEMPLATE_AWARDS:
            arrTemp.append(("awards",num))
        elif a in TEMPLATE_REFERENCES:
            arrTemp.append(("references",num))
        elif a in TEMPLATE_INTERESTS:
            arrTemp.append(("interests",num))
    if(arrTemp[0][0] != "information" and arrTemp[0][1] !=  0) :
        arrTemp.append(("information",0))
    arrTemp.sort(key=takeSecond)
    return arrTemp

def getInfor(data,start,end):
    paragraphData = "".join(data[start:end])
    print(paragraphData)
    list_name = re.findall(r"((([ ]*[A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬÂẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ]{2,})+)+|([ ]*[A-Z][a-z_àáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳâấầẫậẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+)+)", paragraphData)
    list_phone = re.findall(r"(\d{10})",paragraphData)
    list_email = re.findall(r"(\w+@(gmail.com|yahoo.com|vnu.edu.vn))",paragraphData)
    #print("------------------")
    #print(list_name)
    #print(list_phone)
    #print(list_email)
    if list(map(getFirstData,list_name)) : name = list(map(getFirstData,list_name))[0]
    else: name ="No Name"
    if list(list_phone): phone =list(list_phone)[0]
    else: phone ="No Phone"
    if list(map(getFirstData,list_email)): email =list(map(getFirstData,list_email))[0]
    else: email ="No Email"
    data = {
            "Name":name,
            "Phone":phone,
            "Email": email
            }
    return data

def getSkills(data,start,end):
    paragraphData = " ".join(data[start:end])
    skills_1 = []
    skills_2 = []
    for i in LIST_SKILLS_1:
        if i in paragraphData: skills_1.append(i)
    #for i in LIST_SKILLS_2:
     #   if i in paragraphData: skills_2.append(i)
    return {"skills_1": skills_1}






