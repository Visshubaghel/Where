# Professor Locator

A modern web application for finding professors' current locations and schedules in real-time. Now optimized for GitHub Pages deployment!

## 🌟 Features

- **Real-time Professor Search**: Find any professor instantly with intelligent autocomplete
- **Current Status Tracking**: See if a professor is currently in class or free
- **Live Schedule Display**: View today's complete schedule and upcoming classes
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Modern UI**: Clean, intuitive interface with smooth animations
- **Static Website**: Runs entirely in the browser - no server required!

## 🚀 GitHub Pages Deployment

This project is now configured for easy deployment on GitHub Pages using a static website approach.

### Quick Deploy to GitHub Pages

1. **Fork or Clone this repository**
   ```bash
   git clone <your-repository-url>
   cd professor-locator
   ```

2. **Push to your GitHub repository**
   ```bash
   git add .
   git commit -m "Initial commit for GitHub Pages"
   git push origin main
   ```

3. **Enable GitHub Pages**
   - Go to your GitHub repository
   - Click on "Settings" tab
   - Scroll down to "Pages" section
   - Under "Source", select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

4. **Access your deployed website**
   - Your site will be available at: `https://yourusername.github.io/repository-name`
   - GitHub will provide the exact URL in the Pages settings

### Automatic Deployment

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that automatically deploys your site whenever you push changes to the main branch.

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Data**: JSON-based structured data
- **Deployment**: GitHub Pages with GitHub Actions
- **No Backend Required**: Fully static website

## 📁 Project Structure

```
professor-locator/
├── index.html             # Main application (static version)
├── structured_data.json   # Professor and course data
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions deployment
├── templates/             # Original Flask templates (for reference)
├── api/                   # Original Flask API (for reference)
├── app.py                # Original Flask app (for reference)
└── README.md             # This file
```
├── app.py                   # Flask web application
├── templates/
│   ├── index.html           # Main search page
│   └── professor.html       # Professor detail page
└── README.md               # This file
```

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install pandas flask datetime
   ```

2. **Process the CSV Data**:
   ```bash
   python data_processor.py
   ```
   This will create `structured_data.json` from the CSV file.

3. **Run the Web Application**:
   ```bash
   python app.py
   ```

4. **Access the Website**:
   Open your browser and go to `http://localhost:5000`

## How to Use

1. **Search for a Professor**:
   - Type the professor's name in the search box
   - Use the auto-suggest dropdown to select the correct name
   - Click "Find Professor" or press Enter

2. **View Professor Information**:
   - See current status (In class, Free, or No classes today)
   - View current location/room number
   - Check upcoming classes for the day
   - Browse complete daily schedule

## Data Format

The system processes CSV timetable data with the following columns:
- COMP CODE: Course computer code
- COURSE NO.: Course number
- COURSE TITLE: Full course name
- CREDIT: Course credits (L-P-U format)
- SEC: Section identifier
- INSTRUCTOR_IN_CHARGE/INSTRUCTOR: Professor name
- ROOM: Classroom/location
- DAYS: Days of the week (M, T, W, Th, F, S)
- HOURS: Time slots (1-10 representing different hours)

## Time Slot Mapping

- 1: 8:00-8:50
- 2: 9:00-9:50
- 3: 10:00-10:50
- 4: 11:00-11:50
- 5: 12:00-12:50
- 6: 1:00-1:50
- 7: 2:00-2:50
- 8: 3:00-3:50
- 9: 4:00-4:50
- 10: 5:00-5:50

## API Endpoints

- `GET /`: Main search page
- `GET /api/search_professors?q={query}`: Search professors with auto-suggest
- `GET /api/professor_info/{professor_name}`: Get professor information
- `GET /professor/{professor_name}`: Professor detail page

## Features Explained

### Auto-suggest Search
- Fuzzy matching for professor names
- Handles partial matches and typos
- Real-time suggestions as you type

### Current Status Detection
- Compares current time with scheduled classes
- Shows if professor is currently teaching
- Displays current classroom location

### Smart Time Handling
- Converts hour numbers to actual time ranges
- Handles combined time slots (e.g., "78" = 2:00-3:50)
- Real-time comparison with current time

## Customization

### Adding New Data
1. Replace `Data (1).csv` with your new timetable
2. Run `python data_processor.py` to regenerate the JSON
3. Restart the Flask application

### Modifying Time Slots
Edit the `parse_time_slot()` function in `data_processor.py` to match your institution's time schedule.

### Styling Changes
Modify the CSS in the HTML templates to match your institution's branding.

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Data Processing**: Pandas
- **Data Storage**: JSON files
- **Search**: Fuzzy string matching
- **Real-time Updates**: JavaScript fetch API

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Notes

- The system shows real-time information based on the current day and time
- Data is loaded from the JSON file on server startup
- For production use, consider using a proper database instead of JSON files
- The development server should not be used in production environments

## Future Enhancements

- Database integration for better performance
- User authentication and personalized schedules
- Email/SMS notifications for class reminders
- Integration with campus map systems
- Mobile app development
- Multi-semester data support