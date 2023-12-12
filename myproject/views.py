from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import azure.cognitiveservices.speech as speechsdk
import json


# def hello_world(request):
#     return HttpResponse("Hello, World!")

def hello_world(request):
    return render(request, 'hello.html')

def main_page(request):
    return render(request, 'main.html')

def start_page(request):
    return render(request, 'start.html')

def voice_page(request):
    return render(request, 'voice.html')


def get_voice(request):
    print("get voice==============")
    # Speech 서비스 설정
    speech_key = 'a57a40a167fb4e108f0a76da10b11c00'
    service_region = 'koreacentral'

    # Speech 구독 정보 설정
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="ko-KR"

    # Speech 인식 엔진 생성
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # 오디오 파일 또는 오디오 스트림 지정 (예: WAV 파일 경로)
    # audio_file_path = 'path/to/your/audio/file.wav'
    # audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

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

def text_page(request):
    return render(request, 'text.html')
