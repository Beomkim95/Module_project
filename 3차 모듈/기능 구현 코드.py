import pymysql
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
import seaborn as sb
import numpy as np

plt.style.use('ggplot')

def Draw(df,main_category,sub_category,fig_width=10,fig_height=10, \
            bar_type='vertical', between_bar_padding=0.85,\
            within_bar_padding=0.8, config_bar=None):

    num_sub_category = len(sub_category) ## 서브 카테고리 개수
 
    fig = plt.figure(figsize=(fig_width,fig_height)) ## 캔버스 생성
    fig.set_facecolor('white') ## 캔버스 색상 지정
    ax = fig.add_subplot() ## 그림이 그려질 축을 생성
    
    colors = sb.color_palette('hls',num_sub_category) ## 막대기 색상 지정
    
    tick_label = list(df[main_category].unique()) ## 메인 카테고리 라벨 생성
    tick_number = len(tick_label) ## 메인 카테고리 눈금 개수
    
    tick_coord = np.arange(tick_number) ## 메인 카테고리안에서 첫번째 서브 카테고리 막대기가 그려지는 x좌표
 
    width = 1/num_sub_category*between_bar_padding ## 막대기 폭 지정
 
    config_tick = dict()
    config_tick['ticks'] = [t + width*(num_sub_category-1)/2 for t in tick_coord] ## 메인 카테고리 라벨 x좌표
    config_tick['labels'] = tick_label 

    config_bar = dict()
    config_bar['edgecolor'] = 'black'
    config_bar['alpha'] = 0.8

    plt.title("KOREA\'s weather")
 
    if bar_type == 'vertical': ## 수직 바 차트를 그린다.
        plt.xticks(**config_tick) ## x축 눈금 라벨 생성
 
        for i in range(num_sub_category):
            if config_bar: ## 바 차트 추가 옵션이 있는 경우
                ax.bar(tick_coord+width*i, df[sub_category[i]], \
                       width*within_bar_padding, label=sub_category[i], \
                       color=colors[i], **config_bar) ## 수직 바 차트 생성
            else:
                ax.bar(tick_coord+width*i, df[sub_category[i]], \
                       width*within_bar_padding, label=sub_category[i], \
                       color=colors[i]) ## 수직 바 차트 생성
        plt.legend() ## 범례 생성
        plt.show()

    else: ## 수평 바 차트를 그린다.
        plt.yticks(**config_tick) ## x축 눈금 라벨 생성
 
        for i in range(num_sub_category):
            if config_bar: # 바 차트 추가 옵션이 있는 경우
                ax.barh(tick_coord+width*i, df[sub_category[i]], \
                       width*within_bar_padding, label=sub_category[i], \
                        color=colors[i], **config_bar) ## 수평 바 차트 생성
            else:
                ax.barh(tick_coord+width*i, df[sub_category[i]], \
                       width*within_bar_padding, label=sub_category[i], \
                       color=colors[i]) ## 수평 바 차트 생성
        plt.legend() ## 범례 생성
        plt.title("KOREA\'s weather")
        plt.show()


def DBcon():
    global conn 
    global cur 
    conn = pymysql.connect(host='skuser47-instance.cejfit1gmmox.us-east-2.rds.amazonaws.com', user='admin', password='admin123', db='moduledb', charset='utf8', port=3306)
    cur = conn.cursor()

def DBuncon():
    conn.commit()
    conn.close()
    cur.close()


def ex1():
    DBcon()
    sql = '''SELECT city, feels_like FROM team_weather'''
    cur.execute(sql)
    data = cur.fetchall()
    res = {}
    for i in range(-1, -8, -1):
        a = []
        for c in clothes:
            if c['minT'] <= data[i][1] < c['maxT']:
                a.append(c['name'])
        res[data[i][0]] = a
    print(res)
    DBuncon()

