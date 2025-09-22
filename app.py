from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Load the structured data
with open('structured_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

professors = data['professors']
courses = data['courses']

def get_current_day():
    """Get current day name"""
    return datetime.now().strftime('%A')

def get_current_time():
    """Get current time in HH:MM format"""
    return datetime.now().strftime('%H:%M')

def is_time_in_slot(current_time, time_slot):
    """Check if current time falls within a time slot"""
    if not time_slot or '-' not in time_slot:
        return False
    
    try:
        start_time, end_time = time_slot.split('-')
        start_hour, start_min = map(int, start_time.split(':'))
        end_hour, end_min = map(int, end_time.split(':'))
        
        current_hour, current_min = map(int, current_time.split(':'))
        
        start_total_min = start_hour * 60 + start_min
        end_total_min = end_hour * 60 + end_min
        current_total_min = current_hour * 60 + current_min
        
        return start_total_min <= current_total_min <= end_total_min
    except:
        return False

def get_professor_current_location(prof_name):
    """Get professor's current location and class"""
    if prof_name not in professors:
        return None
    
    current_day = get_current_day()
    current_time = get_current_time()
    
    prof_data = professors[prof_name]
    
    # Check if professor has classes today
    if current_day not in prof_data['schedule']:
        return {
            'status': 'No classes today',
            'current_class': None,
            'location': None
        }
    
    # Find current class
    current_class = None
    for class_info in prof_data['schedule'][current_day]:
        if is_time_in_slot(current_time, class_info['time']):
            current_class = class_info
            break
    
    if current_class:
        return {
            'status': 'In class',
            'current_class': current_class,
            'location': current_class['room']
        }
    else:
        return {
            'status': 'Free/Between classes',
            'current_class': None,
            'location': 'Not in scheduled class'
        }

def get_upcoming_classes(prof_name, limit=3):
    """Get upcoming classes for today"""
    if prof_name not in professors:
        return []
    
    current_day = get_current_day()
    current_time = get_current_time()
    current_hour, current_min = map(int, current_time.split(':'))
    current_total_min = current_hour * 60 + current_min
    
    prof_data = professors[prof_name]
    
    if current_day not in prof_data['schedule']:
        return []
    
    upcoming = []
    for class_info in prof_data['schedule'][current_day]:
        if not class_info['time'] or '-' not in class_info['time']:
            continue
            
        try:
            start_time = class_info['time'].split('-')[0]
            start_hour, start_min = map(int, start_time.split(':'))
            start_total_min = start_hour * 60 + start_min
            
            if start_total_min > current_total_min:
                upcoming.append(class_info)
        except:
            continue
    
    return upcoming[:limit]

def search_professors(query):
    """Search professors by name with fuzzy matching"""
    if not query:
        return list(professors.keys())[:10]  # Return first 10 if no query
    
    query = query.lower()
    matches = []
    
    for prof_name in professors.keys():
        prof_lower = prof_name.lower()
        
        # Exact match
        if query == prof_lower:
            matches.insert(0, prof_name)
        # Starts with query
        elif prof_lower.startswith(query):
            matches.append(prof_name)
        # Contains query
        elif query in prof_lower:
            matches.append(prof_name)
        # Word-wise matching
        elif any(word.startswith(query) for word in prof_lower.split()):
            matches.append(prof_name)
    
    return matches[:10]  # Limit to 10 results

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/search_professors')
def api_search_professors():
    """API endpoint for professor search with auto-suggestions"""
    query = request.args.get('q', '').strip()
    results = search_professors(query)
    return jsonify(results)

@app.route('/api/professor_info/<prof_name>')
def api_professor_info(prof_name):
    """API endpoint for professor information"""
    if prof_name not in professors:
        return jsonify({'error': 'Professor not found'}), 404
    
    current_location = get_professor_current_location(prof_name)
    upcoming_classes = get_upcoming_classes(prof_name)
    all_classes_today = professors[prof_name]['schedule'].get(get_current_day(), [])
    
    return jsonify({
        'name': prof_name,
        'current_status': current_location,
        'upcoming_classes': upcoming_classes,
        'all_classes_today': all_classes_today,
        'current_day': get_current_day(),
        'current_time': get_current_time()
    })

@app.route('/professor/<prof_name>')
def professor_detail(prof_name):
    """Professor detail page"""
    if prof_name not in professors:
        return "Professor not found", 404
    
    current_location = get_professor_current_location(prof_name)
    upcoming_classes = get_upcoming_classes(prof_name)
    all_classes_today = professors[prof_name]['schedule'].get(get_current_day(), [])
    
    return render_template('professor.html', 
                         professor_name=prof_name,
                         current_status=current_location,
                         upcoming_classes=upcoming_classes,
                         all_classes_today=all_classes_today,
                         current_day=get_current_day(),
                         current_time=get_current_time())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)