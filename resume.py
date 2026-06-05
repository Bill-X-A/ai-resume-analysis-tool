import streamlit as st
from zhipuai import ZhipuAI
import fitz

client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

st.title("📄 简历优化器")
st.write("上传你的简历，AI给出改进建议")

uploaded_file = st.file_uploader("上传简历（PDF格式）", type="pdf")

if uploaded_file:
    # 提取PDF文字
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        blocks = page.get_text("blocks")
        for block in blocks:
            text += str(block[4]) + "\n"

    st.success("简历读取成功！")
    
    if st.button("开始分析"):
        with st.spinner("AI分析中..."):
            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=[
                    {"role": "user", "content": f"""请分析以下简历，给出具体的改进建议：
                    
{text}

请从这几个角度分析：
1. 整体结构
2. 工作经历描述
3. 技能匹配度
4. 具体改进建议"""}
                ]
            )
            result = response.choices[0].message.content
            st.write(result)