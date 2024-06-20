import streamlit as st
import pandas as pd
import math

# 데이터 불러오기
file_path = './cafe.xlsx'
cafe_data = pd.read_excel(file_path)



cafe_data['order_date'] = pd.to_datetime(cafe_data['order_date'])


# 연도와 월 컬럼 추가
cafe_data['year'] = cafe_data['order_date'].dt.year
cafe_data['month'] = cafe_data['order_date'].dt.month

st. title('카페 매출 대시보드')

# 탭 추가
tab1, tab2, tab3 = st.tabs(['제품 별 매출표', '월별 총 매출표', '총 매출'])

# 사이드바에서 연도와 제품 선택
select_year = st.sidebar.selectbox('연도 선택', map((lambda x: int(x)), filter((lambda x: not math.isnan(x)), sorted(cafe_data['year'].unique()))))
select_product = st.sidebar.selectbox('제품 선택', sorted(cafe_data['item'].unique()))

# 선택된 연도와 제품에 따라 데이터 필터링
filtered_data = cafe_data[(cafe_data['year'] == select_year) & 
                           (cafe_data['item'] == select_product)]

fd = cafe_data[(cafe_data['year'] == select_year)]

# 월별 매출 데이터 계산
monthly_sales = filtered_data.groupby('month')['price'].sum().reset_index()

with tab1:
    # 매출 표 출력
    st.write(f'{select_year}년 {select_product} 매출 데이터')
    st.write(filtered_data)

    # 막대그래프 그리기
    st.write(f'{select_year}년 {select_product} 월별 매출')
    st.bar_chart(monthly_sales.set_index('month'))

with tab2:
    # 월별 총 매출
    cafe_sales = fd.groupby('month')['price'].sum().reset_index()
    st.write(cafe_sales)
    st.write(f'{select_year}년 월별 총매출')
    st.bar_chart(cafe_sales.set_index('month'))


with tab3:
    # 총 매출
    total = cafe_data['price'].sum()
    st.title('총 매출')
    st.title(f'{total}원')



