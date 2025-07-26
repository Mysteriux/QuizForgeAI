import streamlit as st
import tempfile, os
from crew import QuizForgeAICrew
from models.quiz import QuizOutput

def initialize_session_state():
    if 'selected_answers' not in st.session_state:
        st.session_state.selected_answers = {}
    if 'show_answers' not in st.session_state:
        st.session_state.show_answers = {}
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = None
    if 'pdf_processed' not in st.session_state:
        st.session_state.pdf_processed = False

def check_answer(question_num: int):
    st.session_state.show_answers[question_num] = True

def process_pdf(pdf_path: str):
    generator = QuizForgeAICrew()
    with st.spinner("Analyzing PDF and generating quizzes..."):
        result = generator.crew().kickoff(inputs={"pdf_path": pdf_path})
        st.session_state.quiz_data = result.pydantic
        st.session_state.pdf_processed = True

def display_quiz():
    if st.session_state.quiz_data is None:
        return

    quiz_data: QuizOutput = st.session_state.quiz_data
    
    # Display each question
    for i, question in enumerate(quiz_data.questions, 1):
        st.subheader(f"Question {i}")
        st.write(question.question)
        
        if question.type == "multiple_choice":
            options = question.options
            # Initialize the answer for this question if not exists
            if i not in st.session_state.selected_answers:
                st.session_state.selected_answers[i] = None
                
            selected = st.radio(
                f"Select your answer for Question {i}",
                options,
                key=f"q{i}",
                index=None if st.session_state.selected_answers[i] is None 
                    else options.index(st.session_state.selected_answers[i])
            )
            
            # Update the selected answer in session state
            if selected is not None:
                st.session_state.selected_answers[i] = selected
            
            if st.button(f"Check Answer {i}", key=f"check_{i}", on_click=check_answer, args=(i,)):
                pass
                
            if st.session_state.show_answers.get(i, False):
                if st.session_state.selected_answers[i] == question.correct_answer:
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                st.write("**Correct Answer:**", question.correct_answer)
                st.write("**Explanation:**", question.explanation)
        
        elif question.type == "true_false":
            # Initialize the answer for this question if not exists
            if i not in st.session_state.selected_answers:
                st.session_state.selected_answers[i] = None
                
            selected = st.radio(
                f"True or False for Question {i}",
                ["True", "False"],
                key=f"q{i}",
                index=None if st.session_state.selected_answers[i] is None 
                    else ["True", "False"].index(st.session_state.selected_answers[i])
            )
            
            # Update the selected answer in session state
            if selected is not None:
                st.session_state.selected_answers[i] = selected
            
            if st.button(f"Check Answer {i}", key=f"check_{i}", on_click=check_answer, args=(i,)):
                pass
                
            if st.session_state.show_answers.get(i, False):
                if st.session_state.selected_answers[i] == question.correct_answer:
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                st.write("**Correct Answer:**", question.correct_answer)
                st.write("**Explanation:**", question.explanation)
        
        elif question.type == "short_answer":
            # Initialize the answer for this question if not exists
            if i not in st.session_state.selected_answers:
                st.session_state.selected_answers[i] = ""
                
            answer = st.text_input(
                f"Your answer for Question {i}", 
                key=f"q{i}",
                value=st.session_state.selected_answers[i]
            )
            
            # Update the answer in session state
            if answer != st.session_state.selected_answers[i]:
                st.session_state.selected_answers[i] = answer
            
            if st.button(f"Check Answer {i}", key=f"check_{i}", on_click=check_answer, args=(i,)):
                pass
                
            if st.session_state.show_answers.get(i, False):
                st.write("**Correct Answer:**", question.correct_answer)
                st.write("**Explanation:**", question.explanation)
        
        st.write("**Difficulty:**", question.difficulty)
        st.divider()

def main():
    st.title("QuizForge AI")
    st.write("Upload a chapter, let our agents craft your quiz.")

    # Initialize session state
    initialize_session_state()

    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if uploaded_file is not None and not st.session_state.pdf_processed:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            pdf_path = tmp_file.name
            print(f'found pdf path {pdf_path}')
        try:
            process_pdf(pdf_path)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
        finally:
            # Clean up the temporary file
            os.unlink(pdf_path)
    
    # Display the quiz if it exists
    if st.session_state.quiz_data is not None:
        display_quiz()

if __name__ == "__main__":
    main() 