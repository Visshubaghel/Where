#!/usr/bin/env python3
"""
Comprehensive Data Processor for BITS Pilani Timetable
Extracts ALL types of classes (Lecture L, Tutorial T, Practical P) from CSV data
Uses pandas for robust data processing
"""

import pandas as pd
import json
import re
from collections import defaultdict

# Hour to time mapping based on the CSV data analysis
HOUR_MAPPING = {
    1: "8:00-8:50",
    2: "9:00-9:50", 
    3: "10:00-10:50",
    4: "11:00-11:50",
    5: "12:00-12:50",
    6: "1:00-1:50",
    7: "2:00-2:50",
    8: "3:00-3:50",
    9: "4:00-4:50",
    10: "5:00-5:50",  # This is the tutorial time you mentioned!
    11: "6:00-6:50",
    12: "7:00-7:50",
    67: "2:00-4:50"  # Lab sessions are longer
}

# Day abbreviations mapping
DAY_MAPPING = {
    'M': 'Monday',
    'T': 'Tuesday', 
    'W': 'Wednesday',
    'Th': 'Thursday',
    'F': 'Friday',
    'S': 'Saturday'
}

def clean_text(text):
    """Clean and standardize text data"""
    if pd.isna(text) or text == '':
        return ""
    return str(text).strip().replace('\n', ' ').replace('\r', ' ')

def parse_days(day_str):
    """Parse day string into list of full day names"""
    if pd.isna(day_str) or day_str == '':
        return []
    
    day_str = str(day_str).strip()
    days = []
    
    # Handle special case for "T Th" (Tuesday Thursday)
    if 'T Th' in day_str:
        days.extend(['Tuesday', 'Thursday'])
        day_str = day_str.replace('T Th', '')
    
    # Handle "Th" before "T" to avoid confusion
    if 'Th' in day_str:
        days.append('Thursday')
        day_str = day_str.replace('Th', '')
    
    # Handle remaining single character days
    for char in day_str:
        if char in DAY_MAPPING and DAY_MAPPING[char] not in days:
            days.append(DAY_MAPPING[char])
    
    return days

def get_time_from_hour(hour):
    """Convert hour number to time string"""
    if pd.isna(hour) or hour == '':
        return ""
    
    try:
        hour_num = int(float(hour))
        return HOUR_MAPPING.get(hour_num, f"Unknown-{hour}")
    except (ValueError, TypeError):
        return ""

