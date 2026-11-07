
import re
import streamlit as st

from modules.question_generator import generate_next_question
from modules.answer_evaluator import evaluate_answer
from services.speech_service import transcribe_audio
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from database.db_manager import (
    initialize_db,
    add_candidate,
    create_interview,
    save_question,
    save_evaluation,
    complete_interview,
    get_interview_details,
    get_recent_questions
)


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI Mock Interview",
    page_icon="🎤",
    layout="wide"
)


# ==========================================
# 2. DATABASE INITIALIZATION
# ==========================================

initialize_db()


# ==========================================
# 3. SESSION STATE INITIALIZATION
# ==========================================

defaults = {
    "transcript": "",
    "evaluation": "",
    "candidate_id": None,
    "interview_id": None,
    "question_id": None,
    "interview_active": False,
    "interview_completed": False,
    "evaluation_saved": False,
    "interview_role": None,
    "questions": [],
    "used_questions": [],
    "current_question_index": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# 4. APPLICATION HEADING
# ==========================================

st.title("AI Mock Interview Simulator")

st.subheader("Live Video Interview")

st.write(
    "Welcome! Start your mock interview, "
    "answer five AI-generated questions and receive "
    "personalized AI feedback."
)


# ==========================================
# 5. CANDIDATE INFORMATION
# ==========================================

candidate_name = st.text_input(
    "Enter your name",
    disabled=st.session_state.interview_active
)


# ==========================================
# 6. INTERVIEW CONFIGURATION
# ==========================================

st.subheader("Interview Configuration")

job_role = st.selectbox(
    "Select Job Role",
    [
        "Java Developer",
        "Python Developer",
        "Data Analyst",
        "QA Automation Engineer",
        "SQL Developer"
    ],
    disabled=st.session_state.interview_active
)

difficulty = st.selectbox(
    "Select Difficulty",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ],
    disabled=st.session_state.interview_active
)


# ==========================================
# 7. START INTERVIEW
# ==========================================

if not st.session_state.interview_active:

    if st.button("Start Interview"):

        if not candidate_name.strip():

            st.error("Please enter your name!")

        else:

            try:

                with st.spinner(
                    "Gemini is preparing your first interview question..."
                ):

                    # Retrieve questions from previous interviews
                    previous_questions = get_recent_questions(
                        job_role,
                        limit=30
                    )

                    # Generate only the first question
                    first_question = generate_next_question(
                        role=job_role,
                        difficulty=difficulty,
                        previous_questions=previous_questions,
                        question_number=1
                    )

                if not first_question:

                    st.error(
                        "Could not generate a question. "
                        "Please try again."
                    )

                else:

                    # Register candidate
                    candidate_id = add_candidate(
                        candidate_name.strip()
                    )

                    # Create interview session
                    interview_id = create_interview(
                        candidate_id,
                        job_role,
                        difficulty
                    )

                    st.session_state.candidate_id = candidate_id
                    st.session_state.interview_id = interview_id
                    st.session_state.interview_role = job_role

                    # Store the first question
                    st.session_state.questions = [first_question]

                    # Keep previous and current questions
                    st.session_state.used_questions = (
                        previous_questions + [first_question]
                    )

                    st.session_state.current_question_index = 0

                    st.session_state.transcript = ""
                    st.session_state.evaluation = ""
                    st.session_state.question_id = None

                    st.session_state.evaluation_saved = False
                    st.session_state.interview_active = True
                    st.session_state.interview_completed = False

                    st.success("Interview started successfully!")

                    st.rerun()

            except Exception as e:

                st.error(f"Interview Start Error: {str(e)}")

# ==========================================
# 8. LIVE WEBCAM AND MICROPHONE
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
# 9. DISPLAY CURRENT QUESTION
# ==========================================

if st.session_state.interview_active:

    index = st.session_state.current_question_index

    total_questions = 5

    current_question = st.session_state.questions[index]

    st.divider()

    st.subheader("Your Interview Questions")

    st.progress(
        (index + 1) / total_questions
    )

    st.caption(
        f"Question {index + 1} of {total_questions}"
    )

    st.markdown(
        f"### {current_question}"
    )


# ==========================================
# 10. VOICE RECORDING
# ==========================================

