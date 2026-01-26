import streamlit as st
import pandas as pd

df_niigata = pd.read_csv("FEH_00500209_260126084514.csv", encoding="shift-jis") # 新潟県のデータベース
df_nagano = pd.read_csv("FEH_00500209_260126103754.csv", encoding="shift-jis") # 長野県のデータベース

st.title("新潟県の農林業経営体数")

with st.sidebar:
    st.header("条件選択")
    region = st.multiselect("地域の選択",
                           df_niigata["(J315-02-2-001)新潟県地域"].unique())
    keitai = st.radio("経営体系の選択",
                         df_niigata["(J301-02-1-001)農林業経営体数"].unique())
    
df_n = df_niigata[
    (df_niigata["(J315-02-2-001)新潟県地域"].isin(region)) &
    (df_niigata["(J301-02-1-001)農林業経営体数"] == keitai)
]  # 授業と違い、2つ同時に定義

df_h = df_nagano[
    (df_nagano["(J301-02-1-001)農林業経営体数"] == keitai)
    ]

st.subheader("新潟県")
df_n.set_index("(J315-02-2-001)新潟県地域", inplace=True)
st.dataframe(df_n, width=800, height=200)

st.subheader("長野県")
df_h.set_index("(J320-02-2-001)長野県地域", inplace=True)
st.dataframe(df_h, width=800, height=200)