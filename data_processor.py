import pandas as pd
import json
import re
from datetime import datetime, timedelta

def parse_time_slot(hour_str):
    """Convert hour number to actual time"""
    time_mapping = {
        '1': '8:00-8:50',
        '2': '9:00-9:50', 
        '3': '10:00-10:50',
        '4': '11:00-11:50',
        '5': '12:00-12:50',
        '6': '1:00-1:50',
        '7': '2:00-2:50',
        '8': '3:00-3:50',
        '9': '4:00-4:50',
        '10': '5:00-5:50'
    }
    
    if not hour_str or pd.isna(hour_str):
        return []
    
    hour_str = str(hour_str).strip()
    times = []
    
    # Handle single hours and hour ranges
    for hour in hour_str.split():
        if hour in time_mapping:
            times.append(time_mapping[hour])
        elif len(hour) > 1:  # Handle combined hours like "78", "89", "910"
            for i, char in enumerate(hour):
                if char in time_mapping:
                    times.append(time_mapping[char])
    
    return times

def parse_days(day_str):
    """Convert day abbreviations to full day names"""
    day_mapping = {
        'M': 'Monday',
        'T': 'Tuesday', 
        'W': 'Wednesday',
        'Th': 'Thursday',
        'F': 'Friday',
        'S': 'Saturday'
    }
    
    if not day_str or pd.isna(day_str):
        return []
    
    day_str = str(day_str).strip()
    days = []
    
    # Handle "Th" first to avoid confusion with "T"
    if 'Th' in day_str:
        days.append('Thursday')
        day_str = day_str.replace('Th', '')
    
    # Handle other days
    for char in day_str.split():
        if char in day_mapping:
            days.append(day_mapping[char])
    
    return days

def clean_instructor_name(name):
    """Clean and standardize instructor names"""
    if not name or pd.isna(name):
        return ""
    
    name = str(name).strip()
    # Remove extra whitespace and newlines
    name = re.sub(r'\s+', ' ', name)
    # Convert to title case for consistency
    return name.title()

def process_csv_data(csv_file_path):
    """Process the CSV file and convert to structured format"""
    
    # Read CSV file
    df = pd.read_csv(csv_file_path, encoding='utf-8')
    
    # Clean column names
    df.columns = df.columns.str.strip()
    
    # Initialize the structured data
    professors = {}
    courses = {}
    
    current_course_code = None
    current_course_title = None
    
    for index, row in df.iterrows():
        # Skip header rows and empty rows
        if pd.isna(row.iloc[0]) or str(row.iloc[0]).startswith('COMP CODE'):
            continue
            
        comp_code = row.iloc[0] if not pd.isna(row.iloc[0]) else current_course_code
        course_no = row.iloc[1] if not pd.isna(row.iloc[1]) else None
        course_title = row.iloc[2] if not pd.isna(row.iloc[2]) else current_course_title
        
        # Update current course info
        if not pd.isna(row.iloc[0]):
            current_course_code = comp_code
        if not pd.isna(row.iloc[2]):
            current_course_title = course_title
            
        section = row.iloc[6] if not pd.isna(row.iloc[6]) else None
        instructor = clean_instructor_name(row.iloc[7])
        room = row.iloc[8] if not pd.isna(row.iloc[8]) else None
        days = parse_days(row.iloc[9])
        hours = parse_time_slot(row.iloc[10])
        
        if not instructor or instructor == "":
            continue
            
        # Create course entry
        course_key = f"{comp_code}_{section}" if section else str(comp_code)
        if course_key not in courses:
            courses[course_key] = {
                'course_code': str(comp_code),
                'course_number': str(course_no) if course_no else "",
                'course_title': str(current_course_title) if current_course_title else "",
                'section': str(section) if section else "",
                'room': str(room) if room else "",
                'days': days,
                'time_slots': hours,
                'instructors': []
            }
        
        # Add instructor to course
        if instructor not in courses[course_key]['instructors']:
            courses[course_key]['instructors'].append(instructor)
        
        # Create/update professor entry
        if instructor not in professors:
            professors[instructor] = {
                'name': instructor,
                'current_classes': [],
                'schedule': {}
            }
        
        # Add class to professor's schedule
        class_info = {
            'course_code': str(comp_code),
            'course_number': str(course_no) if course_no else "",
            'course_title': str(current_course_title) if current_course_title else "",
            'section': str(section) if section else "",
            'room': str(room) if room else "",
            'days': days,
            'time_slots': hours
        }
        
        professors[instructor]['current_classes'].append(class_info)
        
        # Add to daily schedule
        for day in days:
            if day not in professors[instructor]['schedule']:
                professors[instructor]['schedule'][day] = []
            
            for time_slot in hours:
                schedule_entry = {
                    'time': time_slot,
                    'course_code': str(comp_code),
                    'course_title': str(current_course_title) if current_course_title else "",
                    'section': str(section) if section else "",
                    'room': str(room) if room else ""
                }
                professors[instructor]['schedule'][day].append(schedule_entry)
    
    # Sort schedules by time
    for prof_name in professors:
        for day in professors[prof_name]['schedule']:
            professors[prof_name]['schedule'][day].sort(
                key=lambda x: int(x['time'].split(':')[0]) if ':' in x['time'] else 0
            )
    
    return professors, courses

def save_data(professors, courses, output_file='structured_data.json'):
    """Save the structured data to JSON file"""
    data = {
        'professors': professors,
        'courses': courses,
        'last_updated': datetime.now().isoformat()
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {output_file}")
    print(f"Total professors: {len(professors)}")
    print(f"Total courses: {len(courses)}")

if __name__ == "__main__":
    # Process the CSV file
    csv_file = "Data (1).csv"
    professors, courses = process_csv_data(csv_file)
    
    # Save structured data
    save_data(professors, courses)
    
    # Print sample data
    print("\nSample Professor Data:")
    for i, (prof_name, prof_data) in enumerate(professors.items()):
        if i < 3:  # Show first 3 professors
            print(f"\nProfessor: {prof_name}")
            print(f"Number of classes: {len(prof_data['current_classes'])}")
            if prof_data['schedule']:
                for day, classes in prof_data['schedule'].items():
                    if classes:
                        print(f"  {day}: {len(classes)} classes")