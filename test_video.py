
import streamlit as st

from modules.answer_evaluator import evaluate_answer
from services.speech_service import transcribe_audio
from streamlit_webrtc import webrtc_streamer, WebRtcMode


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide"
)


# ==========================================
# 2. APPLICATION HEADING
# ==========================================

st.title("AI Mock Interview Simulator")
st.subheader("Live Video Interview")

st.write(
    "Welcome! Start your mock interview, "
    "record your answers and receive AI feedback."
)


# ==========================================
# 3. SESSION STATE INITIALIZATION
# ==========================================

if "transcript" not in st.session_state:
    st.session_state.transcript = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = ""


# ==========================================
# 4. CANDIDATE INFORMATION
# ==========================================

candidate_name = st.text_input("Enter your name")


# ==========================================
# 5. INTERVIEW QUESTION AND JOB ROLE
# ==========================================

st.subheader("Interview Question")

interview_question = st.text_input(
    "Enter the question asked by the AI interviewer",
    value="Tell me about yourself."
)

job_role = st.selectbox(
    "Select Job Role",
    [
        "Java Developer",
        "Python Developer",
        "Data Analyst",
        "QA Automation Engineer",
        "SQL Developer"
    ]
)


# ==========================================
# 6. LIVE WEBCAM AND MICROPHONE
# ==========================================

st.subheader("Live Camera")

webrtc_streamer(
    key="candidate-camera",
    mode=WebRtcMode.SENDRECV,
    media_stream_constraints={
        "video": True,
        "audio": True
    },
    async_processing=True
)


# ==========================================
# 7. VOICE RECORDING
# ==========================================

st.subheader("Record Your Interview Answer")

audio_value = st.audio_input(
    "Click to record your answer"
)


# ==========================================
# 8. SPEECH-TO-TEXT CONVERSION
# ==========================================

if audio_value is not None:

    st.success("Your answer has been recorded!")

    st.audio(audio_value)

    st.write(
        "Audio MIME type:",
        audio_value.type
    )

    st.write(
        "Recording size:",
        len(audio_value.getvalue()),
        "bytes"
    )

    if st.button("Convert My Answer to Text"):

        with st.spinner(
            "Gemini is transcribing your answer..."
        ):

            audio_bytes = audio_value.getvalue()

            transcript = transcribe_audio(audio_bytes)

            if (
                transcript
                and not transcript.startswith("Transcription Error:")
            ):

                st.session_state.transcript = transcript

                # Clear previous evaluation
                st.session_state.evaluation = ""

                st.success("Transcription completed!")

            else:

                st.error(transcript)


# ==========================================
# 9. DISPLAY TRANSCRIBED ANSWER
# ==========================================

if st.session_state.transcript:

    st.subheader("Your Spoken Answer")

    st.write(st.session_state.transcript)


    # ======================================
    # 10. AI ANSWER EVALUATION
    # ======================================

    if st.button("Evaluate My Answer"):

        with st.spinner(
            "AI is evaluating your answer..."
        ):

            result = evaluate_answer(
                interview_question,
                st.session_state.transcript,
                job_role
            )

            st.session_state.evaluation = result


    # ======================================
    # 11. DISPLAY EVALUATION RESULTS
    # ======================================

    if st.session_state.evaluation:

        st.subheader("AI Interview Evaluation")

        st.markdown(
            st.session_state.evaluation
        )


# ==========================================
# 12. INSTRUCTIONS
# ==========================================

st.info(
    "Your camera and microphone will be used "
    "for the mock interview."
)


# ==========================================
# 13. WELCOME MESSAGE
# ==========================================

if candidate_name:

    st.success(
        f"Welcome, {candidate_name}!"
    )
