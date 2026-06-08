import streamlit as st
import pandas as pd
from services.ai_engine import get_ai_response

def render_chatbot_page(df):
    st.markdown("# 🤖 AI Investment Assistant")

    # --- NEW USER GUIDE (Beginner Friendly) ---
    with st.expander("📖 New User Guide: How to use this AI"):
        st.markdown("""
        ### Welcome to your AI Copilot! 
        You don't need to be a math genius or a pro trader. Think of this AI as a **financial translator**.
        
        **What can you ask?**
        - **"Explain Bitcoin like I'm 5"** (Great for basics)
        - **"Is it a good time to buy SOL?"** (AI analyzes the charts for you)
        - **"What is my portfolio risk?"** (AI looks at your current balance)
        """)
        
        st.info("💡 **Pro Tip:** The more specific you are, the better the answer. Instead of 'Buy BTC?', try 'Is BTC a good long-term hold given its current volatility?'")

    st.markdown("---")

    # --- AI COMMAND CENTER ---
    col_chat, col_tools = st.columns([3, 1])

    with col_tools:
        st.markdown("### ⚡ Quick Actions")
        if st.button("📈 Analyze Trends", use_container_width=True):
            st.session_state.ai_input = "Analyze the top 3 coins for me."
        if st.button("🛡️ Check My Risk", use_container_width=True):
            st.session_state.ai_input = "Based on my data, is my risk too high?"
        if st.button("🔮 7-Day Forecast", use_container_width=True):
            st.session_state.ai_input = "Predict the price of BTC for next week."

    with col_chat:
        st.markdown("### 💬 Chat with AI")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input
        prompt = st.chat_input("Ask me anything about your portfolio...")
        
        # Trigger from Quick Actions or Chat Input
        input_text = prompt or st.session_state.get('ai_input')

        if input_text:
            # Clear the quick action buffer
            if 'ai_input' in st.session_state:
                st.session_state.ai_input = None
                
            with st.chat_message("user"):
                st.markdown(input_text)
            st.session_state.messages.append({"role": "user", "content": input_text})

            with st.chat_message("assistant"):
                # Pass the dataframe 'df' so the AI knows your specific data
                response = get_ai_response(input_text, df)
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # --- BEGINNER'S DICTIONARY ---
    st.markdown("---")
    st.subheader("📚 Beginner's Crypto Dictionary")
    cols = st.columns(3)
    cols[0].help("**Bull Market:** When prices are going up like a rocket! 🚀")
    cols[0].markdown("**Bull Market**")
    
    cols[1].help("**Bear Market:** When prices are hibernating and going down. 🐻")
    cols[1].markdown("**Bear Market**")
    
    cols[2].help("**HODL:** Hold On for Dear Life. It means don't sell! 💎")
    cols[2].markdown("**HODL**")
