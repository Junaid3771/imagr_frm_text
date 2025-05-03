#app.py
import streamlit as st
import asyncio
from PIL import Image
from main import chat_response

async def run_chat():
    st.set_page_config(page_title="AI Image Generator", layout="centered")
    with st.sidebar:
        st.markdown("## 🧾 About This App")
        st.markdown(
            """
            Welcome to **AI Image Generator**! 🎨  
            Simply **describe a scene**, and let the AI **bring it to life visually**.
            """
        )

        st.markdown("## 🚀 How to Use")
        st.markdown(
            """
            1. ✍️ Enter a **detailed description** of a scene in the chat box below.  
            2. ⏳ Wait a few moments while your image is generated.  
            3. 🖼️ The AI-generated image will appear in the chat!
            """
        )

        st.markdown("## ⚠️ Things to Keep in Mind")
        st.markdown(
            """
            - 🧠 The model does **not remember previous messages** — it is **stateless**.
            - 🖋️ Be **as descriptive** as possible for best results.
            - 🧪 Not all prompts may generate perfect images — experiment!
            - 💡 Try using **cultural, seasonal, or imaginative details**.
            """
        )

    # Initialize message history for UI (not for model)
    if "messages" not in st.session_state:
        st.session_state["messages"] = []  # List of {role: ..., content: str or Image}

    # App header and examples
    st.markdown(
        """
        <h1 style='text-align: center; '>🎨 AI Image Generator from Text</h1>
        <p style='text-align: center; font-size: 16px;'>Describe a scene, and let AI bring it to life visually.</p>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <div style="font-size: 16px;">
            <b>📝 Try one of these ideas:</b><br><br>
            • 🪔 A bustling street market in Delhi during <i>Diwali</i><br>
            • 🛶 A village in Kerala with houseboats and coconut trees<br>
            • 👰 An Indian bride in a red lehenga under a floral mandap<br>
            • 🍲 A street vendor making <i>pani puri</i> in Mumbai<br>
            • 🏔️ Snowy Himachal mountains with a temple on the peak<br>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Show entire conversation (from session_state)
    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            if isinstance(msg["content"], Image.Image):
                st.image(msg["content"], use_container_width=True)
            else:
                st.write(msg["content"])

    # User input
    if prompt := st.chat_input("Type a scene or idea you'd like to visualize..."):
        # Store and display user input
        st.session_state["messages"].append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate and display model response (stateless)
        with st.chat_message("assistant"):
            with st.spinner("🎨 Generating your response..."):
                response_container = st.empty()
                content = []

                try:
                    async for chunk in chat_response(prompt):
                        content.append(chunk)
                        if isinstance(chunk, Image.Image):
                            response_container.image(chunk, use_container_width=True)
                        else:
                            response_container.write("".join([c for c in content if isinstance(c, str)]))
                except Exception as e:
                    response_container.error(f"Error: {e}")
                    return

                # Save all returned parts to session state
                for c in content:
                    st.session_state["messages"].append({"role": "assistant", "content": c})

                # Show stateless warning after generation
                st.markdown(" ")
                st.warning(
                    "⚠️ Each request is processed independently. Previous chats are **not remembered by the model**, "
                    "but are shown here for your reference. This helps keep the app **completely free and stateless**."
                )

if __name__ == "__main__":
    asyncio.run(run_chat())
