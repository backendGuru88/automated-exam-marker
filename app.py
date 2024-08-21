import streamlit as st
from PIL import Image
import pytesseract
import cv2
import numpy as np
def pre_process_image(image):
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, thresh_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = np.ones((2, 2), np.uint8)
    dilated_image = cv2.dilate(thresh_image, kernel, iterations=1)
    return dilated_image



def extract_text_from_image(image):
    try:
        pre_processed_image = pre_process_image(image)
        text = pytesseract.image_to_string(pre_processed_image)
        st.write("Extracted Text (for debugging):")
        st.write(text)  # Debugging: Print extracted text
        return text.strip()
    except Exception as e:
        st.error(f"Error occurred during OCR: {str(e)}")
        return ""

def compare_answers(teacher_text, student_text, score_per_question, answer_separator='\n'):
    teacher_answers = teacher_text.split(answer_separator)
    student_answers = student_text.split(answer_separator)
    
    st.write("Teacher Answers List :", teacher_answers)  # Debugging
    st.write("Student Answers List :", student_answers)  # Debugging
    
    total_questions = len(teacher_answers)
    correct_answers = 0
    
    for teacher_answer, student_answer in zip(teacher_answers, student_answers):
        st.write(f"Comparing: Teacher: '{teacher_answer.strip().lower()}', Student: '{student_answer.strip().lower()}'")  # Debugging
        if teacher_answer.strip().lower() == student_answer.strip().lower():
            correct_answers += 1
            
    total_score = correct_answers * score_per_question
    return total_questions, correct_answers, total_score

st.title("Automated Exam Marker")

col1, col2 = st.columns(2)

with col1:
    st.header("Teacher Uploads")
    teacher_image = st.file_uploader("Upload Correct Answers Image", type=["png"])
    total_score_per_question = st.number_input("Score per question", min_value=1, value=1)
    answer_separator = st.text_input("Answer separator", value='\n')
    
    if teacher_image:
        teacher_img = Image.open(teacher_image)
        st.image(teacher_img, caption="Correct Answers Image", use_column_width=True)
        teacher_text = extract_text_from_image(teacher_img)
        if not teacher_text or teacher_text.startswith("Error occurred during OCR"):
            st.error("Unable to extract text from the teacher's image.")
        else:
            st.write("Extracted Text from Teacher's Image:")
            st.write(teacher_text)

with col2:
    st.header("Student Uploads")
    student_image = st.file_uploader("Upload Student's Answers Image", type=["png"])
    
    if student_image:
        student_img = Image.open(student_image)
        st.image(student_img, caption="Student's Answers Image", use_column_width=True)
        student_text = extract_text_from_image(student_img)
        if not student_text or student_text.startswith("Error occurred during OCR"):
            st.error("Unable to extract text from the student's image.")
        else:
            st.write("Extracted Text from Student's Image:")
            st.write(student_text)

if teacher_image and student_image and total_score_per_question:
    if teacher_text and student_text:
        total_questions, correct_answers, total_score = compare_answers(teacher_text, student_text, total_score_per_question, answer_separator)
        

        st.write("-----------")
        st.write("Result⬇️")
        st.write(f"Student Correct Answers: {correct_answers}")
        st.write(f"Total Score: {total_score}")





"""
https://school-project-nu.vercel.app/
"""