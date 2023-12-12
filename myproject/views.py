from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import azure.cognitiveservices.speech as speechsdk
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os

# def hello_world(request):
#     return HttpResponse("Hello, World!")

def hello_world(request):
    return render(request, 'record.html')

def main_page(request):
    return render(request, 'main.html')

def start_page(request):
    return render(request, 'start.html')

def voice_page(request):
    return render(request, 'voice.html')

def text_page(request):
    return render(request, 'text.html')


def get_voice(request):
    print("get voice==============")
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
    print(settings.MEDIA_ROOT)
    audio_file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', 'jeju1.wav')
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

#type 변환 필요
@csrf_exempt  # 임시로 CSRF 보호 비활성화 (실제 프로젝트에서는 보안 고려 필요)
def save_recording(request):
    if request.method == 'POST':
        audio_file = request.FILES.get('audio')
        if audio_file:
            file_path = os.path.join(settings.MEDIA_ROOT, 'recordings', 'recording.wav')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            
            if os.path.exists(file_path):
                os.remove(file_path)

            with open(file_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            return JsonResponse({'message': 'Recording saved successfully.'})
        else:
            return JsonResponse({'message': 'No audio file received.'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=405)
