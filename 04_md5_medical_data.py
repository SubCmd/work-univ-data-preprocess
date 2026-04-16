import os
import pandas as pd
import hashlib

# 1. 입력 파일 경로
file_path = r"C:\Users\ST-USER\work-univ-data-preprocess\data\raw\2027학년 의치한약수 학생부종합 전형 전처리중.xlsx"

# 2. 출력 폴더 경로
output_dir = r"C:\Users\ST-USER\work-univ-data-preprocess\data\preprocessed"

# 3. 출력 파일명 설정
output_file_name = "에듀비_대학점수조정_중복제거_md5.xlsx"
output_path = os.path.join(output_dir, output_file_name)

# 4. 엑셀 읽기
df = pd.read_excel(file_path)

# 5. 값 정리 함수
def normalize_value(value):
    if pd.isna(value):
        return ""
    return str(value).strip()

# 6. 행 전체 기준 md5 생성
def make_md5(row):
    row_text = "||".join(normalize_value(v) for v in row)
    return hashlib.md5(row_text.encode("utf-8")).hexdigest()

# 7. 기존 md5_key가 있으면 제거
if "md5_key" in df.columns:
    df = df.drop(columns=["md5_key"])

# 8. 가장 앞에 md5_key 컬럼 추가
df.insert(0, "md5_key", df.apply(make_md5, axis=1))

# 9. 저장
df.to_excel(output_path, index=False, engine="openpyxl")

print("저장 완료")
print("출력 경로:", output_path)

'''
py 04_md5_medical_data.py
'''