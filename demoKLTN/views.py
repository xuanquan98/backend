from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import JsonResponse
import re
import upload as uploadToDrive
import smtplib
from django.shortcuts import render
from .models import CV
from django.contrib.auth import authenticate
import sys

# Create your views here.

TEMPLATE_INFORMATION = ["information",
                        "personal details",
                        "contact",
                        "personal infor",
                        "thông tin cá nhân",
                        "thông tin",
                        "thông tin liên hệ"]

TEMPLATE_SUMMARY = ["summary",
                    "objective",
                    "resume summary",
                    "mục tiêu nghề nghiệp",
                    "tóm tắt"]

TEMPLATE_SKILLS = ["skill",
                   "skills",
                   "personality",
                   "kĩ năng"] #tinh cach : team-work

TEMPLATE_EXPERIENCE = ["work experience",
                       "experience",
                       "employment",
                       "kinh nghiệm"]

TEMPLATE_EDUCATION = ["study",
                      "education",
                      "trình độ học vấn",
                      "học vấn"]

TEMPLATE_AWARDS = ["awards",
                   "giải thưởng"]

TEMPLATE_REFERENCES = ["references",
                       "reference",
                       "thông tin thêm"]

TEMPLATE_INTERESTS = ["interests",
                      "sở thích"]

LIST_SKILLS_1 = ["Java","C","C++","Scala","Mysql","Nosql","MongoDB","Git","Svn"] #update them
LIST_SKILLS_2 = ["Communication","Presentation","Individual working","Team-work"]
# Create your views here.
def index(request):
    if request.method == "POST" and request.FILES [ 'file' ] :
        myfile = request.FILES [ 'file' ]
        fs = FileSystemStorage ( )
        filename = fs.save ( myfile.name , myfile )
        file_id = uploadToDrive.writeToGDrive(filename)
        link = "https://drive.google.com/file/d/"+ file_id +"/view"
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
            else: end = len(data) - 1
            if(i[0] == 'information'):
                res['information'] = getInfor(data,i[1],end,temp)
            elif(i[0] == 'skills'):
                res['skills'] = getSkills(data,i[1],end)
            elif(i[0] == 'summary'):
                res['summary'] = getSummary(data,i[1],end)
            elif(i[0] == 'experience'):
                res['experience'] = getExperience(data,i[1],end)
            elif(i[0] == 'education'):
                res['education'] = getEducation(data,i[1],end)
            elif(i[0] == 'awards'):
                res['awards'] = getAwards(data,i[1],end)
            elif(i[0] == 'references'):
                res['references'] = getReferences(data,i[1],end)
            elif(i[0] == 'interests'):
                res['interests'] = getInterest(data,i[1],end)

        saveDB(filename,link,res['skills'],res['information'])
        sendEmail(res['information']['Email'],res['information']['Name'])
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
    result = []
    print('---------------------')
    print(data)
    for num, i in enumerate(data, start=0):
        b = re.findall(r"((\w*[ ]*)*)",i)
        c =" ".join(map(str,list(map(''.join, b))))
        a = c.lower().strip()
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
    if(arrTemp == [] or (arrTemp[0][0] != "information" and arrTemp[0][1] !=  0 )) :
        arrTemp.append(("information",0))
    arrTemp.sort(key=takeSecond)
    return arrTemp

