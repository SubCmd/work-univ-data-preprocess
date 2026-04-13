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

# =========================
# 1단계 : 동일 데이터 찾기 (print)
# 기준 컬럼: 대학명, 전형유형, 계열, 학과명
# =========================
dup_cols = ["대학명", "전형유형", "계열", "학과명"]

duplicate_rows = df[df.duplicated(subset=dup_cols, keep=False)].copy()
duplicate_rows = duplicate_rows.sort_values(dup_cols + ["상위점수", "하위점수"], ascending=[True, True, True, True, False, False])

print("\n[중복 데이터 확인]")
if duplicate_rows.empty:
    print("중복 데이터 없음")
else:
    print(duplicate_rows[dup_cols + ["상위점수", "하위점수"]].to_string(index=False))

    print("\n[중복 건수 요약]")
    duplicate_summary = (
        duplicate_rows
        .groupby(dup_cols)
        .size()
        .reset_index(name="중복개수")
        .sort_values("중복개수", ascending=False)
    )
    print(duplicate_summary.to_string(index=False))

# =========================
# 2단계 : 중복 데이터 중 작은 점수 제거
# 같은 대학명/전형유형/계열/학과명 안에서
# 상위점수, 하위점수가 큰 행을 남기고 나머지 제거
# =========================
before_count = len(df)

df = (
    df.sort_values(
        by=dup_cols + ["상위점수", "하위점수"],
        ascending=[True, True, True, True, False, False]
    )
    .drop_duplicates(subset=dup_cols, keep="first")
    .reset_index(drop=True)
)

after_count = len(df)

print("\n[중복 제거 결과]")
print(f"제거 전 행 수: {before_count}")
print(f"제거 후 행 수: {after_count}")
print(f"제거된 행 수: {before_count - after_count}")

# 5. 대학명끼리 묶기
df["대학명"] = pd.Categorical(df["대학명"], categories=univ_order, ordered=True)
df = df.sort_values(["대학명", "학과명"]).reset_index(drop=True)

# 5-1. 원하는 순서 column 삭제
df = df.drop(df.columns[[6, 7]], axis=1)

# 5-2. 새 컬럼 추가
df.insert(0, "전형명", "수시")
df.insert(1, "학년도", 2027)

# 7. 저장 폴더 생성
output_dir = r"/Users/sublee/work-univ-data-preprocess/data/preprocessed"
os.makedirs(output_dir, exist_ok=True)

# 8. 파일명까지 포함해서 저장
output_path = os.path.join(output_dir, "에듀비_대학점수조정_중복제거.xlsx")
df.to_excel(output_path, index=False)

print("\n변환 완료")
print(f"저장 경로: {output_path}")

'''
python 02_sub.py
'''