def process_csv_data(csv_file_path):
    """Process the CSV file and extract all class data"""
    print(f"Reading CSV file: {csv_file_path}")
    
    # Read CSV with pandas, skipping the first row which is the title
    df = pd.read_csv(csv_file_path, encoding='utf-8', skiprows=1)
    
    # Print column names for debugging
    print(f"Column names: {list(df.columns)}")
    
    # Don't filter out rows here - we need to process continuation rows
    
    professors_data = {}
    courses_data = {}
    
    print(f"Processing {len(df)} rows of data...")
    
    current_course = None
    current_course_data = None
    
    for index, row in df.iterrows():
        # Clean the data
        comp_code = clean_text(row.get('COMP CODE', ''))
        course_no = clean_text(row.get('COURSE NO.', ''))
        course_title = clean_text(row.get('COURSE TITLE', ''))
        section = clean_text(row.get('SEC', ''))
        instructor = clean_text(row.get('INSTRUCTOR_IN_CHARGE/INSTR UCTOR', ''))
        room = clean_text(row.get('ROOM', ''))
        days_str = clean_text(row.get('DAYS', ''))
        hours = clean_text(row.get('HOUR S', ''))
        
        # If this is a new course (has comp_code)
        if comp_code and course_no and course_title:
            current_course = {
                'comp_code': comp_code,
                'course_no': course_no,
                'course_title': course_title
            }
            current_course_data = current_course
            print(f"Processing course: {course_title} ({course_no})")
        
        # Process class entry (L, T, P sections) - can be for current course or continuation row
        if section and instructor and current_course_data:
            days = parse_days(days_str)
            time_slot = get_time_from_hour(hours)
            
            # Skip if no meaningful schedule data
            if not days and not time_slot:
                continue
            
            # Create class info
            class_info = {
                'course_code': current_course_data['comp_code'],
                'course_number': current_course_data['course_no'],
                'course_title': current_course_data['course_title'],
                'section': section,
                'room': room,
                'instructor': instructor,
                'days': days,
                'time_slots': [time_slot] if time_slot else [],
                'raw_hours': hours
            }
            
            # Determine class type for logging
            class_type = 'Unknown'
            if section.startswith('L'):
                class_type = 'Lecture'
            elif section.startswith('T'):
                class_type = 'Tutorial'
            elif section.startswith('P'):
                class_type = 'Practical'
            
            print(f"  → {class_type} {section}: {instructor} on {', '.join(days)} at {time_slot}")
            
            # Add to courses data
            course_key = f"{current_course_data['comp_code']}_{section}"
            courses_data[course_key] = {
                'course_code': current_course_data['comp_code'],
                'course_number': current_course_data['course_no'],
                'course_title': current_course_data['course_title'],
                'section': section,
                'room': room,
                'days': days,
                'time_slots': [time_slot] if time_slot else [],
                'instructors': [instructor]
            }
            
            # Add to professors data
            if instructor and instructor not in professors_data:
                professors_data[instructor] = {
                    'name': instructor,
                    'current_classes': [],
                    'schedule': {
                        'Monday': [],
                        'Tuesday': [],
                        'Wednesday': [],
                        'Thursday': [],
                        'Friday': [],
                        'Saturday': [],
                        'Sunday': []
                    }
                }
            
            if instructor:
                # Add to current classes
                professors_data[instructor]['current_classes'].append(class_info)
                
                # Add to daily schedule
                for day in days:
                    if day in professors_data[instructor]['schedule']:
                        schedule_entry = {
                            'time': time_slot,
                            'course_code': current_course_data['comp_code'],
                            'course_title': current_course_data['course_title'],
                            'section': section,
                            'room': room
                        }
                        professors_data[instructor]['schedule'][day].append(schedule_entry)
    
    print(f"Processed {len(professors_data)} professors")
    print(f"Processed {len(courses_data)} course sections")
    
    # Create final structured data
    structured_data = {
        'professors': professors_data,
        'courses': courses_data
    }
    
    return structured_data

def save_data(data, output_file):
    """Save processed data to JSON file"""
    print(f"Saving data to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Data saved successfully!")

def print_statistics(data):
    """Print processing statistics"""
    professors = data['professors']
    courses = data['courses']
    
    print("\n" + "="*50)
    print("PROCESSING STATISTICS")
    print("="*50)
    print(f"Total Professors: {len(professors)}")
    print(f"Total Course Sections: {len(courses)}")
    
    # Count class types
    lecture_count = sum(1 for course in courses.values() if course['section'].startswith('L'))
    tutorial_count = sum(1 for course in courses.values() if course['section'].startswith('T'))
    practical_count = sum(1 for course in courses.values() if course['section'].startswith('P'))
    
    print(f"Lecture Classes (L): {lecture_count}")
    print(f"Tutorial Classes (T): {tutorial_count}")
    print(f"Practical Classes (P): {practical_count}")
    
    # Check for DIGITAL DESIGN specifically
    digital_design_courses = [course for course in courses.values() 
                            if 'DIGITAL DESIGN' in course['course_title']]
    
    print(f"\nDIGITAL DESIGN Sections Found: {len(digital_design_courses)}")
    for course in digital_design_courses:
        print(f"  - {course['section']}: {course['course_number']} on {', '.join(course['days'])} at {', '.join(course['time_slots'])}")
    
    print("="*50)

def main():
    """Main processing function"""
    try:
        # Process the CSV data
        csv_file = 'Data (1).csv'
        structured_data = process_csv_data(csv_file)
        
        # Print statistics
        print_statistics(structured_data)
        
        # Save to JSON file
        output_file = 'structured_data.json'
        save_data(structured_data, output_file)
        
        print(f"\n✅ Processing completed successfully!")
        print(f"📄 Input: {csv_file}")
        print(f"📊 Output: {output_file}")
        print(f"🎯 Ready for website to use comprehensive class data!")
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()