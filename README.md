# WeatherAI
Weather provision service by region in Korea using AI<br>
AI를 활용한 국내 지역별 날씨 제공 서비스
<br>
<br>
<br>

# Tech Stack
<pre>
conda 23.7.4
jupyter notebook 6.5.4
OpenAI Chat completions API
Weather API
</pre>
<br>
<br>
<br>

# Display
### 기본 화면 구성
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/8f2517c9-cb33-422c-8ceb-68c9f45be5c9)
<br>
<br>

### 천안 날씨에 대한 정보 출력
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/5e4f2ef0-fbda-4c06-b555-0fb9980d18e3)
<br>
<br>

### 태안 화씨 온도에 대한 정보 출력
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/d397d24f-7671-452c-97c2-8e41cef8c2e9)
<br>
<br>
<br>

# 주요 코드
### get_current_weather 함수 (wearther API)
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/7d78624b-80e3-48fd-a88e-c0931e095c1e)
<br>
<br>


### run_conversation 함수 (OpenAI chat completions API)
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/e8a6f87b-21e1-48e9-adc2-181109e221df)
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/d99bfc8a-5d10-4355-9e9a-9487732e1065)
<br>
<br>


### streamlit 입출력
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/bfe1adb1-3011-4407-9e18-d524edd9678f)
<br>
<br>
<br>

