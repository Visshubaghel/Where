#!/usr/bin/env python3
"""
Deployment preparation script for Vercel
This script ensures the structured_data.json is available and optimized for deployment
"""

import json
import os
import sys

def prepare_for_deployment():
    """Prepare the application for Vercel deployment"""
    
    # Check if structured_data.json exists
    if not os.path.exists('structured_data.json'):
        print("ERROR: structured_data.json not found!")
        print("Please run 'python data_processor.py' first to generate the data file.")
        sys.exit(1)
    
    # Load and verify the data
    try:
        with open('structured_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        professors = data.get('professors', {})
        courses = data.get('courses', {})
        
        print(f"✅ Data file loaded successfully!")
        print(f"📊 Found {len(professors)} professors and {len(courses)} courses")
        
    except Exception as e:
        print(f"ERROR loading data file: {e}")
        sys.exit(1)
    
    # Optimize data for serverless (remove any large unnecessary fields)
    optimized_data = {
        'professors': professors,
        'courses': courses,
        'last_updated': data.get('last_updated', ''),
        'deployment_ready': True
    }
    
    # Save optimized version
    with open('structured_data.json', 'w', encoding='utf-8') as f:
        json.dump(optimized_data, f, separators=(',', ':'), ensure_ascii=False)
    
    print("✅ Data optimized for deployment")
    
    # Check required files
    required_files = [
        'vercel.json',
        'requirements.txt',
        'api/index.py',
        'templates/index.html',
        'templates/professor.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"ERROR: Missing required files: {missing_files}")
        sys.exit(1)
    
    print("✅ All required files present")
    
    # Create deployment info
    deployment_info = {
        "app_name": "Professor Locator",
        "version": "1.0.0",
        "deployment_date": data.get('last_updated', ''),
        "professors_count": len(professors),
        "courses_count": len(courses),
        "status": "ready_for_deployment"
    }
    
    with open('deployment_info.json', 'w') as f:
        json.dump(deployment_info, f, indent=2)
    
    print("\n🚀 Deployment preparation complete!")
    print("\nNext steps:")
    print("1. Install Vercel CLI: npm i -g vercel")
    print("2. Login to Vercel: vercel login")
    print("3. Deploy: vercel --prod")
    print("\nOr use GitHub integration:")
    print("1. Push code to GitHub repository")
    print("2. Connect repository to Vercel dashboard")
    print("3. Deploy automatically on push")

if __name__ == "__main__":
    prepare_for_deployment()