import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df_niigata = pd.read_csv("FEH_00500209_260126084514.csv", encoding="shift-jis") # 新潟県のデータベース
df_nagano = pd.read_csv("FEH_00500209_260126103754.csv", encoding="shift-jis") # 長野県のデータベース


