import pandas as pd
import hashlib

# 파일 경로
file_path = "/Users/sublee/work-univ-data-preprocess/data/preprocessed/에듀비_대학점수조정_중복제거.xlsx"

# 엑셀 읽기
df = pd.read_excel(file_path)

# 문자열 정리 함수
def clean_value(x):
    if pd.isna(x):
        return ""
    # 2027.0 -> 2027 처리
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x).strip()

# 점수 표시 함수
def format_score(x):
    if pd.isna(x):
        return ""
    # 94.0 -> 94 / 94.4 -> 94.4
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return str(x)

# md5 해시 생성 대상 문자열: 전형명_학년도_대학명_학과명
def make_md5_key(row):
    base_text = "_".join([
        clean_value(row["전형명"]),
        clean_value(row["학년도"]),
        clean_value(row["대학명"]),
        clean_value(row["학과명"]),
    ])
    md5_hash = hashlib.md5(base_text.encode("utf-8")).hexdigest()
    return f"{base_text}_{md5_hash}"

# 마지막 열 문자열 생성
def make_summary_text(row):
    return (
        f"[{clean_value(row['학년도'])}학년도 {clean_value(row['전형명'])}] "
        f"{clean_value(row['대학명'])} | "
        f"{clean_value(row['전형유형'])} | "
        f"계열 : {clean_value(row['계열'])} | "
        f"학과 : {clean_value(row['학과명'])} | "
        f"상위점수 : {format_score(row['상위점수'])} | "
        f"하위점수 : {format_score(row['하위점수'])}"
    )

# 1번 column 생성
df.insert(0, "전형명_학년도_대학명_학과명_md5해시", df.apply(make_md5_key, axis=1))

# 마지막 열 생성
df["설명문"] = df.apply(make_summary_text, axis=1)

# 저장 경로
output_path = "/Users/sublee/work-univ-data-preprocess/data/preprocessed_2/에듀비_대학점수조정_중복제거_가공완료.xlsx"

# 저장
df.to_excel(output_path, index=False)

print("저장 완료:", output_path)


'''
python 03_chromadb_preprocessed.py
'''