clothes = [
    {'minT':-10, 'maxT':-5, 'type':'outer', 'name':'패딩'},
    {'minT':-10, 'maxT':-5, 'type':'bottom', 'name':'기모바지'},
    {'minT':-10, 'maxT':-5, 'type':'add', 'name':'귀마개'},
    {'minT':-5, 'maxT':0, 'type':'add', 'name':'장갑'},
    {'minT':-5, 'maxT':0, 'type':'add', 'name':'핫팩'},
    {'minT':-5, 'maxT':0, 'type':'add', 'name':'목도리'},
    {'minT':0, 'maxT':5, 'type':'top', 'name':'히트텍'},
    {'minT':0, 'maxT':5, 'type':'bottom', 'name':'니트'},
    {'minT':0, 'maxT':5, 'type':'top', 'name':'두꺼운 목폴라'},
    {'minT':5, 'maxT':9, 'type':'outer', 'name':'조끼 패딩'},
    {'minT':5, 'maxT':9, 'type':'outer', 'name':'울코트'},
    {'minT':5, 'maxT':9, 'type':'top', 'name':'기모 후드티'},
    {'minT':9, 'maxT':12, 'type':'top', 'name':'셔츠'},
    {'minT':9, 'maxT':12, 'type':'outer', 'name':'트렌치코트'},
    {'minT':9, 'maxT':12, 'type':'bottom', 'name':'청바지'},
    {'minT':12, 'maxT':17, 'type':'outer', 'name':'가죽 자켓'},
    {'minT':12, 'maxT':17, 'type':'outer', 'name':'두꺼운 가디건'},
    {'minT':12, 'maxT':17, 'type':'bottom', 'name':'면바지'},
    {'minT':17, 'maxT':20, 'type':'top', 'name':'얇은 맨투맨'},
    {'minT':17, 'maxT':20, 'type':'outer', 'name':'얇은 가디건'},
    {'minT':17, 'maxT':20, 'type':'bottom', 'name':'얇은 청바지'},
    {'minT':20, 'maxT':23, 'type':'top', 'name':'블라우스'},
    {'minT':20, 'maxT':23, 'type':'bottom', 'name':'반바지'},
    {'minT':20, 'maxT':23, 'type':'bottom', 'name':'슬랙스'},
    {'minT':23, 'maxT':28, 'type':'top', 'name':'얇은 셔츠'},
    {'minT':23, 'maxT':28, 'type':'bottom', 'name':'통 넓은 바지'},
    {'minT':23, 'maxT':28, 'type':'add', 'name':'손선풍기'},
    {'minT':28, 'maxT':40, 'type':'shoes', 'name':'샌들'},
    {'minT':28, 'maxT':40, 'type':'bottom', 'name':'짧은 반바지'},
    {'minT':28, 'maxT':40, 'type':'add', 'name':'린넨 소재 옷'},
]

def ex2():
    DBcon()
    sql = '''SELECT city, sky FROM team_weather'''
    cur.execute(sql)
    data3 = cur.fetchall()
    # print('**************************')
    # print(data3)
    # print('**************************')
    rec = {}
    for i in range(-1, -8, -1):
        b = []
        for m in music:
            if data3[i][1] == m['sky']:
                b.append(m['music'])
        rec[data3[i][0]] = b
    print(rec)
    DBuncon()

music = [
    {'sky':'Thunderstorm', 'type':'', 'music':'Electric Shock - f(x)'},
    {'sky':'Drizzle', 'type':'pop', 'music':'Rain Drop - 아이유'},
    {'sky':'Rain', 'type':'hip-hop', 'music':'비도 오고 그래서 - 헤이즈'},
    {'sky':'Rain', 'type':'R&B', 'music':'비가 오는 날엔 - 비스트'},
    {'sky':'Snow', 'type':'pop', 'music':'Must have love - SG워너비 & 브라운아이드 걸스'},
    {'sky':'Mist', 'type':'ballad', 'music':'소나기 - 아이오아이'},
    {'sky':'Smoke', 'type':'OST', 'music':'Beautiful - Crush'},
    {'sky':'Haze', 'type':'R&B', 'music':'괜찮아도 괜찮아 - 디오(EXO)'},
    {'sky':'Dust', 'type':'R&B', 'music':'이 노랠 들어요 - 케이시'},
    {'sky':'Fog', 'type':'ballad', 'music':'거리에서 - 성시경'},
    {'sky':'Sand', 'type':'ballad', 'music':'서른 밤째 - 새봄'},
    {'sky':'Ash', 'type':'dance', 'music':'불꽃놀이 - 오마이걸'},
    {'sky':'Squall', 'type':'ballad', 'music':'우산 - 윤하'},
    {'sky':'Tornado', 'type':'dance', 'music':'Hurricane Venus - 보아'},
    {'sky':'Clear', 'type':'pop', 'music':'좋은날 - 아이유'},
    {'sky':'Clear', 'type':'pop', 'music':'하루끝 - 아이유'},
    {'sky':'Clouds', 'type':'OST', 'music':'스며들기 좋은 오늘 - 백예린'}
]


