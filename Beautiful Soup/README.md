# Resume Skills Web Scraper

A comprehensive tool to scrape your resume webpage from AWS S3 and extract the skills section along with other resume data.

## 📋 Features

- ✅ Fetches resume webpage from AWS S3 (or any URL)
- ✅ Extracts skills using multiple intelligent strategies
- ✅ Extracts all sections from your resume
- ✅ Saves skills to CSV format
- ✅ Saves complete resume data to JSON format
- ✅ Handles various HTML structures automatically

## 🚀 Quick Start

### 1. Install Required Libraries

```powershell
pip install -r requirements.txt
```

Or install individually:
```powershell
pip install beautifulsoup4 requests pandas lxml
```

### 2. Update Your Resume URL

Edit the `resume_scraper.py` file and replace the URL with your S3 bucket URL:

```python
resume_url = "YOUR_S3_BUCKET_URL_HERE"
```

Example:
```python
resume_url = "https://your-bucket.s3.amazonaws.com/resume.html"
```

### 3. Run the Scraper

**Option A: Using the Python Script**
```powershell
cd "C:\Users\Jainh\OneDrive\Desktop\FinTech\Beautiful Soup"
python resume_scraper.py
```

**Option B: Using the Jupyter Notebook**
```powershell
jupyter notebook "Beautiful soup 1st.ipynb"
```

Then update the `resume_url` variable in the notebook and run all cells.

## 📊 Output Files

The scraper will generate:

1. **extracted_skills.csv** - Contains all extracted skills in CSV format
   - Columns: `Skill_Number`, `Skill`

2. **resume_data.json** - Contains complete resume data in JSON format
   - Includes: URL, extraction date, skills, and all sections

## 🔍 How It Works

The scraper uses three intelligent strategies to find skills:

### Strategy 1: ID/Class Matching
Searches for HTML elements with 'skill' in their id or class attributes.

### Strategy 2: Heading-Based Search
Looks for headings (h1-h6) containing keywords like 'skill', 'technical', or 'expertise', then extracts content below them.

### Strategy 3: Comprehensive List Search
Searches all lists (ul, ol) and checks if they're under skills-related headings.

## 💡 Usage Examples

### Basic Usage
```python
from resume_scraper import ResumeSkillsScraper

# Create scraper
scraper = ResumeSkillsScraper("YOUR_S3_URL")

# Fetch and extract
scraper.fetch_webpage()
skills = scraper.extract_skills()

# Display results
scraper.display_skills()

# Save to CSV
scraper.save_to_csv('my_skills.csv')
```

### Extract All Sections
```python
scraper.extract_all_sections()
scraper.display_all_sections()
scraper.save_to_json('complete_resume.json')
```

### Get Skills as List
```python
skills_list = scraper.skills
print(skills_list)
```

## 🛠️ Customization

### Add Custom Keywords
Edit the scraper to search for additional keywords:

```python
if any(keyword in context for keyword in ['skill', 'technical', 'expertise', 'tools', 'technologies']):
    # Extract skills
```

### Change Output Format
Modify the `save_to_csv()` or `save_to_json()` methods to customize output format.

## 📝 Example Output

### Console Output
```
====================================
🚀 Resume Skills Web Scraper
====================================
Fetching webpage from: https://...
✓ Successfully fetched webpage
  Status Code: 200
  Content Length: 15234 bytes

====================================
🔎 EXTRACTING SKILLS...
====================================
🔍 Strategy 1: Searching by ID/Class...
  ✓ Found skills section!

====================================
📋 EXTRACTED SKILLS
====================================
 1. Python
 2. JavaScript
 3. Web Scraping
 4. Data Analysis
 5. Machine Learning
...

✓ Total skills found: 15
====================================

✓ Skills saved to: extracted_skills.csv
✓ Complete resume data saved to: resume_data.json
```

## ❓ Troubleshooting

### No Skills Found?

1. **Check URL**: Ensure your S3 bucket URL is accessible
2. **Inspect HTML**: View the HTML structure of your resume
3. **Manual Extraction**: Use the HTML preview to identify skill section structure
4. **Customize**: Modify the extraction strategies to match your HTML structure

### View HTML Structure
```python
scraper = ResumeSkillsScraper("YOUR_URL")
scraper.fetch_webpage()
print(scraper.get_html_preview(2000))
```

## 📌 Notes

- Ensure your S3 bucket has proper CORS configuration for web scraping
- Make sure your resume webpage is publicly accessible (or use appropriate authentication)
- The scraper works with any HTML resume webpage, not just S3-hosted ones

## 🔗 Your Resume URL

Current URL configured: `http://hardik-jain-1837.s3-website-us-east-1.amazonaws.com/`

Update this in:
- `resume_scraper.py` (line 242)
- `Beautiful soup 1st.ipynb` (cell 2)

## 📦 Required Libraries

- **beautifulsoup4**: HTML parsing
- **requests**: HTTP requests
- **pandas**: Data manipulation and CSV export
- **lxml**: HTML parser backend (optional but recommended)

## 🎯 Next Steps

1. Install requirements: `pip install -r requirements.txt`
2. Update your S3 URL in the script
3. Run the scraper: `python resume_scraper.py`
4. Check the generated CSV and JSON files

Happy Scraping! 🎉

