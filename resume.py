import streamlit as st
from zhipuai import ZhipuAI
import fitz

if "show_adjust" not in st.session_state:
    st.session_state.show_adjust = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "你是一个专门分析简历的助手。你的任务是帮助用户优化他们的简历，不要公式化改简历。"}
    ]

client = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"])

st.title("📄 简历优化器")
st.write("上传你的简历，谢鹏辉大王给出改进建议")

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
            st.session_state.chat_history.append({
    "role": "user",
    "content": f"""请分析以下简历，给出具体的改进建议：
    
{text}

请从这几个角度分析：
1. 整体结构
2. 工作经历描述
3. 技能匹配度
4. 具体改进建议"""
})

            response = client.chat.completions.create(
                model="glm-4-flash",
                messages=st.session_state.chat_history
)
            
            # 把AI回复也加入历史
            result = response.choices[0].message.content
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": result
            })
            st.write(result)
            st.session_state.show_adjust = True

if st.session_state.show_adjust:
    st.divider()
    adjust_input = st.text_input("对简历分析有什么自己的想法？", placeholder="比如：我觉得工作经历部分描述得不够具体")

    if st.button("调整建议"):
        if adjust_input:
            st.session_state.chat_history.append({
                "role": "user",
                "content":  f"请严格按照以下要求修改上面的改进建议，不要忽略任何要求：{adjust_input}"
            })
            with st.spinner("调整中..."):
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=st.session_state.chat_history
                )
                result = response.choices[0].message.content
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": result
                })
                st.write(result)
