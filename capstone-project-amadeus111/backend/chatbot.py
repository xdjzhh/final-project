# import flask.request as request
from flask import request
import backend.format_change as change

from flask import Flask
from flask_restplus import Resource, Api,fields
from api_demo.api_test import detect_intent_texts
from machine_learning.ir_model.model import inforetrival_model
import database.dao as dao
import pytesseract
from PIL import Image

from machine_learning.LSTM_model.preprocessing import prepocess
from machine_learning.LSTM_model.my_predict_model import run_predict

def after_request(response1):
    response1.headers['Access-Control-Allow-Origin'] = '*'
    response1.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
    response1.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response1

app=Flask(__name__)
app.after_request(after_request)
api = Api(app)
ir_model=inforetrival_model()
db=dao.connectdb()

@api.route('/main/<session_id>/<user_input>')
@api.param('session_id','use for the contex of the dialog')
@api.param('user_input','what the user sent to the server')
class chatbot(Resource):
    def post(self,session_id,user_input):
        if user_input=='tar=1':
            f=request.files['avatar']
            image = Image.open(f)
            code = pytesseract.image_to_string(image)
            user_input=code
        response=detect_intent_texts(session_id,user_input)
        # print(session_id,user_input)
        if response.query_result.intent.display_name == 'Default Fallback Intent':
            qa_list = []
            for each in ir_model.get_the_topNans(5, user_input):
                temp = ir_model.df.loc[each[0]]
                # print(temp.qapair)
                qa_list.append(temp.qapair)
            raw_ans = dao.query_anser_top(db, qa_list)
            ans_list = [prepocess(i) for i in raw_ans]

            index = run_predict(prepocess(user_input), ans_list)
            res = raw_ans[index]
            return res, 200

            # qapair=ir_model.df.loc[ir_model.get_the_topNans(5,user_input)[0][0]].qapair
            # res=dao.query_anser_id(db,qapair)
            # print(qapair)
            # return res[0],200
            # return dao.query_anser_id(db,ir_model.df.loc[ir_model.get_the_topNans(1,user_input)[0][0]].qapair),200
        elif response.query_result.intent.display_name[0] in ['K','k']:
            ans=response.query_result.knowledge_answers.answers
            temp=str(ans).split('\n')
            return temp[2], 200
            pass
        elif response.query_result.intent.display_name == 'course info':
            course_name = response.query_result.parameters.fields['course_name'].string_value
            course_number = response.query_result.parameters.fields['course_number'].string_value
            print(type(response.query_result.fulfillment_text))
            print(response.query_result.fulfillment_text)
            if course_name == '' and course_number == '':
                pass
            else:
                list = change.format_change(dao.query_of_user(db,course_name, course_number)[0])
                string = list.tostring()
                return string,200
        return response.query_result.fulfillment_text,200
        # pass


if __name__ == '__main__':
    app.run(debug=True)