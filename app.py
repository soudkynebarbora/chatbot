import streamlit as st
from llm_chains import load_normal_chain
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from streamlit_mic_recorder import mic_recorder, speech_to_text
from audio_handler import audio_to_text


def load_chain(chat_history):
    return load_normal_chain(chat_history)

def set_send_input():
    st.session_state.send_input = True
    clear_input_field()

def clear_input_field():
    st.session_state.user_question = st.session_state.user_input
    st.session_state.user_input = ""

def main():
    st.title("Walkbot")
    chat_container = st.container()


    fonts = ['Arial', 'Courier New', 'Georgia', 'Times New Roman', 'Verdana']
    selected_font = st.sidebar.selectbox("Select font", fonts)

    # Sidebar options for text size selection
    text_size = st.sidebar.slider("Select text size", 10, 50, 20)

    # Sidebar options for color selection
    colors = ['Black', 'Red', 'Green', 'Blue', 'Purple']
    selected_color = st.sidebar.selectbox("Select text color", colors)





    if "send_input" not in st.session_state:
        st.session_state.send_input = False
        st.session_state.user_question = ""


    chat_history = StreamlitChatMessageHistory(key = "history") #logs llm output in history
    llm_chain = load_chain(chat_history)
    user_input = st.text_input("Write your message here", key = "user_input", on_change=set_send_input)

    send_button_column,voice_record_column = st.columns(2)

    #with voice_recording_column:
        #voice_recording=mic_recorder(start_prompt="Start recording",stop_prompt="Stop recording", just_once=True)

    with send_button_column:  
        send_button = st.button("Send", key = "send_button")

    with voice_record_column:
        voice_recording_text = speech_to_text(
        language='en',
        start_prompt="Start recording",
        stop_prompt="Stop recording",
        just_once=True,
        use_container_width=False)

    if voice_recording_text:
        llm_chain.run(voice_recording_text)
    
    #if voice_recording:
        #audio_text = audio_to_text(voice_recording["bytes"])
        #llm_chain.run(audio_text)

    if send_button or st.session_state.send_input:
        if st.session_state.user_question != "":
            llm_response = llm_chain.run(st.session_state.user_question)
            st.session_state.user_question = ""

    if chat_history.messages != []:
        with chat_container:
            st.write("chat history")
            for message in chat_history.messages:
                st.chat_message(message.type).write(message.content)

if __name__ == "__main__":
    main()
