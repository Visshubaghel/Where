#!/usr/bin/env python3
"""
Test script to verify Vercel deployment readiness
"""

import os
import json
import sys
from api.index import app

def test_vercel_deployment():
    """Test the Vercel-ready application"""
    
    print("🧪 Testing Vercel deployment readiness...\n")
    
    # Test 1: Check if all required files exist
    required_files = [
        'vercel.json',
        'requirements.txt', 
        'api/index.py',
        'templates/index.html',
        'templates/professor.html',
        'structured_data.json'
    ]
    
    print("📁 Checking required files:")
    all_files_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING!")
            all_files_exist = False
    
    if not all_files_exist:
        print("\n❌ Some required files are missing!")
        return False
    
    # Test 2: Verify data loading
    print("\n📊 Testing data loading:")
    try:
        with open('structured_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        professors = data.get('professors', {})
        courses = data.get('courses', {})
        
        if len(professors) > 0 and len(courses) > 0:
            print(f"  ✅ Data loaded: {len(professors)} professors, {len(courses)} courses")
        else:
            print("  ❌ Data appears to be empty!")
            return False
            
    except Exception as e:
        print(f"  ❌ Error loading data: {e}")
        return False
    
    # Test 3: Test Flask app initialization
    print("\n🌐 Testing Flask app:")
    try:
        with app.test_client() as client:
            # Test main page
            response = client.get('/')
            if response.status_code == 200:
                print("  ✅ Main page loads successfully")
            else:
                print(f"  ❌ Main page failed: {response.status_code}")
                return False
            
            # Test API endpoint
            response = client.get('/api/search_professors?q=test')
            if response.status_code == 200:
                print("  ✅ API endpoint responds successfully")
            else:
                print(f"  ❌ API endpoint failed: {response.status_code}")
                return False
            
            # Test with actual professor
            if professors:
                first_prof = list(professors.keys())[0]
                response = client.get(f'/api/professor_info/{first_prof}')
                if response.status_code == 200:
                    print("  ✅ Professor info API works")
                else:
                    print(f"  ❌ Professor info API failed: {response.status_code}")
                    return False
    
    except Exception as e:
        print(f"  ❌ Flask app test failed: {e}")
        return False
    
    # Test 4: Verify Vercel configuration
    print("\n⚙️ Testing Vercel configuration:")
    try:
        with open('vercel.json', 'r') as f:
            vercel_config = json.load(f)
        
        if 'builds' in vercel_config and 'routes' in vercel_config:
            print("  ✅ Vercel.json is properly configured")
        else:
            print("  ❌ Vercel.json missing required sections")
            return False
            
    except Exception as e:
        print(f"  ❌ Vercel config test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Your app is ready for Vercel deployment.")
    print("\n📋 Deployment summary:")
    print(f"  • Professors: {len(professors)}")
    print(f"  • Courses: {len(courses)}")
    print(f"  • App size: Ready for serverless")
    print(f"  • Configuration: Complete")
    
    print("\n🚀 Ready to deploy with:")
    print("  vercel --prod")
    
    return True

if __name__ == "__main__":
    success = test_vercel_deployment()
    sys.exit(0 if success else 1)