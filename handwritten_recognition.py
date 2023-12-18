import os, io
from google.cloud import vision
from google.cloud.vision_v1 import types
import pandas as pd 


# client 
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'PhotoExam.json'
client = vision.ImageAnnotatorClient()

# reading image
image_path = './WhatsApp Image 2023-12-14 at 22.49.30.jpeg'
with io.open(image_path, 'rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content)

# converting image to text
response = client.document_text_detection(image=image)
full_txt = response.full_text_annotation.text
print(full_txt)


# # check for each word confidence level
# for page in response.full_text_annotation.pages:
#         for block in page.blocks:
#             print(f"\nBlock confidence: {block.confidence}\n")

#             for paragraph in block.paragraphs:
#                 print("Paragraph confidence: {}".format(paragraph.confidence))

#                 for word in paragraph.words:
#                     word_text = "".join([symbol.text for symbol in word.symbols])
#                     print(
#                         "Word text: {} (confidence: {})".format(
#                             word_text, word.confidence
#                         )
#                     )

#                     for symbol in word.symbols:
#                         print(
#                             "\tSymbol: {} (confidence: {})".format(
#                                 symbol.text, symbol.confidence
#                             )
#                         )
