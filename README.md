# Serverless Face Dectector API

This is REST API which includes only one API endpoint for now.
It takes base64 encoded image content and returns coordinates of bounding boxes for the faces detected from given image.

It detects human frontal faces using [DNN](https://docs.opencv.org/master/d2/d58/tutorial_table_of_content_dnn.html).

Recommended python version: 3.7

## Deploy

First setup aws credentials using following command. 

```bash
sls config credentials --provider aws --profile honorlock --key [AWS_KEY] --secret [AWS_SECRET]
```

In order to deploy the endpoint, simply run 

```bash
sls deploy
```

## Usage

You can do base64 encode of the source image and detect human faces from it using below commands.

Imagine used api key looks like this: `9WN&]/jR#8NHT(P6\8u+8)S:a`

### Base64 encode

```bash
base64 -w 0 picture-with-human-faces.jpg > picture-with-human-faces.jpg.base64
```

### Detect face

```bash
curl --location --request GET 'https://xxxx.execute-api.us-east-1.amazonaws.com/dev/detect' \
--header 'x-api-key: 9WN&]/jR#8NHT(P6\8u+8)S:a' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'image=PASS_BASE64_ENCODED_IMAGE_AS_STRING_HERE'
```

Example Result:

It returns detected face bounding boxes position as array.  [x, y, width, height]

```json
[
    [
        900,
        124,
        80,
        80
    ],
    [
        442,
        27,
        88,
        88
    ],
    [
        295,
        280,
        100,
        100
    ],
    [
        496,
        292,
        95,
        95
    ]
]
```