def getInfor(data,start,end,arrTemp):
    if (start != 0):
        paragraphData = " ".join(data[start + 1 :end])
    else:
        paragraphData = " ".join(data[start:end])
    if (arrTemp[0][1] !=  0):
        paragraphData = " ".join(data[0:arrTemp[0][1]]) + " " + paragraphData
    print(paragraphData)

    if (paragraphData.lower().find('full name') != -1 | paragraphData.lower().find('họ và tên') != -1):
        print("111111111")
    else: print("2222222222")
    list_name = re.findall(r"((([ ]*[A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬÂẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴÝỶỸ]{2,})+)+|([ ]*[A-Z][a-z_àáâãèéêìíòóôõùúăđĩũơưăạảấầẩẫậắằẳâấầẫậẵặẹẻẽềềểễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]+)+)", paragraphData)
    list_phone = re.findall(r"(\d{10})",paragraphData)
    list_email = re.findall(r"(\w+@(gmail.com|yahoo.com|vnu.edu.vn))",paragraphData)
    list_date = re.findall(r"\b((\d{1,4}|Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)[\/\-. ](\d{1,2}|Jan|Feb|Mar|Apr|May|Jun|July|Aug|Sep|Oct|Nov|Dec|January|February|March|April|May|June|July|August|September|October|November|December)[\/\-.](\d{1,4}))\b|\b(\d{8})\b|\b(\d{6}[\/\-. ]?\d{1,2})\b|\b(\d{4}[\/\-. ]?\d{2,4})\b|\b(\d{2}[\/\-. ]?\d{4,6})\b|\b(\d{3}[\/\-. ]?\d{4})\b|\b(\d{5}[\/\-. ]?\d{1,2})\b",paragraphData)

    gender = 'Empty'
    if (paragraphData.find('male') != -1 or paragraphData.find('men') != -1 or paragraphData.find('Male') != -1 or paragraphData.find('MALE') != -1 or paragraphData.find('Men') != -1 or paragraphData.find('Men') != -1 or paragraphData.find('Nam') != -1) or paragraphData.find('name') != -1:
        gender = 'male'
    elif (paragraphData.find('female') != -1 or paragraphData.find('women') != -1 or paragraphData.find('Female') != -1 or paragraphData.find('Women') != -1 or paragraphData.find('FEMALE') != -1 or paragraphData.find('WOMEN') != -1) or paragraphData.find('Nữ') != -1 or paragraphData.find('nữ') != -1:
        gender = 'female'

    #print("------------------")
    #print(list_name)
    #print(list_phone)
    #print(list_email)
    if list(map(getFirstData,list_name)) : name = list(map(getFirstData,list_name))[0]
    else: name ="No name"
    if list(list_phone): phone =list(list_phone)[0]
    else: phone ="No phone"
    if list(map(getFirstData,list_email)): email =list(map(getFirstData,list_email))[0]
    else: email ="No email"
    if list(map(getFirstData,list_date)): date =list(map(getFirstData,list_date))[0]
    else: date ="No date"



    data = {
            "Name":name,
            "Phone":phone,
            "Email": email,
            "Gender": gender,
            "DateOfBirth": date,
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


def getSummary(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData

def getExperience(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData

def getEducation(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData

def getAwards(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData

def getReferences(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData

def getInterest(data,start,end):
    paragraphData = " ".join(data[start:end])
    return paragraphData


def saveDB(filename,link,skill,info):
    cv = CV()
    cv.nameCv = filename
    cv.fullName = info['Name']
    cv.email = info['Email']
    cv.gender = info['Gender']
    cv.dateOfBirth = info['DateOfBirth']
    cv.phone = info['Phone']
    cv.link = link
    cv.skill = skill
    cv.save()

def listCv(request):
    if request.method == "GET" :
        month = request.GET.get('month')
        year = request.GET.get('year')
        data =  list(CV.objects.filter(date__year = year).filter(date__month = month).values())
        return JsonResponse({'data': data})


def sendEmail(email,name):
    if email != 'No email':
        gmail_user = 'quanvu.kltn@gmail.com'
        gmail_password = 'xuanquan98'

        sent_from = gmail_user
        to = [email]
        subject = 'Email from Quan_'
        body = """
        Hello 
        Thanks for sending us your CV.
        We will contact you soon
        """
        print(body)
        email_text = """\
            From: %s
            To: %s
            Subject: %s

            %s
            """ % (sent_from, ", ".join(to), subject, body)

        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print('Email sent!')
        except:
            print(sys.exc_info()[0])
            print('Something went wrong...')
    else: print("No email")


def login(request):
    if request.method == "POST":
        data = request.POST.copy()
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            response = JsonResponse({'data':data['username']})
            response.set_cookie(key='user', value=data['username'])
            return response
            # A backend authenticated the credentials
        else:
            return JsonResponse({'data':'Fail'})
            # No backend authenticated the credentials

def logout(request):
    return JsonResponse({'data':'1'})