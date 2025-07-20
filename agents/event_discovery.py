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
        
        # Event sources
        self.sources = {
            'linux_foundation': {
                'url': 'https://www.linuxfoundation.org/events/',
                'name': 'Linux Foundation Events'
            },
            'cncf': {
                'url': 'https://www.cncf.io/events/',
                'name': 'CNCF Events'
            },
            'kubecon': {
                'url': 'https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/',
                'name': 'KubeCon Events'
            }
        }
        
        # Event cache
        self.event_cache = {}
        self.cache_expiry = timedelta(hours=6)
    
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
                'source': 'live',
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
        
        async with aiohttp.ClientSession() as session:
            async with session.get(source_info['url']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    if source_id == 'linux_foundation':
                        events = self._parse_linux_foundation_events(soup)
                    elif source_id == 'cncf':
                        events = self._parse_cncf_events(soup)
                    elif source_id == 'kubecon':
                        events = self._parse_kubecon_events(soup)
        
        return events
    
    def _parse_linux_foundation_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse Linux Foundation events."""
        events = []
        
        # Look for event cards/containers
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|item'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'linux_foundation')
                if event:
                    events.append(event)
            except Exception as e:
                self.log_activity(f"Error parsing Linux Foundation event: {str(e)}")
        
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
                self.log_activity(f"Error parsing CNCF event: {str(e)}")
        
        return events
    
    def _parse_kubecon_events(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Parse KubeCon events."""
        events = []
        
        # Look for KubeCon specific event containers
        event_containers = soup.find_all(['div', 'article'], class_=re.compile(r'event|card|item|kubecon'))
        
        for container in event_containers:
            try:
                event = self._extract_event_data(container, 'kubecon')
                if event:
                    events.append(event)
            except Exception as e:
                self.log_activity(f"Error parsing KubeCon event: {str(e)}")
        
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