### 대한민국 지역의 데이터.csv
### korean_city.csv
![image](https://github.com/dlwnsgur9242/WeatherAI/assets/90494150/25693f4c-4cfc-448a-8b45-7d59f63f8ce4)
<br>
<pre>
import pandas as pd

korean_cities = {
    "서울": "Seoul", "부산": "Busan", "인천": "Incheon", "대구": "Daegu", "대전": "Daejeon",
    "광주": "Gwangju", "수원": "Suwon", "울산": "Ulsan", "창원": "Changwon", "고양": "Goyang",
    "용인": "Yongin", "성남": "Seongnam", "청주": "Cheongju", "안산": "Ansan", "안양": "Anyang",
    "전주": "Jeonju", "천안": "Cheonan", "남양주": "Namyangju", "화성": "Hwaseong", "파주": "Paju",
    "평택": "Pyeongtaek", "의정부": "Uijeongbu", "시흥": "Siheung", "김해": "Gimhae", "구미": "Gumi",
    "광명": "Gwangmyeong", "김포": "Gimpo", "제주": "Jeju", "양산": "Yangsan", "나주": "Naju",
    "아산": "Asan", "익산": "Iksan", "양주": "Yangju", "동두천": "Dongducheon", "이천": "Icheon",
    "구리": "Guri", "여수": "Yeosu", "충주": "Chungju", "안동": "Andong", "김천": "Gimcheon",
    "목포": "Mokpo", "경산": "Gyeongsan", "정읍": "Jeongeup", "거제": "Geoje", "진주": "Jinju",
    "포항": "Pohang", "완주": "Wanju", "단양": "Danyang", "부여": "Buyeo", "보령": "Boryeong",
    "태안": "Taean", "당진": "Dangjin", "서산": "Seosan", "홍성": "Hongseong", "청양": "Cheongyang",
    "영덕": "Yeongdeok", "울진": "Uljin", "포천": "Pocheon", "양평": "Yangpyeong", "하남": "Hanam",
    "의왕": "Uiwang", "오산": "Osan", "하동": "Hadong", "고성": "Goseong", "영암": "Yeongam",
    "신안": "Sinan", "청송": "Cheongsong", "영월": "Yeongwol", "고창": "Gochang", "무주": "Muju",
    "화순": "Hwasun", "진안": "Jinan", "영광": "Yeonggwang", "장성": "Jangseong", "함평": "Hampyeong",
    "강진": "Gangjin", "신안": "Sinan", "담양": "Damyang", "곡성": "Gokseong", "장흥": "Jangheung",
    "해남": "Haenam", "보성": "Boseong", "고흥": "Goheung", "강화": "Ganghwa", "옹진": "Ongjin",
    "진도": "Jindo", "함안": "Haman", "고창": "Gochang", "영광": "Yeonggwang", "장성": "Jangseong",
    "함평": "Hampyeong", "강진": "Gangjin", "신안": "Sinan", "담양": "Damyang", "곡성": "Gokseong",
    "장흥": "Jangheung", "해남": "Haenam", "보성": "Boseong", "고흥": "Goheung", "강화": "Ganghwa",
    "옹진": "Ongjin", "진도": "Jindo", "함안": "Haman", "고령": "Goryeong", "성주": "Seongju",
    "의성": "Uiseong", "청송": "Cheongsong", "영양": "Yeongyang", "영덕": "Yeongdeok", "울릉": "Ulleung",
    "독도": "Dokdo", "울진": "Uljin", "상주": "Sangju", "문경": "Mungyeong", "안동": "Andong",
    "영주": "Yeongju", "예천": "Yecheon", "경주": "Gyeongju", "청도": "Cheongdo", "군위": "Gunwi",
    "의령": "Uiryeong", "청송": "Cheongsong", "영덕": "Yeongdeok", "영양": "Yeongyang", "영주": "Yeongju",
    "영천": "Yeongcheon", "예천": "Yecheon", "울릉": "Ulleung", "울진": "Uljin", "인제": "Inje",
    "정선": "Jeongseon", "철원": "Cheorwon", "태백": "Taebaek", "평창": "Pyeongchang", "홍천": "Hongcheon",
    "화천": "Hwacheon", "횡성": "Hoengseong", "강릉": "Gangneung", "동해": "Donghae", "삼척": "Samcheok",
    "속초": "Sokcho", "양구": "Yanggu", "양양": "Yangyang", "인제": "Inje", "정선": "Jeongseon",
    "철원": "Cheorwon", "태백": "Taebaek", "세종": "Sejong", "원주": "Wonju", "춘천": "Chuncheon", "천안": "Cheonan",
    "수원": "Suwon","안동": "Andong", "대구": "Daegu", "제주": "Jeju", "포항": "Pohang", "광주": "Gwangju",
    "창원": "Changwon", "평택": "Pyeongtaek", "청주": "Cheongju", "안산": "Ansan", "양산": "Yangsan",
    "서울": "Seoul", "부산": "Busan", "대전": "Daejeon", "울산": "Ulsan", "인천": "Incheon",
    "세종": "Sejong", "강릉": "Gangneung", "원주": "Wonju", "정선": "Jeongseon", "동해": "Donghae",
    "영월": "Yeongwol", "삼척": "Samcheok", "태백": "Taebaek", "속초": "Sokcho", "홍천": "Hongcheon",
    "횡성": "Hoengseong", "철원": "Cheorwon", "화천": "Hwacheon", "양구": "Yanggu", "인제": "Inje",
    "고성": "Goseong", "양양": "Yangyang", "춘천": "Chuncheon", "원주": "Wonju", "강릉": "Gangneung",
    "동해": "Donghae", "삼척": "Samcheok", "속초": "Sokcho", "홍천": "Hongcheon", "횡성": "Hoengseong",
    "영월": "Yeongwol", "정선": "Jeongseon", "철원": "Cheorwon", "화천": "Hwacheon", "양구": "Yanggu",
    "인제": "Inje", "고성": "Goseong", "양양": "Yangyang", "청양": "Cheongyang", "단양": "Danyang",
    "보은": "Boeun", "영동": "Yeongdong", "영춘": "Yeongchun", "영동": "Yeongdong", "보은": "Boeun",
    "옥천": "Okcheon", "음성": "Eumseong", "제천": "Jecheon", "증평": "Jeungpyeong", "진천": "Jincheon",
    "괴산": "Goesan", "단양": "Danyang", "보은": "Boeun", "영동": "Yeongdong", "옥천": "Okcheon",
    "음성": "Eumseong", "제천": "Jecheon", "증평": "Jeungpyeong", "진천": "Jincheon", "괴산": "Goesan",
    "대천": "Daecheon", "보령": "Boryeong", "서천": "Seocheon", "부여": "Buyeo", "금산": "Geumsan",
    "논산": "Nonsan", "당진": "Dangjin", "태안": "Taean", "예산": "Yesan", "홍성": "Hongseong",
    "청양": "Cheongyang", "공주": "Gongju", "금산": "Geumsan", "논산": "Nonsan", "당진": "Dangjin",
    "태안": "Taean", "예산": "Yesan", "홍성": "Hongseong", "청양": "Cheongyang", "공주": "Gongju",
    "부여": "Buyeo", "금산": "Geumsan", "논산": "Nonsan", "당진": "Dangjin", "태안": "Taean",
    "예산": "Yesan", "홍성": "Hongseong", "청양": "Cheongyang", "공주": "Gongju", "보령": "Boryeong",
    "대천": "Daecheon", "서천": "Seocheon", "부여": "Buyeo", "금산": "Geumsan", "논산": "Nonsan",
    "당진": "Dangjin", "태안": "Taean", "예산": "Yesan", "홍성": "Hongseong", "청양": "Cheongyang",
    "공주": "Gongju", "보령": "Boryeong", "대천": "Daecheon", "서천": "Seocheon", "연천": "Yeoncheon",
    "포천": "Pocheon", "가평": "Gapyeong"
}

# 딕셔너리를 데이터프레임으로 변환
df = pd.DataFrame(list(korean_cities.items()), columns=['한글 도시 이름', '영어 도시 이름'])

# 데이터프레임을 CSV 파일로 저장
df.to_csv('korean_citi.csv', index=False)
</pre>
