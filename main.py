import os
import numpy as np
import pandas as pd

# 1. 파일경로
file_path = r"/Users/sublee/work-univ-data-preprocess/data/raw/에듀비 서류 평가 지원 대학 샘플 (raw).xlsx"

# 2. 엑셀 읽기
df = pd.read_excel(file_path)

# 2-1. 원래 대학 등장 순서 저장
univ_order = pd.unique(df["대학명"])

# 3-1. 대학별 조정값 설정
adjustments = {
    "한양대": -0.3,
    "경희대": -0.2,
    "경기대": -0.5,
    "국민대": -0.8,
    "단국대": -0.2,
    "동덕여대": -0.3,
    "삼육대": -1,
    "성신여대": -0.2,
    "세종대": -0.3,
    "숙명여대": -0.5,
    "숭실대": -2,
    "아주대": -0.5,
    "인천대": -0.2,
    "인하대": -0.4,
    "한국공학대": -0.5,
    "한국항공대": -0.4,
    "한양대(에리카)": -0.5,
    "홍익대": -0.5,
    "고려대": -0.4,
    "연세대": -1.2,
    "이화여대": -0.5,
}

# 3-2. 특정학과 제외 설정
exclude_departments = {
    "숭실대": ["컴퓨터학부"],
    "한국공학대": ["항공운항학과"],
    "홍익대": ["건축공학과"],
}

# 4. 대학별 점수 조정
for univ, val in adjustments.items():
    excluded = exclude_departments.get(univ, [])
    mask = (df["대학명"] == univ) & (~df["학과명"].isin(excluded))

    df.loc[mask, "상위점수"] = df.loc[mask, "상위점수"] + val
    df.loc[mask, "하위점수"] = df.loc[mask, "하위점수"] + val

# 5. 대학명끼리 묶기
df["대학명"] = pd.Categorical(df["대학명"], categories=univ_order, ordered=True)
df = df.sort_values(["대학명", "학과명"]).reset_index(drop=True)

# 6. 원하는 순서 column 삭제
df = df.drop(df.columns[[6, 7]], axis=1)

# 7. 저장 폴더 생성
output_dir = r"/Users/sublee/work-univ-data-preprocess/data/preprocessed"
os.makedirs(output_dir, exist_ok=True)

# 8. 파일명까지 포함해서 저장
output_path = os.path.join(output_dir, "에듀비_대학점수조정.xlsx")
df.to_excel(output_path, index=False)

print("변환 완료")
print(f"저장 경로: {output_path}")

'''
python main.py
'''