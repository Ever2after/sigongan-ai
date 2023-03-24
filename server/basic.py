from flask import request
from flask_restx import Resource, Api, Namespace, fields
from chat_ai import *

Basic = Namespace('Basic')

basic_imageUrl = Basic.model('Basic', {  # Model 객체 생성
    'imageUrl': fields.String(description='url of the image', required=True, example="https://picsum.photos/200/300")
})

basic_imageUrl_labels = Basic.inherit('Basic with labels', basic_imageUrl,  {
    'labels': fields.List(fields.String(), description='list of label', required=True, default=['photo', 'text'])
})

@Basic.route('/ocr')
class Basic_OCR(Resource):
    @Basic.expect(basic_imageUrl)
    def post(self):
        imageUrl = request.json.get('imageUrl')
        sigongan = SigonganAI(imageUrl)
        ocr = sigongan.imgOCR()
        return {"result": ocr}
    
@Basic.route('/caption')
class Basic_Caption(Resource):
    @Basic.expect(basic_imageUrl)
    def post(self):
        imageUrl = request.json.get('imageUrl')
        sigongan = SigonganAI(imageUrl)
        caption = sigongan.img2text()
        return {"result": caption}

@Basic.route('/0class')
class Basic_0class(Resource):
    @Basic.expect(basic_imageUrl_labels)
    def post(self):
        imageUrl = request.json.get('imageUrl')
        labels = request.json.get('labels')
        sigongan = SigonganAI(imageUrl)
        class0 = sigongan.img0Class(labels)
        return {"result": class0}