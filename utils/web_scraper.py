"""
Web Scraper Utility

Provides web scraping functionality for the AI agent.
"""

import aiohttp
import asyncio
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
import re
import logging
from datetime import datetime
import time

class WebScraper:
    """Web scraper utility for fetching data from various sources."""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(__name__)
        
        # Default headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; CloudNativeAIAgent/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    async def fetch_page(self, url: str, headers: Optional[Dict] = None) -> Optional[str]:
        """Fetch a web page asynchronously."""
        if headers is None:
            headers = self.headers
        
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=self.timeout) as response:
                        if response.status == 200:
                            return await response.text()
                        else:
                            self.logger.warning(f"HTTP {response.status} for {url}")
                            
            except asyncio.TimeoutError:
                self.logger.warning(f"Timeout on attempt {attempt + 1} for {url}")
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {str(e)}")
            
            # Wait before retry
            if attempt < self.max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    async def scrape_events(self, url: str, parser_type: str) -> List[Dict[str, Any]]:
        """Scrape events from a given URL using the specified parser."""
        html = await self.fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        
        if parser_type == 'linux_foundation':
            return self._parse_linux_foundation_events(soup)
        elif parser_type == 'cncf':
            return self._parse_cncf_events(soup)
        elif parser_type == 'kubecon':
            return self._parse_kubecon_events(soup)
        else:
            return self._parse_generic_events(soup)
    
    def _parse_linux_foundation_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse Linux Foundation events."""
        events = []
        
        # Look for event containers
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|item'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'linux_foundation')
                if event:
                    events.append(event)
            except Exception as e:
                self.logger.error(f"Error parsing Linux Foundation event: {str(e)}")
        
        return events
    
    def _parse_cncf_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse CNCF events."""
        events = []
        
        # Look for event containers
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|item'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'cncf')
                if event:
                    events.append(event)
            except Exception as e:
                self.logger.error(f"Error parsing CNCF event: {str(e)}")
        
        return events
    
    def _parse_kubecon_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse KubeCon events."""
        events = []
        
        # Look for KubeCon specific containers
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|item|kubecon'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'kubecon')
                if event:
                    events.append(event)
            except Exception as e:
                self.logger.error(f"Error parsing KubeCon event: {str(e)}")
        
        return events
    
    def _parse_generic_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse generic events using common patterns."""
        events = []
        
        # Look for common event patterns
        event_containers = soup.find_all(['div', 'article', 'section'], 
                                       class_=re.compile(r'event|card|item|post'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'generic')
                if event:
                    events.append(event)
            except Exception as e:
                self.logger.error(f"Error parsing generic event: {str(e)}")
        
        return events
    
    def _extract_event_data(self, container, source: str) -> Optional[Dict[str, Any]]:
        """Extract event data from a container element."""
        try:
            # Extract title
            title_elem = container.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
            title = title_elem.get_text(strip=True) if title_elem else None
            
            # Extract date
            date_elem = container.find(['time', 'span', 'div'], class_=re.compile(r'date|time'))
            date_str = date_elem.get_text(strip=True) if date_elem else None
            
            # Extract location
            location_elem = container.find(['span', 'div'], class_=re.compile(r'location|venue|place'))
            location = location_elem.get_text(strip=True) if location_elem else None
            
            # Extract description
            desc_elem = container.find(['p', 'div'], class_=re.compile(r'description|summary|excerpt'))
            description = desc_elem.get_text(strip=True) if desc_elem else None
            
            # Extract URL
            link_elem = container.find('a', href=True)
            url = link_elem['href'] if link_elem else None
            
            if title and date_str:
                return {
                    'id': f"{source}_{hash(title)}",
                    'title': title,
                    'date': date_str,
                    'location': location,
                    'description': description,
                    'url': url,
                    'source': source,
                    'scraped_at': datetime.now().isoformat()
                }
        
        except Exception as e:
            self.logger.error(f"Error extracting event data: {str(e)}")
        
        return None
    
    async def scrape_scholarship_info(self, url: str) -> Dict[str, Any]:
        """Scrape scholarship information from a URL."""
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract scholarship information
        scholarship_info = {
            'requirements': [],
            'deadlines': {},
            'coverage': [],
            'max_amount': None
        }
        
        # Look for requirements
        req_elements = soup.find_all(['li', 'p'], string=re.compile(r'requirement|eligible|qualify', re.I))
        for elem in req_elements:
            text = elem.get_text(strip=True)
            if text:
                scholarship_info['requirements'].append(text)
        
        # Look for deadlines
        deadline_elements = soup.find_all(['span', 'div'], string=re.compile(r'deadline|due|application', re.I))
        for elem in deadline_elements:
            text = elem.get_text(strip=True)
            if text:
                # Try to extract date information
                date_match = re.search(r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text)
                if date_match:
                    scholarship_info['deadlines']['application'] = date_match.group(1)
        
        # Look for coverage information
        coverage_elements = soup.find_all(['li', 'p'], string=re.compile(r'cover|include|provide', re.I))
        for elem in coverage_elements:
            text = elem.get_text(strip=True)
            if text:
                scholarship_info['coverage'].append(text)
        
        # Look for amount information
        amount_elements = soup.find_all(string=re.compile(r'\$\d+|\d+\s*dollars', re.I))
        for elem in amount_elements:
            amount_match = re.search(r'\$?(\d+)', elem)
            if amount_match:
                scholarship_info['max_amount'] = int(amount_match.group(1))
                break
        
        return scholarship_info
    
    async def scrape_travel_funding_info(self, url: str) -> Dict[str, Any]:
        """Scrape travel funding information from a URL."""
        html = await self.fetch_page(url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract travel funding information
        funding_info = {
            'requirements': [],
            'coverage': [],
            'max_amount': None,
            'deadlines': {}
        }
        
        # Look for requirements
        req_elements = soup.find_all(['li', 'p'], string=re.compile(r'requirement|eligible|qualify', re.I))
        for elem in req_elements:
            text = elem.get_text(strip=True)
            if text:
                funding_info['requirements'].append(text)
        
        # Look for coverage
        coverage_elements = soup.find_all(['li', 'p'], string=re.compile(r'cover|include|provide|travel|accommodation', re.I))
        for elem in coverage_elements:
            text = elem.get_text(strip=True)
            if text:
                funding_info['coverage'].append(text)
        
        # Look for amount information
        amount_elements = soup.find_all(string=re.compile(r'\$\d+|\d+\s*dollars', re.I))
        for elem in amount_elements:
            amount_match = re.search(r'\$?(\d+)', elem)
            if amount_match:
                funding_info['max_amount'] = int(amount_match.group(1))
                break
        
        return funding_info
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\-\:]', '', text)
        
        return text.strip()
    
    def extract_dates(self, text: str) -> List[str]:
        """Extract dates from text."""
        date_patterns = [
            r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}',  # MM/DD/YYYY or MM-DD-YYYY
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',    # YYYY/MM/DD or YYYY-MM-DD
            r'\w+\s+\d{1,2},?\s+\d{4}',        # Month DD, YYYY
            r'\d{1,2}\s+\w+\s+\d{4}'           # DD Month YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        return dates
    
    def extract_urls(self, text: str) -> List[str]:
        """Extract URLs from text."""
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        return re.findall(url_pattern, text)
    
    def extract_emails(self, text: str) -> List[str]:
        """Extract email addresses from text."""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.findall(email_pattern, text) 