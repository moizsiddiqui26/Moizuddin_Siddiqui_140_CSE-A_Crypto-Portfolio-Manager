from groq import Groq
import streamlit as st

def ask_ai(user_query, portfolio_context=""):
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
        if not api_key:
            return "⚠️ Setup Required: Please add 'GROQ_API_KEY' to your Streamlit secrets."

        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": f"You are a helpful Crypto AI Assistant. Context: {portfolio_context}"},
                {"role": "user", "content": user_query}
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"⚠️ Groq Error: {str(e)}"
