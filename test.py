import streamlit as st
import openai
import os
import requests
import json
import re


WEATHER_API_KEY = os.environ["WEATHER_API_KEY"]
city = "Seoul" # 도시는 서울로 지정
lang_code = "ko"

url = "http://api.weatherapi.com/v1/current.json" # 현재 날씨를 위한 요청

parameters = {
    "key": WEATHER_API_KEY, # API 키 지정
    "q": city,
    "lang": lang_code
}
r = requests.get(url, params=parameters)
current_weather = r.json()
print(current_weather)
# API 키 설정
openai.api_key = os.environ["OPENAI_API_KEY"]

# Chat Completion API를 이용해 사용자 입력에 따라 함수를 호출하고 응답하는 함수
# API 키 설정
openai.api_key = os.environ["OPENAI_API_KEY"]

# Chat Completion API를 이용해 사용자 입력에 따라 함수를 호출하고 응답하는 함수
def run_conversation(user_query):
    # 사용자 입력
    messages = [{"role":"user", "content":user_query}]
    
    # 함수 정보 입력
    functions = [
        {
            "name":"get_current_weather",
            "description": "도시 이름을 입력해 현재 날씨, 날짜, 시각, 몇 시인지 가져오기",
            "parameters": {
                "type": "object",
                "properties":{
                    "location": {
                        "type": "string",
                        "description": "도시 이름, 예를 들면, 서울, 부산, 대전",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["섭씨", "화씨"],
                        "description": "온도 단위로 섭씨 혹은 화씨",
                    },
                },
                "required": ["location"], # 필수 입력 변수 지정
            }
        }
    ]
    
    # 1단계: 사용자 입력과 함수 정보를 Chat Completions API 모델로 보내기
    response = openai.ChatCompletion.create( # Chat Completions API 모델로 보내기
        # model="gpt-3.5-turbo"
        model="gpt-3.5-turbo",
        messages=messages,
        functions=functions,
        function_call="auto"
    )
    
    # 2단계: 응답 생성
    response_message = response["choices"][0]["message"] # 모델의 응답 메시지
    
    if response_message.get("function_call"): # 응답이 함수 호출인지 확인하기
        # 3단계: JSON 객체를 분석해 함수 이름과 인수를 추출한 후에 함수 호출
        # (주의: JSON 응답이 항상 유효하지 않을 수 있음)
        
        # 호출할 함수 이름을 지정
        # (아래는 하나의 함수를 지정했지만 여러 함수 지정 가능)
        available_functions = {"get_current_weather": get_current_weather}
        
        # 함수 이름 추출
        function_name = response_message["function_call"]["name"]
        
        # 호출할 함수 선택
        function_to_call = available_functions[function_name]
        
        # 함수 호출을 위한 인수 추출
        function_args = json.loads(response_message["function_call"]["arguments"])
        
        # 함수 호출 및 반환 결과 받기
        function_response = function_to_call(
            location=function_args.get("location"), # 인수 지정
            unit=function_args.get("unit")
        )
        print("[호출한 함수의 응답 결과]\n", function_response)
        
        # 4단계: 함수 호출 결과를 기존 메시지에 추가하고,
        #        Chat Completions API 모델로 보내 응답받기
        
        # 함수 호출 결과를 기존 메시지에 추가히기
        messages.append(response_message) # 기존 messages에 조력자 응답 추가
        messages.append(                  # 함수와 함수 호출 결과 추가
            {
                "role": "function",       # roll: function으로 지정 
                "name": function_name,    # name: 호출할 함수 이름 지정
                "content": function_response, # content: 함수 호출 결과 지정
            }
        )
        # 함수 호출 결과를 추가한 메시지를 Chat Completions API 모델로 보내 응답받기
        second_response = openai.ChatCompletion.create(
            # model="get-3.5-turbo",
            model="gpt-3.5-turbo",
            messages=messages,
        )
        return second_response # 두 번째 응답 반환
    
    return response_message # 응답 메시지 반환

def get_current_weather(location, unit="섭씨"):
    
    reg = re.compile(r'[a-zA-Z]') # 영어 입력인지를 검사하는 정규식
    
    if reg.match(location): # 영어로 도시 이름을 지정한 경우
        city = location # 영어 도시 이름을 바로 지정
    else: # 영어로 지정하지 않은 경우
        city_names = {"서울": "Seoul", "인천": "Incheon", "대전": "Daejeon",
                      "대구": "Daegu", "부산": "Busan", "광주": "Gwangju",
                      "수원": "Suwon", "파리": "Paris", "뉴욕": "New York"}
        city = city_names[location] # 한글 도시 이름을 영어로 변경
        
    WEATHER_API_KEY = os.environ["WEATHER_API_KEY"] # API 키 지정
    
    url = "http://api.weatherapi.com/v1/current.json"
    parameters = {"key":WEATHER_API_KEY, "q":city}
    
    r = requests.get(url, params=parameters)
    current_weather = r.json()
    
    name = current_weather['location']['name'] # 설정 지역
    localtime = current_weather['location']['localtime'] # 날짜 및 시각
    temp_c = current_weather['current']['temp_c'] # 섭씨온도
    temp_f = current_weather['current']['temp_f'] # 화씨온도
    condition_text = current_weather['current']['condition']['text'] # 날씨 상태
    
    # unit 지정에 따라서 섭씨온도 혹은 화씨온도를 지정
    if unit == "섭씨":
        temp = temp_c
    elif unit == "화씨":
        temp = temp_f
    else:
        unit == "섭씨"
        temp = temp_c
        
        
    weather_info = {
        "location": name,
        "temperature": temp,
        "unit": unit,
        "current weather": condition_text,
        "local time": localtime
    }
    
    return json.dumps(weather_info, ensure_ascii=False) # JSON 형식으로 반환

# Streamlit 애플리케이션 시작
st.title("날씨 정보 알리미")

# 사용자 입력 받기
user_input = st.text_input("날씨에 대해 물어보세요.")

# 사용자 입력에 따라 응답 생성
if user_input:
    response = run_conversation(user_input)
    if isinstance(response, dict) and "content" in response:
        st.write(response["content"]) # 필요한 응답만 표시
    else:
        st.write(response) # 응답 표시
