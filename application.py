from flask import Flask, request, jsonify
import meal

all_meal = meal.get_all_meal()
application = Flask(__name__)

@application.route("/")
def hello():
    return all_meal

@application.route("/meal",methods=['POST'])
def meal_bot():
    req = request.get_json()
    
    meal_type = req["action"]["detailParams"]["Meal"]["value"]	# json파일 읽기
    
    # 답변 텍스트 설정
    if meal_type == '비타':
        answer = meal.get_meal(0)
    elif meal_type == '교대':
        answer = meal.get_meal(1)
    elif meal_type == '긱식':
        answer = meal.get_meal(2)
    elif meal_type == '메캠':
        answer = meal.get_meal(3)
    else:
        answer = "비타/교대/긱식/메캠 중 하나를 입력해보세요!"
        
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    # 답변 전송
    return jsonify(res)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5000, threaded=True)