# 불쾌지수가 제일 높은 시간대 알려주기 
def ex3():
    DBcon()
    sql1 = '''SELECT temp , humidity FROM team_weather'''
    cur.execute(sql1)
    data1 = list(cur.fetchall())

    temp_data = []
    humidity1 = []
     
    # print('*'*100 + "불쾌지수")

    for i in range(0,len(data1)):
        temp1 = data1[i][0]
        hum1 = data1[i][1]
        temp_data.append(temp1)
        humidity1.append(hum1)

    # print('*'*100 + "온도")   
    # print(temp_data)
    # print('*'*100 + "습도")
    # print(humidity1)

    badfill = []

    for j in range(0,len(temp_data)):
        badfill.append((9/5*temp_data[j])-(0.55*(1-(humidity1[j]/100))*(9/5*temp_data[j]-26))+32)

    # print('*'*100 + "불쾌")
    # print(max(badfill))
    idx1 = badfill.index(max(badfill))

    sql3 = 'SELECT created_at FROM team_weather'
    # print('*'*100 + '불쾌 높은 날짜')
    cur.execute(sql3)

    data2 = list(cur.fetchall()) 
    wantdata = str(data2[idx1]).split(',')[0]
    wantdata2 = wantdata.split('(')[1]

    sql4 = 'SELECT city FROM team_weather'
    # print('*'*100 + "불쾌 지수 높은 지역")
    cur.execute(sql4)
    data3 = list(cur.fetchall()) 
    # print('!'*50)
 
    wantdata3 = str(data3[idx1]).split(',')[0]
    wantdata4 = wantdata3.split('(')[1]

    print("지금 외출을 하시는 분은 참고해주세요!!")
    print(" 불쾌지수가 가장 높은 지역은 : " + wantdata4 + "\n 시간대는 : " + wantdata2 + "\n 불쾌지수는 " + str(max(badfill)) + "입니다")

# 최근 지역 온도 알려주기

    @action(detail=False, methods=['GET'])
    def newarea(self, request):

        q = request.query_params.get('q', None)
        qs = self.get_queryset().filter(city=q)

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    data = serializer.data
    max_data = []
    min_data = []
    city = []
    for i in range(-1, -8, -1):
        max_data.append(data[i][4])
        min_data.append(data[i][3])   
        city.append(data[i][1])

    return Response(city)
    return Response(max_data)
    return Response(min_data)

# 내가 살고 있는 지역 정보 알려주기
def ex5(city_name):
    DBcon()
    sql = '''SELECT city, temp, feels_like FROM team_weather'''
    cur.execute(sql)
    datap = list(cur.fetchall())

    temp_ex5 = []
    feels_like_ex5 = []
    city_ex5 = []
    for i in range(len(datap)):
        temp_ex5.append(datap[i][1])
        feels_like_ex5.append(datap[i][2])   
        city_ex5.append(datap[i][0])
    
    df_ex5 = pd.DataFrame()
    df_ex5['city'] = city_ex5
    df_ex5['temp'] = temp_ex5 
    df_ex5['feels_like'] = feels_like_ex5

    # print(df_ex5[df_ex5.city=='Seoul'])
    print(df_ex5[df_ex5.city== city_name].describe()) # 온도, 체감온도의 통계량

    df2_ex5 = df_ex5.groupby(['city'], as_index=False).mean() # 그룹별 온도

    # print(df2_ex5)

    main_category = 'city'
    sub_category = ['temp', 'feels_like']

    Draw(df2_ex5,main_category,sub_category,bar_type='horizon',between_bar_padding=0.85,within_bar_padding=0.9,config_bar=None)

# 질문 하는 내용
def quest():
    print('*' * 100)
    print('*' * 40 + '살고 있는 지역은 어디입니까?' + '*' * 40)
    print('*' * 100)

    while True:
        try:
            cmd = int(input(' 1.서울 2.부산 3.대구 4.대전 5.제주 6.인천 7.광주 8.종료 '))

        except ValueError:
            print('1 ~ 8 사이를 입력해 주세요.')
            continue

        if cmd == 1: 
            ex5(city_name = 'Seoul')

        if cmd == 2:
            ex5(city_name = 'Busan')

        if cmd == 3:
            ex5(city_name = 'Daegu')

        if cmd == 4:
            ex5(city_name = 'Daejeon')

        if cmd == 5:
            ex5(city_name = 'Jeju city')

        if cmd == 6:
            ex5(city_name = 'Incheon')        

        if cmd == 7:
            ex5(city_name = 'Gwangju')

        else:
            break

# quest()

ex1()
ex2()
ex3()
ex4()
quest()

print("끝")
