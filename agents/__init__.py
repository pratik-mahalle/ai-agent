"""
Cloud-Native AI Agent Package

This package contains the core AI agents for:
- Event Discovery
- Talk Proposal Generation
- Scholarship Application Assistance
- Travel Funding Assistance
"""

from .event_discovery import EventDiscoveryAgent
from .proposal_generator import ProposalGeneratorAgent
from .scholarship_assistant import ScholarshipAssistantAgent
from .travel_funding_assistant import TravelFundingAssistantAgent

__all__ = [
    'EventDiscoveryAgent',
    'ProposalGeneratorAgent', 
    'ScholarshipAssistantAgent',
    'TravelFundingAssistantAgent'
] 