import os

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.utils import handle_exceptions
from rest_framework.parsers import MultiPartParser
from .serializers import AudioUploadSerializer
from openai import OpenAI
from openai._exceptions import OpenAIError
import tempfile
from .models import AudioUpload

RETURN_RESPONSE = settings.RESPONSE_TEMPLATE
client = OpenAI(api_key=settings.OPEN_API_KEY)
# Create your views here.


class TranscribeAudio(APIView):

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    @handle_exceptions
    def post(self, request):
        serializer = AudioUploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            audio = request.FILES['audio']

            # save the uploaded audio temporarily

            try:
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_audio:
                    for chunk in audio.chunks():
                        temp_audio.write(chunk)
                    temp_audio.flush()
                    temp_path = temp_audio.name

                # send the file to OpenAI whisper

                with open(temp_audio.name, "rb") as f:
                    response = client.audio.transcriptions.create(model="whisper-1", file=f)

                    uploaded = AudioUpload.objects.create(user=request.user, audio=audio,
                                                          transcribed_text=response.text)
                    uploaded.save()
                    RETURN_RESPONSE['status'] = True
                    RETURN_RESPONSE['message'] = "Transcription successful"
                    RETURN_RESPONSE['data'] = {
                        "transcription" : response.text
                    }
                    return Response(RETURN_RESPONSE, status=status.HTTP_200_OK)

            except OpenAIError as e:
                RETURN_RESPONSE['status'] = False
                RETURN_RESPONSE['message'] = f"{e}"
                RETURN_RESPONSE['data'] = {}
                return Response(RETURN_RESPONSE, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            finally:
                os.remove(temp_path)

        RETURN_RESPONSE['status'] = False
        RETURN_RESPONSE['message'] = "Transcription failed"
        RETURN_RESPONSE['data'] = {
            "error" : serializer.errors
        }
        return Response(RETURN_RESPONSE, status=status.HTTP_400_BAD_REQUEST)