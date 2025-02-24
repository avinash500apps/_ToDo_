from backend.aws.s3 import s3,S3_REGION,UploadFile,File,BUCKET_NAME
from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            file.filename,
        )
        file_url = f"https://{BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file.filename}"
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "fileUrl": file_url,
        }
    except Exception as e:
        return {"error": str(e)}


@router.get("/get-image/{filename}")
async def get_image(filename: str):
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": filename},
            ExpiresIn=3600,
        )
        return {"image_url": url}
    except Exception as e:
        return {"error": str(e)}


@router.delete("/delete/{filename}")
async def delete_image(filename: str):

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)

        return {"message": "File deleted successfully", "filename": filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@router.put("/update/{filename}")
async def update_image(filename: str, file: UploadFile = File(...)):
    try:
        s3.head_object(Bucket=BUCKET_NAME, Key=filename)

        s3.upload_fileobj(file.file, BUCKET_NAME, filename)

        file_url = f"https://{BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{filename}"

        return {
            "message": "File updated successfully",
            "filename": filename,
            "fileUrl": file_url,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating file: {str(e)}")