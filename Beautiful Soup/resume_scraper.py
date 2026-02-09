"""
Resume Skills Web Scraper
Scrapes resume webpage from AWS S3 and extracts skills section
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
from datetime import datetime


class ResumeSkillsScraper:
    """
    A comprehensive web scraper for extracting skills from resume webpages
    """

    def __init__(self, url):
        """Initialize the scraper with resume URL"""
        self.url = url
        self.soup = None
        self.skills = []
        self.all_sections = {}

    def fetch_webpage(self):
        """Fetch the resume webpage"""
        try:
            print(f"Fetching webpage from: {self.url}")
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()

            print(f"✓ Successfully fetched webpage")
            print(f"  Status Code: {response.status_code}")
            print(f"  Content Length: {len(response.content)} bytes")

            self.soup = BeautifulSoup(response.content, 'html.parser')
            return True

        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching webpage: {e}")
            return False

    def extract_skills(self):
        """Extract skills using multiple strategies"""
        if not self.soup:
            print("Error: No webpage loaded. Call fetch_webpage() first.")
            return []

        skills = []

        # Strategy 1: Look for sections with 'skill' in id or class
        print("\n🔍 Strategy 1: Searching by ID/Class attributes...")
        skills_section = (
            self.soup.find(id=lambda x: x and 'skill' in x.lower()) or
            self.soup.find(class_=lambda x: x and 'skill' in str(x).lower()) or
            self.soup.find('section', class_=lambda x: x and 'skill' in str(x).lower()) or
            self.soup.find('div', class_=lambda x: x and 'skill' in str(x).lower())
        )

        if skills_section:
            print("  ✓ Found skills section!")

            # Extract from list items
            list_items = skills_section.find_all(['li', 'span', 'p'])
            for item in list_items:
                skill_text = item.get_text(strip=True)
                if skill_text and len(skill_text) > 0 and skill_text not in skills:
                    skills.append(skill_text)

            # If no list items, get all text
            if not skills:
                skills_text = skills_section.get_text(separator='\n', strip=True)
                skills = [line.strip() for line in skills_text.split('\n')
                         if line.strip() and line.strip().lower() != 'skills']

        # Strategy 2: Look for headings containing 'skill'
        if not skills:
            print("  ✗ No skills found")
            print("\n🔍 Strategy 2: Searching by headings...")
            headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

            for heading in headings:
                heading_text = heading.get_text().lower()
                if 'skill' in heading_text or 'technical' in heading_text or 'expertise' in heading_text:
                    print(f"  ✓ Found heading: '{heading.get_text(strip=True)}'")

                    # Get the next sibling elements
                    next_element = heading.find_next_sibling()
                    while next_element:
                        if next_element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                            break
                        if next_element.name in ['ul', 'ol']:
                            list_items = next_element.find_all('li')
                            for item in list_items:
                                skill = item.get_text(strip=True)
                                if skill and skill not in skills:
                                    skills.append(skill)
                        elif next_element.name in ['p', 'div']:
                            text = next_element.get_text(strip=True)
                            if text and text not in skills:
                                # Check if it's comma-separated skills
                                if ',' in text:
                                    skill_list = [s.strip() for s in text.split(',')]
                                    skills.extend([s for s in skill_list if s and s not in skills])
                                else:
                                    skills.append(text)
                        next_element = next_element.find_next_sibling()

                    if skills:
                        break

        # Strategy 3: Search for all lists and filter
        if not skills:
            print("  ✗ No skills found")
            print("\n🔍 Strategy 3: Comprehensive list search...")
            all_lists = self.soup.find_all(['ul', 'ol'])

            for lst in all_lists:
                # Check if parent or previous sibling mentions skills
                context = ""
                prev_heading = lst.find_previous(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                if prev_heading:
                    context = prev_heading.get_text().lower()

                if any(keyword in context for keyword in ['skill', 'technical', 'expertise', 'proficien']):
                    print(f"  ✓ Found relevant list under: '{prev_heading.get_text(strip=True)}'")
                    list_items = lst.find_all('li')
                    for item in list_items:
                        skill = item.get_text(strip=True)
                        if skill and skill not in skills:
                            skills.append(skill)
                    break

        self.skills = skills
        return skills

    def extract_all_sections(self):
        """Extract all sections from the resume"""
        if not self.soup:
            print("Error: No webpage loaded. Call fetch_webpage() first.")
            return {}

        sections = {}
        headings = self.soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        for heading in headings:
            section_title = heading.get_text(strip=True)
            section_content = []

            # Get content until next heading
            next_element = heading.find_next_sibling()
            while next_element and next_element.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                text = next_element.get_text(strip=True)
                if text:
                    section_content.append(text)
                next_element = next_element.find_next_sibling()

            if section_content:
                sections[section_title] = section_content

        self.all_sections = sections
        return sections

    def display_skills(self):
        """Display extracted skills"""
        print("\n" + "="*60)
        print("📋 EXTRACTED SKILLS")
        print("="*60)

        if self.skills:
            for idx, skill in enumerate(self.skills, 1):
                print(f"{idx:2d}. {skill}")
            print(f"\n✓ Total skills found: {len(self.skills)}")
        else:
            print("✗ No skills found.")
            print("\nTroubleshooting tips:")
            print("1. Check if your resume webpage is accessible")
            print("2. Inspect the HTML structure of your skills section")
            print("3. Ensure the skills section has identifiable headings or classes")

        print("="*60)

    def display_all_sections(self):
        """Display all extracted sections"""
        print("\n" + "="*60)
        print("📄 ALL RESUME SECTIONS")
        print("="*60)

        for section_title, content in self.all_sections.items():
            print(f"\n### {section_title} ###")
            for item in content:
                # Truncate long items
                display_item = item if len(item) <= 100 else item[:97] + "..."
                print(f"  • {display_item}")

        print("="*60)

    def save_to_csv(self, filename='extracted_skills.csv'):
        """Save skills to CSV file"""
        if not self.skills:
            print("No skills to save.")
            return None

        df = pd.DataFrame({
            'Skill_Number': range(1, len(self.skills) + 1),
            'Skill': self.skills
        })

        df.to_csv(filename, index=False)
        print(f"\n✓ Skills saved to: {filename}")
        return df

    def save_to_json(self, filename='resume_data.json'):
        """Save all extracted data to JSON file"""
        data = {
            'url': self.url,
            'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'skills': self.skills,
            'all_sections': self.all_sections
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"✓ Complete resume data saved to: {filename}")
        return data

    def get_html_preview(self, chars=2000):
        """Get a preview of the HTML structure"""
        if self.soup:
            return self.soup.prettify()[:chars]
        return None


def main():
    """Main function to run the scraper"""
    print("="*60)
    print("🚀 Resume Skills Web Scraper")
    print("="*60)

    # Replace with your actual S3 URL
    resume_url = "http://hardik-jain-1837.s3-website-us-east-1.amazonaws.com/"

    # You can also pass the URL as a variable
    # resume_url = input("Enter your resume webpage URL: ").strip()

    # Create scraper instance
    scraper = ResumeSkillsScraper(resume_url)

    # Fetch webpage
    if not scraper.fetch_webpage():
        print("\n❌ Failed to fetch webpage. Exiting...")
        return

    # Extract skills
    print("\n" + "="*60)
    print("🔎 EXTRACTING SKILLS...")
    print("="*60)
    skills = scraper.extract_skills()

    # Display skills
    scraper.display_skills()

    # Extract all sections (optional)
    print("\n" + "="*60)
    print("🔎 EXTRACTING ALL SECTIONS...")
    print("="*60)
    scraper.extract_all_sections()
    scraper.display_all_sections()

    # Save results
    if skills:
        print("\n" + "="*60)
        print("💾 SAVING RESULTS...")
        print("="*60)
        scraper.save_to_csv('extracted_skills.csv')
        scraper.save_to_json('resume_data.json')

    print("\n✅ Scraping complete!")

    # Show HTML preview if no skills found
    if not skills:
        print("\n" + "="*60)
        print("📝 HTML STRUCTURE PREVIEW")
        print("="*60)
        print(scraper.get_html_preview(1500))
        print("\n... (preview truncated)")


if __name__ == "__main__":
    main()

