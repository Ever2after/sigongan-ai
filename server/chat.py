from flask import request
from flask_restx import Resource, Api, Namespace, fields
from chat_ai import *

Chat = Namespace('Chat')

chat_message = Chat.model('Chat', {  # Model 객체 생성
    "role": fields.String(description="'assistant', 'user', 'system'", required=True, default="user"),
    "content": fields.String(description="content of the message", example="nice to meet you"),
})

chat_messages = Chat.model('Chats', {
    "messages": fields.List(fields.Nested(
        chat_message
    ), description="List of the message", required=True)
})

@Chat.route('/')
class Chat_(Resource):
    @Chat.expect(chat_messages)
    def post(self):
        messages = request.json.get('messages')
        sigongan = SigonganAI('')
        sigongan.initMessage(messages)
        answer = sigongan.getGPT()
        return {"result": answer}
