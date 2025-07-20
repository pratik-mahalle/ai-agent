"""
Test Script for Cloud-Native AI Agent

Simple test script to verify the agent functionality.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import agents
from agents.event_discovery import EventDiscoveryAgent
from agents.proposal_generator import ProposalGeneratorAgent
from agents.scholarship_assistant import ScholarshipAssistantAgent
from agents.travel_funding_assistant import TravelFundingAssistantAgent

async def test_event_discovery():
    """Test the event discovery agent."""
    print("🔍 Testing Event Discovery Agent...")
    
    agent = EventDiscoveryAgent()
    
    # Test event discovery
    result = await agent.discover_events({'type': 'discover'})
    
    if result['success']:
        print(f"✅ Discovered {len(result['events'])} events")
        for event in result['events'][:3]:  # Show first 3 events
            print(f"  - {event.get('title', 'Unknown')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

async def test_proposal_generation():
    """Test the proposal generation agent."""
    print("\n📝 Testing Proposal Generator Agent...")
    
    agent = ProposalGeneratorAgent()
    
    # Test proposal generation
    result = await agent.generate_proposal({
        'type': 'generate',
        'topic': 'Kubernetes Operators in Production',
        'speaker_expertise': ['Kubernetes', 'DevOps'],
        'target_audience': 'intermediate',
        'talk_type': 'session'
    })
    
    if result['success']:
        proposal = result['proposal']
        print(f"✅ Generated proposal: {proposal.get('title', 'Untitled')}")
        print(f"  Abstract: {proposal.get('abstract', 'No abstract')[:100]}...")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

async def test_scholarship_assistant():
    """Test the scholarship assistant agent."""
    print("\n🎓 Testing Scholarship Assistant Agent...")
    
    agent = ScholarshipAssistantAgent()
    
    # Test scholarship info
    result = await agent.get_scholarship_info({'type': 'info'})
    
    if result['success']:
        print(f"✅ Found {result['total_programs']} scholarship programs")
        for program_id, program in result['programs'].items():
            print(f"  - {program['name']}: ${program.get('max_amount', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

async def test_travel_funding():
    """Test the travel funding assistant agent."""
    print("\n✈️ Testing Travel Funding Assistant Agent...")
    
    agent = TravelFundingAssistantAgent()
    
    # Test funding info
    result = await agent.get_funding_info({'type': 'info'})
    
    if result['success']:
        print(f"✅ Found {result['total_sources']} funding sources")
        for source_id, source in result['funding_sources'].items():
            print(f"  - {source['name']}: ${source.get('max_amount', 'N/A')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

async def test_cost_estimation():
    """Test travel cost estimation."""
    print("\n💸 Testing Cost Estimation...")
    
    agent = TravelFundingAssistantAgent()
    
    result = await agent.estimate_costs({
        'event_details': {
            'location': 'San Francisco, CA',
            'duration_days': 3
        },
        'travel_preferences': {
            'departure_location': 'New York, NY',
            'accommodation': 'standard'
        }
    })
    
    if result['success']:
        print(f"✅ Estimated total cost: ${result['total_cost']:.2f}")
        for category, details in result['cost_breakdown'].items():
            print(f"  - {category.title()}: ${details['amount']:.2f}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

async def main():
    """Run all tests."""
    print("🚀 Cloud-Native AI Agent - Test Suite")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  Warning: OPENAI_API_KEY not set. Some features may not work.")
        print("   Set your OpenAI API key in the .env file to test AI features.")
    
    try:
        # Run tests
        await test_event_discovery()
        await test_proposal_generation()
        await test_scholarship_assistant()
        await test_travel_funding()
        await test_cost_estimation()
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("This might be due to missing dependencies or configuration.")

if __name__ == "__main__":
    asyncio.run(main()) 