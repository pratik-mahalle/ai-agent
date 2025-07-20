"""
Event Discovery Agent

Discovers cloud-native events from Linux Foundation and CNCF websites.
"""

import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import re
from .base_agent import BaseAgent

class EventDiscoveryAgent(BaseAgent):
    """Agent for discovering cloud-native events."""
    
    def __init__(self):
        super().__init__(
            name="EventDiscoveryAgent",
            description="Discovers cloud-native events from Linux Foundation and CNCF"
        )
        
        # Event sources with more specific URLs
        self.sources = {
            'linux_foundation': {
                'url': 'https://www.linuxfoundation.org/events/',
                'name': 'Linux Foundation Events',
                'fallback_urls': [
                    'https://events.linuxfoundation.org/',
                    'https://www.linuxfoundation.org/events/upcoming-events/'
                ]
            },
            'cncf': {
                'url': 'https://www.cncf.io/events/',
                'name': 'CNCF Events',
                'fallback_urls': [
                    'https://www.cncf.io/events/upcoming-events/',
                    'https://www.cncf.io/events/past-events/'
                ]
            },
            'kubecon': {
                'url': 'https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/',
                'name': 'KubeCon Events',
                'fallback_urls': [
                    'https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/',
                    'https://events.linuxfoundation.org/kubecon-cloudnativecon-china/'
                ]
            }
        }
        
        # Event cache
        self.event_cache = {}
        self.cache_expiry = timedelta(hours=6)
        
        # Sample data for testing when web scraping fails
        self.sample_events = [
            {
                'id': 'kubecon_na_2024',
                'title': 'KubeCon + CloudNativeCon North America 2024',
                'date': 'November 12-15, 2024',
                'location': 'Salt Lake City, Utah',
                'description': 'The Cloud Native Computing Foundation\'s flagship conference bringing together adopters and technologists from leading open source and cloud native communities.',
                'url': 'https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/',
                'source': 'kubecon',
                'type': 'conference',
                'relevance_score': 10.0
            },
            {
                'id': 'kubecon_eu_2024',
                'title': 'KubeCon + CloudNativeCon Europe 2024',
                'date': 'March 19-22, 2024',
                'location': 'Paris, France',
                'description': 'The largest open source developer conference in Europe focused on cloud native applications and Kubernetes.',
                'url': 'https://events.linuxfoundation.org/kubecon-cloudnativecon-europe/',
                'source': 'kubecon',
                'type': 'conference',
                'relevance_score': 10.0
            },
            {
                'id': 'cncf_webinar_2024',
                'title': 'CNCF Webinar: Kubernetes Security Best Practices',
                'date': 'January 15, 2024',
                'location': 'Virtual',
                'description': 'Learn about the latest security best practices for Kubernetes clusters and containerized applications.',
                'url': 'https://www.cncf.io/events/',
                'source': 'cncf',
                'type': 'webinar',
                'relevance_score': 8.0
            },
            {
                'id': 'lf_workshop_2024',
                'title': 'Linux Foundation Workshop: Cloud Native Development',
                'date': 'February 20-22, 2024',
                'location': 'San Francisco, CA',
                'description': 'Hands-on workshop covering cloud native development practices, tools, and methodologies.',
                'url': 'https://www.linuxfoundation.org/events/',
                'source': 'linux_foundation',
                'type': 'workshop',
                'relevance_score': 7.0
            }
        ]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process event discovery requests."""
        request_type = request.get('type', 'discover')
        
        if request_type == 'discover':
            return await self.discover_events(request)
        elif request_type == 'filter':
            return await self.filter_events(request)
        elif request_type == 'details':
            return await self.get_event_details(request)
        else:
            return {
                'success': False,
                'error': f'Unknown request type: {request_type}'
            }
    
    async def discover_events(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Discover events from all sources."""
        try:
            self.log_activity("Starting event discovery")
            
            # Check cache first
            if self._is_cache_valid():
                self.log_activity("Using cached events")
                return {
                    'success': True,
                    'events': self.event_cache.get('events', []),
                    'source': 'cache',
                    'timestamp': self.event_cache.get('timestamp')
                }
            
            # Discover events from all sources
            all_events = []
            
            for source_id, source_info in self.sources.items():
                try:
                    events = await self._scrape_source(source_id, source_info)
                    all_events.extend(events)
                    self.log_activity(f"Discovered {len(events)} events from {source_info['name']}")
                except Exception as e:
                    self.log_activity(f"Error scraping {source_id}: {str(e)}")
            
            # If no events found from web scraping, use sample data
            if not all_events:
                self.log_activity("No events found from web scraping, using sample data")
                all_events = self.sample_events.copy()
            
            # Process and enrich events
            processed_events = await self._process_events(all_events)
            
            # Update cache
            self.event_cache = {
                'events': processed_events,
                'timestamp': datetime.now().isoformat()
            }
            
            # Add to conversation history
            self.add_to_history('assistant', f"Discovered {len(processed_events)} cloud-native events")
            
            return {
                'success': True,
                'events': processed_events,
                'source': 'live' if all_events != self.sample_events else 'sample',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_activity(f"Error in event discovery: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def filter_events(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Filter events based on criteria."""
        filters = request.get('filters', {})
        
        # Get events (from cache or discover)
        if not self._is_cache_valid():
            await self.discover_events({'type': 'discover'})
        
        events = self.event_cache.get('events', [])
        
        # Apply filters
        filtered_events = []
        for event in events:
            if self._matches_filters(event, filters):
                filtered_events.append(event)
        
        return {
            'success': True,
            'events': filtered_events,
            'filters_applied': filters,
            'total_found': len(filtered_events)
        }
    
    async def get_event_details(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed information about a specific event."""
        event_id = request.get('event_id')
        
        if not event_id:
            return {
                'success': False,
                'error': 'Event ID is required'
            }
        
        # Get events from cache or discover
        if not self._is_cache_valid():
            await self.discover_events({'type': 'discover'})
        
        events = self.event_cache.get('events', [])
        
        # Find the event
        event = next((e for e in events if e.get('id') == event_id), None)
        
        if not event:
            return {
                'success': False,
                'error': f'Event with ID {event_id} not found'
            }
        
        # Enrich with additional details
        enriched_event = await self._enrich_event_details(event)
        
        return {
            'success': True,
            'event': enriched_event
        }
    
    async def _scrape_source(self, source_id: str, source_info: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Scrape events from a specific source."""
        events = []
        
        # Try main URL first
        events = await self._scrape_url(source_info['url'], source_id)
        
        # If no events found, try fallback URLs
        if not events and 'fallback_urls' in source_info:
            for fallback_url in source_info['fallback_urls']:
                try:
                    fallback_events = await self._scrape_url(fallback_url, source_id)
                    events.extend(fallback_events)
                    if fallback_events:
                        break
                except Exception as e:
                    self.log_activity(f"Error scraping fallback URL {fallback_url}: {str(e)}")
        
        return events
    
    async def _scrape_url(self, url: str, source_id: str) -> List[Dict[str, Any]]:
        """Scrape events from a specific URL."""
        events = []
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; CloudNativeAIAgent/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
        
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(headers=headers, timeout=timeout) as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        if source_id == 'linux_foundation':
                            events = self._parse_linux_foundation_events(soup, url)
                        elif source_id == 'cncf':
                            events = self._parse_cncf_events(soup, url)
                        elif source_id == 'kubecon':
                            events = self._parse_kubecon_events(soup, url)
                    else:
                        self.log_activity(f"HTTP {response.status} for {url}")
            except Exception as e:
                self.log_activity(f"Error scraping {url}: {str(e)}")
        
        return events
    
    def _parse_linux_foundation_events(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Parse Linux Foundation events with improved selectors."""
        events = []
        
        # Multiple selectors for different page structures
        selectors = [
            'div[class*="event"]',
            'div[class*="card"]',
            'article[class*="event"]',
            'div[class*="item"]',
            'li[class*="event"]',
            '.event-item',
            '.event-card',
            '.upcoming-event',
            '[data-event]'
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                for container in containers:
                    try:
                        event = self._extract_event_data(container, 'linux_foundation', base_url)
                        if event:
                            events.append(event)
                    except Exception as e:
                        self.log_activity(f"Error parsing Linux Foundation event: {str(e)}")
                break  # If we found events with one selector, don't try others
        
        return events
    
    def _parse_cncf_events(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Parse CNCF events with improved selectors."""
        events = []
        
        # Multiple selectors for different page structures
        selectors = [
            'div[class*="event"]',
            'div[class*="card"]',
            'article[class*="event"]',
            '.event-item',
            '.event-card',
            '.upcoming-event',
            '[data-event]',
            'div[class*="webinar"]'
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                for container in containers:
                    try:
                        event = self._extract_event_data(container, 'cncf', base_url)
                        if event:
                            events.append(event)
                    except Exception as e:
                        self.log_activity(f"Error parsing CNCF event: {str(e)}")
                break
        
        return events
    
    def _parse_kubecon_events(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, Any]]:
        """Parse KubeCon events with improved selectors."""
        events = []
        
        # Multiple selectors for different page structures
        selectors = [
            'div[class*="kubecon"]',
            'div[class*="event"]',
            'div[class*="card"]',
            'article[class*="event"]',
            '.event-item',
            '.event-card',
            '.kubecon-event',
            '[data-event]'
        ]
        
        for selector in selectors:
            containers = soup.select(selector)
            if containers:
                for container in containers:
                    try:
                        event = self._extract_event_data(container, 'kubecon', base_url)
                        if event:
                            events.append(event)
                    except Exception as e:
                        self.log_activity(f"Error parsing KubeCon event: {str(e)}")
                break
        
        return events
    
    def _extract_event_data(self, container, source: str, base_url: str) -> Optional[Dict[str, Any]]:
        """Extract event data from a container element with improved logic."""
        try:
            # Extract title with multiple strategies
            title = None
            title_selectors = [
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                '[class*="title"]',
                '[class*="name"]',
                '.event-title',
                '.event-name'
            ]
            
            for selector in title_selectors:
                title_elem = container.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if title and len(title) > 5:  # Ensure it's not just whitespace
                        break
            
            # Extract date with multiple strategies
            date_str = None
            date_selectors = [
                'time',
                '[class*="date"]',
                '[class*="time"]',
                '.event-date',
                '.event-time',
                '[datetime]'
            ]
            
            for selector in date_selectors:
                date_elem = container.select_one(selector)
                if date_elem:
                    # Try datetime attribute first
                    date_str = date_elem.get('datetime') or date_elem.get_text(strip=True)
                    if date_str and len(date_str) > 3:
                        break
            
            # Extract location
            location = None
            location_selectors = [
                '[class*="location"]',
                '[class*="venue"]',
                '[class*="place"]',
                '.event-location',
                '.event-venue'
            ]
            
            for selector in location_selectors:
                location_elem = container.select_one(selector)
                if location_elem:
                    location = location_elem.get_text(strip=True)
                    if location and len(location) > 2:
                        break
            
            # Extract description
            description = None
            desc_selectors = [
                '[class*="description"]',
                '[class*="summary"]',
                '[class*="excerpt"]',
                '.event-description',
                '.event-summary',
                'p'
            ]
            
            for selector in desc_selectors:
                desc_elem = container.select_one(selector)
                if desc_elem:
                    description = desc_elem.get_text(strip=True)
                    if description and len(description) > 10:
                        break
            
            # Extract URL
            url = None
            link_elem = container.select_one('a[href]')
            if link_elem:
                href = link_elem['href']
                if href.startswith('http'):
                    url = href
                elif href.startswith('/'):
                    url = base_url.rstrip('/') + href
                else:
                    url = base_url.rstrip('/') + '/' + href
            
            # Create event if we have at least a title
            if title:
                return {
                    'id': f"{source}_{hash(title)}",
                    'title': title,
                    'date': date_str or 'TBD',
                    'location': location or 'TBD',
                    'description': description or 'No description available',
                    'url': url or base_url,
                    'source': source,
                    'type': 'conference' if 'kubecon' in source.lower() else 'event'
                }
        
        except Exception as e:
            self.log_activity(f"Error extracting event data: {str(e)}")
        
        return None
    
    async def _process_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process and enrich events with additional information."""
        processed_events = []
        
        for event in events:
            try:
                # Add additional metadata
                event['processed_at'] = datetime.now().isoformat()
                event['relevance_score'] = self._calculate_relevance_score(event)
                event['deadlines'] = self._estimate_deadlines(event)
                
                processed_events.append(event)
            except Exception as e:
                self.log_activity(f"Error processing event {event.get('title', 'Unknown')}: {str(e)}")
        
        # Sort by relevance and date
        processed_events.sort(key=lambda x: (x.get('relevance_score', 0), x.get('date', '')), reverse=True)
        
        return processed_events
    
    def _calculate_relevance_score(self, event: Dict[str, Any]) -> float:
        """Calculate relevance score for an event."""
        score = 0.0
        
        title = event.get('title', '').lower()
        description = event.get('description', '').lower()
        
        # Keywords that indicate cloud-native relevance
        cloud_native_keywords = [
            'kubernetes', 'kubecon', 'cncf', 'cloud native', 'container', 'microservices',
            'devops', 'gitops', 'observability', 'service mesh', 'istio', 'prometheus',
            'grafana', 'helm', 'operators', 'cri-o', 'containerd', 'etcd'
        ]
        
        for keyword in cloud_native_keywords:
            if keyword in title:
                score += 2.0
            if keyword in description:
                score += 1.0
        
        # Bonus for KubeCon events
        if 'kubecon' in title.lower():
            score += 5.0
        
        # Bonus for Linux Foundation events
        if event.get('source') in ['linux_foundation', 'cncf']:
            score += 1.0
        
        return min(score, 10.0)  # Cap at 10
    
    def _estimate_deadlines(self, event: Dict[str, Any]) -> Dict[str, str]:
        """Estimate important deadlines for an event."""
        # This is a simplified estimation - in practice, you'd want to parse actual dates
        return {
            'cfp_deadline': 'TBD',
            'registration_deadline': 'TBD',
            'scholarship_deadline': 'TBD'
        }
    
    def _matches_filters(self, event: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if an event matches the given filters."""
        for key, value in filters.items():
            if key == 'location' and value:
                if not event.get('location') or value.lower() not in event['location'].lower():
                    return False
            elif key == 'date_range' and value:
                # Implement date range filtering
                pass
            elif key == 'min_relevance' and value:
                if event.get('relevance_score', 0) < value:
                    return False
            elif key == 'event_type' and value:
                if event.get('type') != value:
                    return False
        
        return True
    
    def _is_cache_valid(self) -> bool:
        """Check if the event cache is still valid."""
        if not self.event_cache:
            return False
        
        timestamp_str = self.event_cache.get('timestamp')
        if not timestamp_str:
            return False
        
        try:
            cache_time = datetime.fromisoformat(timestamp_str)
            return datetime.now() - cache_time < self.cache_expiry
        except:
            return False
    
    async def _enrich_event_details(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich event with additional details."""
        # Add scholarship information
        event['scholarship_info'] = {
            'available': True,
            'deadline': 'TBD',
            'requirements': [
                'Student or early career professional',
                'Demonstrated interest in cloud-native technologies',
                'Financial need'
            ]
        }
        
        # Add travel funding information
        event['travel_funding'] = {
            'available': True,
            'deadline': 'TBD',
            'coverage': 'Partial travel and accommodation'
        }
        
        return event 