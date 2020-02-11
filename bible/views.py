from django.shortcuts import render
import os
# Create your views here.
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from google.cloud import texttospeech
from . db import BibleDataGetter
import urllib3
import json
from ast import literal_eval
# Create your views here.
def getBibleData(request) :
    question = request.GET['question']
    bdg = BibleDataGetter()
    
    book, chap, verse, get_para = bdg.recogBiblePosition(question)
    if get_para :
        title, content = bdg.getBibleParagraph(book, chap, verse)
    else :
        title, content = bdg.getBibleVerse(book, chap[0], verse[0])
    print(title, content)
    return title, content

def clean_text(text):
    text = re.sub("[\r\n]", "", text)
    return text

def todayBible(request) :
    today = get_today_bible()
    bdg = BibleDataGetter()
    book, chap, verse, get_para = bdg.recogBiblePosition(today)
    if get_para :
        title, content = bdg.getBibleParagraph(book, chap, verse)
    else :
        title, content = bdg.getBibleVerse(book, chap[0], verse[0])
    #{"index": index, "contents": contents,"simple": today_simple,"all": all_contents}
    print(content)
    return render(request, 'todayBible.html', {"content" : content })


def bible(request):
    question = request.GET['question']

    #title_name = Dict[result]
    #jang = Jang.objects.get(title=title_name)
    try:
        title,contents = getBibleData(request)
        return render(request, 'bible.html', {'question': question, 'title': title ,'contents': contents})
    except:
        return render(request, 'notfound.html')

def get_today_bible():
    #오늘의 말씀
    url = "http://qt.swim.org/user_utf/life/user_print_web.php?"
    result = urlopen(url)
    html = result.read()
    soup = BeautifulSoup(html, 'html.parser')


    strong = soup.find_all("strong")
    index = strong[1].text
    index = index.replace(":", "장 ")
    index = index.replace("-", "에서")
    index = index.split()
    index.insert(3, "절")
    index.insert(7, "절")
    index.insert(1, " ")
    index.insert(3, " ")
    index.insert(6, " ")
    index.insert(8, " ")
    index.insert(10, " ")
    result= ""
    for i in index:
        result += i
    return result

def generateMP3(contents):
    #credentials = service_account.Credentials.from_service_account_file('./voiceauth.json')

    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.types.SynthesisInput(text=contents)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ko-KR',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL,
        name = "ko-KR-Wavenet-C")

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)
        
    return response.audio_content

def respondAudioFile(request):
    textQuery = request.GET['textQuery'] # tts에 들어갈 글 
    
    ttsAudio = generateMP3(textQuery)
    response = HttpResponse(ttsAudio)
    response['Content-Type'] ='audio/mp3'
    return response

def qa(request):
    question = request.GET['question']
    contents = request.GET['contents']
    answer = get_ans_from_passage(question,contents)
    return render(request, 'q_a.html', {'question': question, 'answer': answer ,'contents': contents, 'source':"erti"})

def qa2(request):
    question = request.GET['question']
    contents = request.GET['contents']
    answer = get_ans_from_passage2(question,contents)
    return render(request, 'q_a.html', {'question': question, 'answer': answer ,'contents': contents, 'source': "DMSLab"})


def get_ans_from_passage(question,passage):
    openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
    accessKey = "730fbff1-9460-4e55-9086-6b3341155647"
    question = question
    passage = passage
    requestJson = {
    "access_key": accessKey,
        "argument": {
            "question": question,
            "passage": passage
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    my_bytes_value = response.data
    my_json = my_bytes_value.decode('utf8').replace("'", '"')

    data = json.loads(my_json)
    answer= str(data['return_object']['MRCInfo']['answer'])
    return answer

def get_ans_from_passage2(q,p):
    ApiURL = "http://117.16.136.56:8000/mrc"
    paragraph = p
    question = q

    requestJson = {
        "argument": {
            "paragraph": paragraph,
            "question": question
        }
    }

    http = urllib3.PoolManager()
    response = http.request(
        "POST",
        ApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )
    print("[responseCode] " + str(response.status))
    print("[responBody]")
    return response.data.decode('utf-8')