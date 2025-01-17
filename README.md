# Image to Black & White Azure Function

Converts color images to black & white using Azure Function.

## Input Format
Send POST request with JSON body:
```json
{
    "image": "base64_encoded_image_string"
}