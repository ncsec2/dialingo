from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import azure.cognitiveservices.speech as speechsdk
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
# import argparse
#방언
from .translator import infer, run
import uuid
#번역
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
from azure.core.exceptions import HttpResponseError
import json


# def hello_world(request):
#     return HttpResponse("Hello, World!")

def hello_world(request):
    return render(request, 'record.html')

#음성, 문자 선택
def main_page(request):
    return render(request, 'main.html')

#시작하기
def start_page(request):
    return render(request, 'start.html')

#음성
def voice_page(request):
    return render(request, 'voice.html')

def voice_output_page(request):
    print("voice_output_page")
    context = {'translation_sentences': request.GET.get('translation_sentences')}
    return render(request, 'voiceOutput.html', context)         
#음성
def get_translation(request):
    print("get_translation")
    if request.method == 'POST':
        user_sentences = request.POST.get('user_sentences', '')
        result = run.main(user_sentences)
        print(type(result))

        if result is not None:
            return JsonResponse({'data': result})
        else:
            # 유효한 JSON 데이터가 아닌 경우에 대한 처리
            return JsonResponse({'error': 'Invalid response from run.main'})

    # POST 요청이 아닌 경우 404 에러 반환 또는 다른 처리
    return JsonResponse({'error': 'Invalid request method'})

#언어 번역
def lang_translation(request):
    key = "e779303e52cc41b8b0586435f0ae17c1"
    endpoint = "https://api.cognitive.microsofttranslator.com/"
    region = "koreacentral"

    credential = TranslatorCredential(key, region)
    text_translator = TextTranslationClient(endpoint=endpoint, credential=credential)

    lang = {'영어' : 'en', '베트남어' : 'vi', '일본어' : 'ja', '중국어' : 'zh-Hans', '태국어' : 'th', '필리핀어' : 'fil'}

    ########입력값########
    user_lang = '영어'
    if request.method == 'POST':
        json_data = json.loads(request.body.decode('utf-8'))
        translated_text = json_data.get('data', '')
        print(">>>>>>>.:", translated_text)
        # print(">>>>>>>.:", request.body)
        # translated_text = request.POST.get('data', '')
    #####################

    try:
        source_language = "ko"
        target_languages = [lang[user_lang]]
        input_text_elements = [ InputTextItem(text = translated_text) ]

        response = text_translator.translate(content = input_text_elements, to = target_languages, from_parameter = source_language)
        translation = response[0] if response else None

        if translation:
            for translated_text in translation.translations:
                print(f"번역 대상 언어: '{user_lang}', 번역 결과: '{translated_text.text}'.")
                return JsonResponse({'transcription':translated_text.text})

    except HttpResponseError as exception:
        print(f"Error Code: {exception.error.code}")
        print(f"Message: {exception.error.message}")



#문자
def text_page(request):
    return render(request, 'text.html')

#언어선택
def dialect_page(request):
    return render(request, 'dialect.html')


def get_voice(request, wav_name=None):
    # Speech 서비스 설정
    speech_key = 'a57a40a167fb4e108f0a76da10b11c00'
    service_region = 'koreacentral'

    # Speech 구독 정보 설정
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="ko-KR"

    # Speech 인식 엔진 생성
    # available_audio_devices = speechsdk.audio.AudioConfig.list_microphone_names()
    # print("Available Audio Devices:", available_audio_devices)
    
    # 마이크
    # audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    # print(file_config)
    # speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 오디오 파일 또는 오디오 스트림 지정 (예: WAV 파일 경로)
    print("wav_name: ", wav_name, type(wav_name))
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', 'jeju4.wav')

    if wav_name is not None:        
        audio_file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', str(wav_name))

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 인식 시작
    result = speech_recognizer.recognize_once_async().get()

    # result = speech_recognizer.recognize_once(audio_config)

    # 결과 반환
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # print(result.text)
        # decoded_string = bytes(result.text, 'utf-8').decode('unicode_escape')
        return JsonResponse({'transcription':result.text})
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return JsonResponse({'error': 'No speech could be recognized'})
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return JsonResponse({'error': f'Speech Recognition canceled: {cancellation_details.reason}'})

    # return render(request, 'voice.html', )

def translate(request):
    return render(request, 'voice.html')    



#type 변환 필요
@csrf_exempt  # 임시로 CSRF 보호 비활성화 (실제 프로젝트에서는 보안 고려 필요)
def save_recording(request):
    if request.method == 'POST':
        print("AB")
        print(request.FILES)
        print(request)
        # audio_file = audio = request.body
        print(request.FILES)
        audio_file = request.FILES.get('audio')
        print(audio_file)
        if audio_file:
            file_uuid = str(uuid.uuid4())
            file_name = file_uuid+'.wav'
            # file_name = file_uuid+'.webm'

            file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            
            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            #파일 읽기
            get_voice(request, file_name)

            return JsonResponse({'message': 'Recording saved successfully.'})
        else:
            return JsonResponse({'message': 'No audio file received.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)