if st.session_state.interview_active:

    st.subheader("Record Your Interview Answer")

    st.info(
        """
        **How to answer interview questions:**

        1. For theoretical questions, explain your answer clearly.
        2. For coding questions, explain your logic first.
        3. Then speak your code step by step.
        4. Clearly mention programming keywords, operators,
           brackets, parentheses and semicolons.
        5. Explain the expected output and edge cases.

        You can answer all questions using your microphone.
        No typing is required.
        """
    )

    audio_value = st.audio_input(
        "Click to record your answer",
        key=f"audio_input_{st.session_state.current_question_index}"
    )

    if audio_value is not None:

        st.audio(audio_value)

        if st.button("Convert My Answer to Text"):

            try:

                with st.spinner("Gemini is transcribing your answer..."):

                    audio_bytes = audio_value.getvalue()

                    current_question = st.session_state.questions[
                        st.session_state.current_question_index
                    ]

                    transcript = transcribe_audio(
                        audio_bytes,
                        current_question
                    )

                if (
                    transcript
                    and not transcript.startswith("Transcription Error:")
                ):

                    st.session_state.transcript = transcript
                    st.session_state.evaluation = ""
                    st.session_state.evaluation_saved = False
                    st.session_state.question_id = None

                    st.success("Transcription completed!")

                else:

                    st.error(transcript)

            except Exception as e:

                st.error(f"Transcription Error: {str(e)}")
# ==========================================
# 11. DISPLAY TRANSCRIBED ANSWER
# ==========================================

if (
    st.session_state.interview_active
    and st.session_state.transcript
):

    st.subheader("Your Spoken Answer")

    st.write(st.session_state.transcript)


# ==========================================
# 12. AI ANSWER EVALUATION
# ==========================================

if (
    st.session_state.interview_active
    and st.session_state.transcript
    and not st.session_state.evaluation_saved
):

    if st.button("Evaluate My Answer"):

        try:

            with st.spinner(
                "AI is evaluating your answer..."
            ):

                index = st.session_state.current_question_index

                current_question = st.session_state.questions[index]

                # Generate AI evaluation
                result = evaluate_answer(
                    current_question,
                    st.session_state.transcript,
                    st.session_state.interview_role
                )

                if (
                    not result
                    or result.startswith("Gemini API Error:")
                    or result.startswith("Gemini is temporarily unavailable")
                ):

                    st.error(
                        "Evaluation failed. Please try again later."
                    )

                else:

                    st.session_state.evaluation = result

                    # Save question only once
                    if st.session_state.question_id is None:

                        question_id = save_question(
                            st.session_state.interview_id,
                            current_question,
                            st.session_state.transcript
                        )

                        st.session_state.question_id = question_id

                    # Extract evaluation scores
                    def extract_score(pattern, text):

                        match = re.search(
                            pattern,
                            text,
                            re.IGNORECASE
                        )

                        if match:

                            return float(match.group(1))

                        return None

                    correctness = extract_score(
                        r"Correctness Score:\s*(\d+(?:\.\d+)?)",
                        result
                    )

                    relevance = extract_score(
                        r"Relevance Score:\s*(\d+(?:\.\d+)?)",
                        result
                    )

                    completeness = extract_score(
                        r"Completeness Score:\s*(\d+(?:\.\d+)?)",
                        result
                    )

                    # Save evaluation and scores
                    save_evaluation(
                        st.session_state.question_id,
                        result,
                        correctness,
                        relevance,
                        completeness
                    )

                    st.session_state.evaluation_saved = True

                    st.success(
                        "Answer and evaluation saved successfully!"
                    )

        except Exception as e:

            st.error(
                f"Evaluation or database error: {str(e)}"
            )


# ==========================================
# 13. DISPLAY EVALUATION
# ==========================================

if st.session_state.evaluation:

    st.subheader("AI Interview Evaluation")

    st.markdown(
        st.session_state.evaluation
    )


# ==========================================
# 14. NEXT QUESTION
# ==========================================

if (
    st.session_state.interview_active
    and st.session_state.evaluation_saved
):

    current_index = st.session_state.current_question_index

    total_questions = 5

    if current_index < total_questions - 1:

        if st.button("Next Question"):

            try:

                with st.spinner(
                    "Gemini is generating your next fresh question..."
                ):

                    next_question = generate_next_question(
                        role=st.session_state.interview_role,
                        difficulty=difficulty,
                        previous_questions=st.session_state.used_questions,
                        question_number=current_index + 2
                    )

                if not next_question:

                    st.error(
                        "Could not generate a new question. "
                        "Please try again."
                    )

                else:

                    # Store the newly generated question
                    st.session_state.questions.append(next_question)

                    st.session_state.used_questions.append(next_question)

                    # Move to next question
                    st.session_state.current_question_index += 1

                    # Clear previous answer and evaluation
                    st.session_state.transcript = ""
                    st.session_state.evaluation = ""
                    st.session_state.question_id = None
                    st.session_state.evaluation_saved = False

                    st.rerun()

            except Exception as e:

                st.error(
                    f"Next Question Error: {str(e)}"
                )

    else:

        st.success(
            "You have successfully completed all five questions!"
        )

        if st.button("Complete Interview"):

            try:

                result = complete_interview(
                    st.session_state.interview_id
                )

                if result:

                    st.session_state.interview_active = False
                    st.session_state.interview_completed = True

                    st.success(
                        "Interview completed and saved successfully!"
                    )

                    st.rerun()

                else:

                    st.error("Interview record not found.")

            except Exception as e:

                st.error(
                    f"Database Error: {str(e)}"
                )

