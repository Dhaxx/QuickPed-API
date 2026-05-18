import uuid
import boto3
from fastapi import UploadFile
from botocore.exceptions import ClientError
from app.core.config import settings


class ImageUploadService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.CLOUDFLARE_R2_ENDPOINT_URL,
            aws_access_key_id=settings.CLOUDFLARE_R2_ACCESS_KEY_ID,
            aws_secret_access_key=settings.CLOUDFLARE_R2_SECRET_ACCESS_KEY,
            region_name="auto"
        )
        self.bucket_name = settings.CLOUDFLARE_R2_BUCKET_NAME

    async def upload_image(self, file: UploadFile) -> str:
        """
        Faz o upload de um arquivo de imagem para o Cloudflare R2 e retorna sua URL pública.
        """
        try:
            # Gerar um nome de arquivo único
            file_extension = file.filename.split(".")[-1] if "." in file.filename else "png"
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            # Ler o conteúdo do arquivo
            contents = await file.read()
            # Upload para o R2
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=unique_filename,
                Body=contents,
                ContentType=file.content_type,
            )
            return unique_filename
        except ClientError as e:
            # Tratar erros do S3/R2
            print(f"Erro ao fazer upload para o R2: {e}")
            raise  # Re-raise para que o endpoint da API possa tratar
        except Exception as e:
            print(f"Erro inesperado ao fazer upload de imagem: {e}")
            raise


_image_upload_service = None

def get_image_upload_service() -> ImageUploadService:
    global _image_upload_service
    if _image_upload_service is None:
        _image_upload_service = ImageUploadService()
    return _image_upload_service