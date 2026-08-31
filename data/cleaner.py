from bs4 import BeautifulSoup
import re

class ContentCleaner:
    @staticmethod
    def clean_html(html_content: str) -> str:
        """
        Removes boilerplate, scripts, styles, and extracts readable text.
        """
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")

        # Remove script and style elements
        for script_or_style in soup(["script", "style", "noscript", "iframe", "header", "footer", "nav"]):
            script_or_style.decompose()

        # Get text
        text = soup.get_text(separator=" ")

        # Normalize whitespace (remove multiple spaces/newlines)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    @staticmethod
    def extract_metadata(html_content: str) -> dict:
        """
        Extracts basic metadata like title, description.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        title = soup.title.string if soup.title else ""
        
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            description = meta_desc.get("content", "")
            
        return {
            "title": title,
            "description": description
        }