# ==========================================
# 15. FINAL INTERVIEW REPORT
# ==========================================

if st.session_state.interview_completed:

    st.divider()

    st.title("Final Interview Performance Report")

    st.success(
        "Congratulations! You have completed all five interview questions."
    )

    st.write(
        "Below is your complete AI-generated interview performance report."
    )

    # Retrieve all five question records from database
    interview_details = get_interview_details(
        st.session_state.interview_id
    )

    if interview_details:

        # Calculate average scores
        correctness_scores = [
            row[4] for row in interview_details if row[4] is not None
        ]

        relevance_scores = [
            row[5] for row in interview_details if row[5] is not None
        ]

        completeness_scores = [
            row[6] for row in interview_details if row[6] is not None
        ]

        avg_correctness = (
            sum(correctness_scores) / len(correctness_scores)
            if correctness_scores else 0
        )

        avg_relevance = (
            sum(relevance_scores) / len(relevance_scores)
            if relevance_scores else 0
        )

        avg_completeness = (
            sum(completeness_scores) / len(completeness_scores)
            if completeness_scores else 0
        )

        overall_score = (
            avg_correctness +
            avg_relevance +
            avg_completeness
        ) / 3

        # Overall performance
        st.subheader("Overall Performance")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Correctness",
            f"{avg_correctness:.2f}/10"
        )

        col2.metric(
            "Relevance",
            f"{avg_relevance:.2f}/10"
        )

        col3.metric(
            "Completeness",
            f"{avg_completeness:.2f}/10"
        )

        col4.metric(
            "Overall Score",
            f"{overall_score:.2f}/10"
        )

        st.progress(
            min(max(overall_score / 10, 0.0), 1.0)
        )

        st.divider()

        # Individual question feedback
        st.subheader("Question-wise Evaluation")

        for index, row in enumerate(interview_details, start=1):

            question_id = row[0]
            question_text = row[1]
            candidate_answer = row[2]
            evaluation = row[3]

            correctness = row[4]
            relevance = row[5]
            completeness = row[6]

            with st.expander(
                f"Question {index}: {question_text}",
                expanded=False
            ):

                st.markdown("**Your Answer:**")

                st.write(
                    candidate_answer or "No answer recorded."
                )

                st.markdown("**Individual Scores:**")

                score1, score2, score3 = st.columns(3)

                score1.metric(
                    "Correctness",
                    f"{correctness:.1f}/10"
                    if correctness is not None else "N/A"
                )

                score2.metric(
                    "Relevance",
                    f"{relevance:.1f}/10"
                    if relevance is not None else "N/A"
                )

                score3.metric(
                    "Completeness",
                    f"{completeness:.1f}/10"
                    if completeness is not None else "N/A"
                )

                st.markdown("**AI Feedback:**")

                st.markdown(
                    evaluation or "Evaluation not available."
                )

        st.divider()

        # Final AI feedback
        st.subheader("Final Interview Feedback")

        with st.spinner(
            "Gemini is preparing your overall interview feedback..."
        ):

            from services.gemini_service import generate_response

            feedback_prompt = f"""
            Act as an experienced technical interview evaluator.

            Analyze the candidate's complete five-question interview.

            Job Role: {st.session_state.interview_role}

            Average Correctness Score: {avg_correctness:.2f}/10
            Average Relevance Score: {avg_relevance:.2f}/10
            Average Completeness Score: {avg_completeness:.2f}/10
            Overall Score: {overall_score:.2f}/10

            Individual Question Evaluations:

            """

            for index, row in enumerate(interview_details, start=1):

                feedback_prompt += f"""
                Question {index}: {row[1]}

                Candidate Answer: {row[2]}

                AI Evaluation: {row[3]}

                """

            feedback_prompt += """
            Provide the final report with these sections:

            1. Overall Interview Performance
            2. Candidate Strengths
            3. Technical Knowledge Gaps
            4. Communication Skills
            5. Areas for Improvement
            6. Recommended Topics to Study
            7. Final Interviewer Verdict

            Be honest, constructive and specific.
            Do not invent information.
            """

            final_feedback = generate_response(feedback_prompt)

        if final_feedback and not final_feedback.startswith(
            ("Gemini API Error:", "Gemini is temporarily unavailable")
        ):

            st.markdown(final_feedback)

        else:

            st.warning(
                "The individual evaluations and average scores are available, "
                "but final combined AI feedback could not be generated."
            )

    else:

        st.warning(
            "No interview evaluation records were found in the database."
        )


# ==========================================
# 16. INSTRUCTIONS
# ==========================================

st.info(
    "Your camera and microphone will be used "
    "for the mock interview."
)
