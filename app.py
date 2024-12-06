from chalice import Chalice
import boto3

app = Chalice(app_name='polly')

@app.route('/')
def synthesize_and_upload():
    text = "girino é um bebê sapo"
    voice_id = 'Camila'
    audio_format = 'mp3'
    output_key = 'girino.mp3'
    bucket_name = '<<bucket-name>>'  # Nome do bucket

    polly_client = boto3.client('polly')
    s3_client = boto3.client('s3')

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=audio_format,
            VoiceId=voice_id
        )

        audio_stream = response['AudioStream']

        s3_client.upload_fileobj(audio_stream, bucket_name, output_key)
        return {'message': f'Audio saved in S3 bucket "{bucket_name}" with key "{output_key}".'}
    except Exception as e:
        return {'error': str(e)}
