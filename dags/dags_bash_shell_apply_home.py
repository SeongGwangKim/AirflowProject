import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse
import random
import time
import datetime


parser = argparse.ArgumentParser()
parser.add_argument('--job_base_date', type=str)

args = parser.parse_args()

job_base_date = args.job_base_date

if args.job_base_date is None:
    print("job_base_date_none")
    exit()



date_format = ('%Y%m%d %H:%M:%S')
today = datetime.datetime.strptime(job_base_date + ' 00:00:00', date_format)

###today = datetime.datetime.strptime(job_base_date +' 00:00:00',date_format)


next_month = (int)(job_base_date[:-2]) +1
last_month = (int)(job_base_date[:-2]) -1


def makeForm(pageIndex=1, beginPd=last_month, endPd=next_month):
    # request용 변수들 생성용 함수
    userAgent = 'Chrome/55.0.2883.91 Mobile Safari/537.36'
    url = 'https://www.applyhome.co.kr/ai/aia/selectAPTLttotPblancListView.do'
    headers = {'User-Agent': userAgent}
    formData = {'beginPd': beginPd,  # 검색시작 연월
                'endPd': endPd,  # 검색종료 연월
                'houseDetailSecd': "",  # 주택구분 드롭다운
                'suplyAreaCode': "",  # 공급지역 드롭다운
                'houseNm': "",  # 주택명(건설업체명) 검색창 입력내용
                'chk0': "",  # 분양/임대 체크박스
                'pageIndex': str(pageIndex),  # 페이지번호 수
                'gvPgmId': "AIA01M01"  # 청약일정 및 통계 - 분양정보/경쟁률에서 'APT'에 해당하는 코드
                }
    return url, headers, formData

df = pd.DataFrame(columns=['지역', '주택구분', '분양/임대', '주택명', '시공사', '문으처', '모집공고일', '청약기간', '당첨자발표', '비고1', '비고2'])
page = 1
i = 1
while (True):
    page += 1
    url, headers, formData = makeForm(page)
    time.sleep(random.random() + 3)  # 혹시 모를 아이피밴 방지
    data = requests.post(url, formData, headers=headers)
    bs = BeautifulSoup(data.text, 'html.parser')
    end_YN = bs.find_all('td', attrs={'class': 'list_none'})

    if len(end_YN): break

    tbody = bs.find('table', class_='tbl_st').tbody
    trs = tbody.find_all('tr')

    for tr in trs:
        value_list = []
        for td in tr.find_all('td'):
            value_list.append(td.text.strip())
        df.loc[i] = value_list
        i += 1

if not df.empty:
    df.to_csv('/nas/dpfm/test/apply_home_{}.csv'.format(job_base_date), encoding='utf-8')

