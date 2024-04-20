import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

kr_timezone = pytz.timezone('Asia/Seoul')
now = datetime.now(kr_timezone)
print(now)
weekday_num = now.weekday()
today = str(now)
today = today[:10]
today = today.replace("-", ".")

# 비전타워 url
vision_url = "https://www.gachon.ac.kr/kor/7347/subview.do"
# 교육대학원 url
edu_url = "https://www.gachon.ac.kr/kor/7349/subview.do"
# 학생생활관 url
dorm_url = "https://www.gachon.ac.kr/kor/7350/subview.do"
# 메디컬캠퍼스 url
medical_url = "https://www.gachon.ac.kr/kor/7351/subview.do"

def search_meal(url):
    # 웹페이지에 요청을 보내고 응답을 받음
    response = requests.get(url)

    # 응답 파싱하여 BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 학식 정보가 포함된 요소 찾기
    meal_info = soup.find('div', class_='table_1')

    # 텍스트를 줄 단위로 분할하여 처리
    lines = meal_info.text.strip().split('\n')
    # 리스트 속 공백 제거
    lines = list(filter(None, lines))
    # 리스트 안에 있는 각 문자열에서 \r을 \n로 바꾸기
    lines = [line.replace('\r', '\n') for line in lines]
    lines = lines[4:]

    return lines

vision_list = search_meal(vision_url)
edu_list = search_meal(edu_url)
dorm_list = search_meal(dorm_url)
medical_list = search_meal(medical_url)

def get_meal(location):
    if weekday_num == (5 or 6) and location != 2:
        today_meal = "오늘은 주말! 평일에 봐요!"
    
    else:
        today_meal = ""

        # vision
        if location == 0:
            index = 7
            meal_list = vision_list
            today_meal += "오늘의 비타 밥\n\n"
        # edu
        elif location == 1:
            index = 5
            meal_list = edu_list
            today_meal += "오늘의 교대 밥\n\n"
        # dorm
        elif location == 2:
            index = 9
            meal_list = dorm_list
            today_meal += "오늘의 긱식\n\n"
            if weekday_num == 5:
                # index = 9
                meal_list = [line.replace(' ', '') for line in meal_list]
                joinline = meal_list[45] + " " + meal_list[47]
                meal_list = meal_list[:45] + [joinline] + meal_list[48:]
        # medical
        elif location == 3:
            index = 5
            meal_list = medical_list
            meal_list = [line.replace(' ', '') for line in meal_list]
            today_meal += "오늘의 메캠 밥\n\n"


        # 메뉴 정보를 담을 딕셔너리 생성
        menu_dict = {}
        current_menu = []
        i = 0

        while i < len(meal_list):
            if meal_list[i].startswith("2024."):
                current_menu = []
                current_date = meal_list[i]
                for j in range(i+1, i+index):
                    current_menu.append(meal_list[j])
            menu_dict[current_date] = current_menu
            i = i + 1

        for date, menu in menu_dict.items():
            if (today == date[:10]):
                # print(date)
                today_meal += date + "\n"
                i = 0
                for item in menu:
                    if i % 2 == 0 and i != 0:
                        # print()
                        today_meal += "\n"
                    # print(item)
                    today_meal += item + "\n"
                    i += 1
                # print("\n")
                today_meal += "\n"

        today_meal += "행복한 하루 되세요 ^^"    

    # print(menu_dict)
    return today_meal


def get_all_meal():
    all_meal = get_meal(0) + "\n" + get_meal(1) + "\n" + get_meal(2) + "\n" + get_meal(3)
    return all_meal

print(get_meal(2))