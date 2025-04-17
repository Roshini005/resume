import re

# Function to analyze the resume text and generate pros and cons
def analyze_resume(resume_text):
    # Define keywords for pros and cons
    pros_keywords = [
        "experience", "expertise", "certified", "award", "achievement",
        "skilled", "proficient", "leadership", "success", "published",
        "developed", "innovative", "quick learner", "strong foundation",
        "proficient", "experienced", "knowledgeable", "passionate"
    ]
    
    cons_keywords = [
        "gap", "unemployed", "lack", "missing", "limited", "incomplete",
        "absence", "insufficient", "no experience", "not proficient",
        "challenges", "difficulties", "struggled", "weakness"
    ]
    
    # Split the resume text into sentences for analysis
    sentences = re.split(r'[.!?]', resume_text)
    sentences = [sentence.strip() for sentence in sentences if sentence.strip()]
    
    # Initialize pros and cons lists
    pros = []
    cons = []
    
    # Analyze each sentence
    for sentence in sentences:
        # Check for pros
        for keyword in pros_keywords:
            if re.search(rf'\b{keyword}\b', sentence, re.IGNORECASE):
                pros.append(sentence)
                break
        
        # Check for cons
        for keyword in cons_keywords:
            if re.search(rf'\b{keyword}\b', sentence, re.IGNORECASE):
                cons.append(sentence)
                break
    
    return pros, cons


# Function to format and display the output
def display_analysis(pros, cons):
    print(f"{'Question':<50} {'Pros and Cons':<100}")
    print("-" * 150)
    
    # Display pros
    if pros:
        print(f"{'What are the strengths?':<50} {'; '.join(pros):<100}")
    else:
        print(f"{'What are the strengths?':<50} {'No strengths identified.':<100}")
    
    # Display cons
    if cons:
        print(f"{'What are the weaknesses?':<50} {'; '.join(cons):<100}")
    else:
        print(f"{'What are the weaknesses?':<50} {'No weaknesses identified.':<100}")


# Main function
if __name__ == "__main__":
    # Prompt user to input resume text
    print("Please paste the resume text below (type 'END' on a new line when finished):")
    resume_lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        resume_lines.append(line)
    
    # Combine all lines into a single string
    resume_text = "\n".join(resume_lines)
    
    # Analyze the resume text
    pros, cons = analyze_resume(resume_text)
    
    # Display the analysis
    display_analysis(pros, cons)
