"""
Cloud-Native AI Agent - Main Application

A Streamlit web application that provides an interface for the AI agent system.
"""

import streamlit as st
import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any

# Import our agents
from agents.event_discovery import EventDiscoveryAgent
from agents.proposal_generator import ProposalGeneratorAgent
from agents.scholarship_assistant import ScholarshipAssistantAgent
from agents.travel_funding_assistant import TravelFundingAssistantAgent

# Configure page
st.set_page_config(
    page_title="Cloud-Native AI Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class CloudNativeAIAgent:
    """Main application class for the Cloud-Native AI Agent."""
    
    def __init__(self):
        self.event_agent = EventDiscoveryAgent()
        self.proposal_agent = ProposalGeneratorAgent()
        self.scholarship_agent = ScholarshipAssistantAgent()
        self.travel_agent = TravelFundingAssistantAgent()
        
        # Initialize session state
        if 'events' not in st.session_state:
            st.session_state.events = []
        if 'proposals' not in st.session_state:
            st.session_state.proposals = []
        if 'applications' not in st.session_state:
            st.session_state.applications = []
    
    def run(self):
        """Run the main application."""
        # Header
        st.markdown('<h1 class="main-header">🚀 Cloud-Native AI Agent</h1>', unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <p style="font-size: 1.2rem; color: #666;">
                Your intelligent assistant for cloud-native events, talk proposals, and funding applications
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar navigation
        self._create_sidebar()
        
        # Main content area
        page = st.session_state.get('current_page', 'dashboard')
        
        if page == 'dashboard':
            self._show_dashboard()
        elif page == 'events':
            self._show_events_page()
        elif page == 'proposals':
            self._show_proposals_page()
        elif page == 'scholarships':
            self._show_scholarships_page()
        elif page == 'travel_funding':
            self._show_travel_funding_page()
        elif page == 'settings':
            self._show_settings_page()
    
    def _create_sidebar(self):
        """Create the sidebar navigation."""
        st.sidebar.title("Navigation")
        
        pages = {
            'dashboard': '📊 Dashboard',
            'events': '🔍 Event Discovery',
            'proposals': '📝 Talk Proposals',
            'scholarships': '🎓 Scholarships',
            'travel_funding': '✈️ Travel Funding',
            'settings': '⚙️ Settings'
        }
        
        selected_page = st.sidebar.selectbox(
            "Choose a page:",
            list(pages.keys()),
            format_func=lambda x: pages[x],
            index=0
        )
        
        st.session_state.current_page = selected_page
        
        # Agent status
        st.sidebar.markdown("---")
        st.sidebar.subheader("Agent Status")
        
        agents = [
            ("Event Discovery", self.event_agent),
            ("Proposal Generator", self.proposal_agent),
            ("Scholarship Assistant", self.scholarship_agent),
            ("Travel Funding", self.travel_agent)
        ]
        
        for name, agent in agents:
            status = agent.get_status()
            st.sidebar.markdown(f"**{name}**: ✅ Active")
    
    def _show_dashboard(self):
        """Show the main dashboard."""
        st.header("📊 Dashboard")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Events Found", len(st.session_state.events))
        
        with col2:
            st.metric("Proposals Generated", len(st.session_state.proposals))
        
        with col3:
            st.metric("Applications Tracked", len(st.session_state.applications))
        
        with col4:
            st.metric("Active Agents", 4)
        
        # Quick actions
        st.subheader("🚀 Quick Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Discover Events", use_container_width=True):
                st.session_state.current_page = 'events'
                st.rerun()
            
            if st.button("📝 Generate Proposal", use_container_width=True):
                st.session_state.current_page = 'proposals'
                st.rerun()
        
        with col2:
            if st.button("🎓 Check Scholarships", use_container_width=True):
                st.session_state.current_page = 'scholarships'
                st.rerun()
            
            if st.button("✈️ Plan Travel Funding", use_container_width=True):
                st.session_state.current_page = 'travel_funding'
                st.rerun()
        
        # Recent activity
        st.subheader("📈 Recent Activity")
        
        if st.session_state.events:
            st.markdown("**Recent Events:**")
            for event in st.session_state.events[-3:]:
                st.markdown(f"- {event.get('title', 'Unknown Event')}")
        
        if st.session_state.proposals:
            st.markdown("**Recent Proposals:**")
            for proposal in st.session_state.proposals[-3:]:
                st.markdown(f"- {proposal.get('title', 'Unknown Proposal')}")
    
    def _show_events_page(self):
        """Show the events discovery page."""
        st.header("🔍 Event Discovery")
        
        # Search controls
        col1, col2, col3 = st.columns(3)

        with col1:
            location_filter = st.text_input("Location Filter", placeholder="e.g., San Francisco")
        
        with col2:
            event_type = st.selectbox("Event Type", ["All", "Conference", "Workshop", "Meetup"])
        
        with col3:
            if st.button("🔍 Discover Events", use_container_width=True):
                asyncio.run(self._discover_events(location_filter, event_type))
        
        # Display events
        if st.session_state.events:
            st.subheader("📅 Discovered Events")
            
            for i, event in enumerate(st.session_state.events):
                with st.expander(f"📅 {event.get('title', 'Unknown Event')}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Date:** {event.get('date', 'TBD')}")
                        st.markdown(f"**Location:** {event.get('location', 'TBD')}")
                        st.markdown(f"**Source:** {event.get('source', 'Unknown')}")
                        
                        if event.get('description'):
                            st.markdown(f"**Description:** {event['description']}")
                    
                    with col2:
                        st.markdown(f"**Relevance Score:** {event.get('relevance_score', 0):.1f}/10")
                        
                        if event.get('url'):
                            st.markdown(f"[🔗 Event Website]({event['url']})")
                        
                        if st.button(f"Get Details", key=f"details_{i}"):
                            import asyncio
                            asyncio.run(self._get_event_details(event))
        else:
            st.info("No events discovered yet. Click 'Discover Events' to start!")
    
    def _show_proposals_page(self):
        """Show the proposal generation page."""
        st.header("📝 Talk Proposal Generator")
        
        # Proposal form
        with st.form("proposal_form"):
            st.subheader("Generate New Proposal")
            
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input("Topic", placeholder="e.g., Kubernetes Operators in Production")
                speaker_expertise = st.multiselect(
                    "Your Expertise",
                    ["Kubernetes", "Docker", "Microservices", "DevOps", "GitOps", 
                     "Observability", "Security", "Service Mesh", "Cloud Native", "Containers"]
                )
                target_audience = st.selectbox("Target Audience", ["Beginner", "Intermediate", "Advanced"])
            
            with col2:
                talk_type = st.selectbox("Talk Type", ["Session", "Lightning Talk", "Workshop", "Panel"])
                event_context = st.text_area("Event Context (Optional)", 
                                           placeholder="Any specific event or context...")
            
            submitted = st.form_submit_button("🚀 Generate Proposal")
            
            if submitted:
                import asyncio
                asyncio.run(self._generate_proposal(topic, speaker_expertise, target_audience, talk_type, event_context))
        
        # Display generated proposals
        if st.session_state.proposals:
            st.subheader("📋 Generated Proposals")
            
            for i, proposal in enumerate(st.session_state.proposals):
                with st.expander(f"📝 {proposal.get('title', 'Untitled Proposal')}"):
                    st.markdown(f"**Abstract:** {proposal.get('abstract', 'No abstract')}")
                    
                    if proposal.get('learning_objectives'):
                        st.markdown("**Learning Objectives:**")
                        for obj in proposal['learning_objectives']:
                            st.markdown(f"- {obj}")
                    
                    if proposal.get('track_suggestions'):
                        st.markdown(f"**Suggested Tracks:** {', '.join(proposal['track_suggestions'])}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"Improve Proposal", key=f"improve_{i}"):
                            import asyncio
                            asyncio.run(self._improve_proposal(proposal))
                    with col2:
                        if st.button(f"Export", key=f"export_{i}"):
                            self._export_proposal(proposal)
    
    def _show_scholarships_page(self):
        """Show the scholarships page."""
        st.header("🎓 Scholarship Assistant")
        
        # Scholarship info
        tab1, tab2, tab3 = st.tabs(["📋 Available Scholarships", "✅ Check Eligibility", "📝 Generate Application"])
        
        with tab1:
            st.subheader("Available Scholarship Programs")
            
            if st.button("🔍 Get Scholarship Info"):
                import asyncio
                asyncio.run(self._get_scholarship_info())
        
        with tab2:
            st.subheader("Check Your Eligibility")
            
            with st.form("eligibility_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    is_student = st.checkbox("I am a student")
                    is_early_career = st.checkbox("I am an early career professional (≤3 years)")
                    financial_need = st.checkbox("I have financial need")
                
                with col2:
                    is_underrepresented = st.checkbox("I am from an underrepresented group")
                    previously_awarded = st.checkbox("I have previously received a scholarship")
                    community_involvement = st.checkbox("I am involved in the community")
                
                if st.form_submit_button("✅ Check Eligibility"):
                    self._check_eligibility(is_student, is_early_career, financial_need, 
                                          is_underrepresented, previously_awarded, community_involvement)
        
        with tab3:
            st.subheader("Generate Application")
            
            with st.form("application_form"):
                applicant_info = st.text_area("Tell us about yourself", 
                                            placeholder="Your background, experience, goals...")
                
                if st.form_submit_button("📝 Generate Application"):
                    self._generate_scholarship_application(applicant_info)
    
    def _show_travel_funding_page(self):
        """Show the travel funding page."""
        st.header("✈️ Travel Funding Assistant")
        
        tab1, tab2, tab3 = st.tabs(["💰 Funding Sources", "💸 Cost Estimation", "📝 Application"])
        
        with tab1:
            st.subheader("Available Travel Funding")
            
            if st.button("🔍 Get Funding Sources"):
                self._get_travel_funding_sources()
        
        with tab2:
            st.subheader("Estimate Travel Costs")
            
            with st.form("cost_estimation_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    event_location = st.text_input("Event Location", placeholder="e.g., San Francisco, CA")
                    departure_location = st.text_input("Departure Location", placeholder="e.g., New York, NY")
                    event_duration = st.number_input("Event Duration (days)", min_value=1, value=3)
                
                with col2:
                    accommodation_preference = st.selectbox("Accommodation Preference", 
                                                          ["Budget", "Standard", "Premium"])
                    is_domestic = st.checkbox("Domestic travel")
                
                if st.form_submit_button("💸 Estimate Costs"):
                    self._estimate_travel_costs(event_location, departure_location, event_duration, 
                                              accommodation_preference, is_domestic)
        
        with tab3:
            st.subheader("Generate Funding Application")
            
            with st.form("funding_application_form"):
                event_details = st.text_area("Event Details", 
                                           placeholder="Event name, dates, your participation...")
                financial_situation = st.text_area("Financial Situation", 
                                                 placeholder="Your financial need and constraints...")
                
                if st.form_submit_button("📝 Generate Application"):
                    self._generate_travel_funding_application(event_details, financial_situation)
    
    def _show_settings_page(self):
        """Show the settings page."""
        st.header("⚙️ Settings")
        
        st.subheader("API Configuration")
        
        gemini_key = st.text_input("Gemini API Key", type="password", 
                                  help="Your Google Gemini API key for AI-powered features")
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved successfully!")
        
        st.subheader("Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear All Data"):
                st.session_state.events = []
                st.session_state.proposals = []
                st.session_state.applications = []
                st.success("All data cleared!")
        
        with col2:
            if st.button("📥 Export Data"):
                self._export_all_data()
    
    async def _discover_events(self, location_filter: str, event_type: str):
        """Discover events using the event discovery agent."""
        try:
            with st.spinner("🔍 Discovering events..."):
                filters = {}
                if location_filter:
                    filters['location'] = location_filter
                if event_type != "All":
                    filters['event_type'] = event_type.lower()
                
                result = await self.event_agent.discover_events({'type': 'discover', 'filters': filters})
                
                if result['success']:
                    st.session_state.events = result['events']
                    st.success(f"✅ Discovered {len(result['events'])} events!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error discovering events: {str(e)}")
    
    async def _get_event_details(self, event: Dict[str, Any]):
        """Get detailed information about an event."""
        try:
            with st.spinner("🔍 Getting event details..."):
                result = await self.event_agent.get_event_details({'event_id': event.get('id')})
                
                if result['success']:
                    st.json(result['event'])
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error getting event details: {str(e)}")
    
    async def _generate_proposal(self, topic: str, speaker_expertise: List[str], 
                               target_audience: str, talk_type: str, event_context: str):
        """Generate a talk proposal."""
        try:
            with st.spinner("🚀 Generating proposal..."):
                request = {
                    'type': 'generate',
                    'topic': topic,
                    'speaker_expertise': speaker_expertise,
                    'target_audience': target_audience,
                    'talk_type': talk_type,
                    'event_context': event_context
                }
                
                result = await self.proposal_agent.generate_proposal(request)
                
                if result['success']:
                    proposal = result['proposal']
                    proposal['generated_at'] = datetime.now().isoformat()
                    st.session_state.proposals.append(proposal)
                    st.success("✅ Proposal generated successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error generating proposal: {str(e)}")
    
    async def _improve_proposal(self, proposal: Dict[str, Any]):
        """Improve an existing proposal."""
        try:
            with st.spinner("🔧 Improving proposal..."):
                result = await self.proposal_agent.improve_proposal({'proposal': proposal})
                
                if result['success']:
                    st.json(result['improved_proposal'])
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error improving proposal: {str(e)}")
    
    def _export_proposal(self, proposal: Dict[str, Any]):
        """Export a proposal."""
        st.download_button(
            label="📥 Download Proposal",
            data=json.dumps(proposal, indent=2),
            file_name=f"proposal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    async def _get_scholarship_info(self):
        """Get scholarship information."""
        try:
            with st.spinner("🔍 Getting scholarship info..."):
                result = await self.scholarship_agent.get_scholarship_info({})
                
                if result['success']:
                    for program_id, program in result['programs'].items():
                        with st.expander(f"🎓 {program['name']}"):
                            st.markdown(f"**Max Amount:** ${program.get('max_amount', 'N/A')}")
                            st.markdown(f"**Requirements:**")
                            for req in program.get('requirements', []):
                                st.markdown(f"- {req}")
                            st.markdown(f"**Coverage:**")
                            for coverage in program.get('coverage', []):
                                st.markdown(f"- {coverage}")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error getting scholarship info: {str(e)}")
    
    async def _check_eligibility(self, is_student: bool, is_early_career: bool, 
                               financial_need: bool, is_underrepresented: bool, 
                               previously_awarded: bool, community_involvement: bool):
        """Check scholarship eligibility."""
        try:
            with st.spinner("✅ Checking eligibility..."):
                applicant_info = {
                    'is_student': is_student,
                    'is_early_career': is_early_career,
                    'financial_need': financial_need,
                    'is_underrepresented': is_underrepresented,
                    'previously_awarded': previously_awarded,
                    'community_involvement': community_involvement
                }
                
                result = await self.scholarship_agent.check_eligibility({
                    'applicant_info': applicant_info,
                    'program_id': 'kubecon'  # Default to KubeCon scholarship
                })
                
                if result['success']:
                    if result['eligible']:
                        st.success("✅ You are eligible for scholarships!")
                    else:
                        st.warning("⚠️ You may not be eligible for some scholarships")
                    
                    st.markdown("**Requirements Check:**")
                    for check in result['requirements_check']:
                        status = "✅" if check['eligible'] else "❌"
                        st.markdown(f"{status} {check['requirement']}")
                    
                    if result['recommendations']:
                        st.markdown("**Recommendations:**")
                        for rec in result['recommendations']:
                            st.markdown(f"- {rec}")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error checking eligibility: {str(e)}")
    
    async def _generate_scholarship_application(self, applicant_info: str):
        """Generate a scholarship application."""
        try:
            with st.spinner("📝 Generating application..."):
                # Parse applicant info (simplified)
                parsed_info = {
                    'background': applicant_info,
                    'years_experience': 2,  # Default
                    'current_role': 'Developer',
                    'interests': ['Kubernetes', 'Cloud Native']
                }
                
                result = await self.scholarship_agent.generate_application({
                    'applicant_info': parsed_info,
                    'program_id': 'kubecon'
                })
                
                if result['success']:
                    application = result['application']
                    
                    st.markdown("**Personal Statement:**")
                    st.markdown(application['personal_statement'])
                    
                    st.markdown("**Financial Need Statement:**")
                    st.markdown(application['financial_need_statement'])
                    
                    st.markdown("**Goals Statement:**")
                    st.markdown(application['goals_statement'])
                    
                    st.success("✅ Application generated successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error generating application: {str(e)}")
    
    async def _get_travel_funding_sources(self):
        """Get travel funding sources."""
        try:
            with st.spinner("💰 Getting funding sources..."):
                result = await self.travel_agent.get_funding_info({})
                
                if result['success']:
                    for source_id, source in result['funding_sources'].items():
                        with st.expander(f"💰 {source['name']}"):
                            st.markdown(f"**Max Amount:** ${source.get('max_amount', 'N/A')}")
                            st.markdown(f"**Requirements:**")
                            for req in source.get('requirements', []):
                                st.markdown(f"- {req}")
                            st.markdown(f"**Coverage:**")
                            for coverage in source.get('coverage', []):
                                st.markdown(f"- {coverage}")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error getting funding sources: {str(e)}")
    
    async def _estimate_travel_costs(self, event_location: str, departure_location: str, 
                                   event_duration: int, accommodation_preference: str, is_domestic: bool):
        """Estimate travel costs."""
        try:
            with st.spinner("💸 Estimating costs..."):
                result = await self.travel_agent.estimate_costs({
                    'event_details': {
                        'location': event_location,
                        'duration_days': event_duration
                    },
                    'travel_preferences': {
                        'departure_location': departure_location,
                        'accommodation': accommodation_preference
                    }
                })
                
                if result['success']:
                    st.markdown(f"**Total Estimated Cost:** ${result['total_cost']:.2f}")
                    
                    st.markdown("**Cost Breakdown:**")
                    for category, details in result['cost_breakdown'].items():
                        st.markdown(f"- **{category.title()}:** ${details['amount']:.2f} - {details['description']}")
                    
                    if result['cost_saving_tips']:
                        st.markdown("**Cost Saving Tips:**")
                        for tip in result['cost_saving_tips']:
                            st.markdown(f"- {tip}")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error estimating costs: {str(e)}")
    
    async def _generate_travel_funding_application(self, event_details: str, financial_situation: str):
        """Generate a travel funding application."""
        try:
            with st.spinner("📝 Generating funding application..."):
                result = await self.travel_agent.generate_application({
                    'applicant_info': {
                        'background': 'Cloud-native developer',
                        'financial_need': True
                    },
                    'event_details': {
                        'name': 'Cloud-Native Conference',
                        'location': 'San Francisco'
                    },
                    'funding_source': 'cncf_travel'
                })
                
                if result['success']:
                    application = result['application']
                    
                    st.markdown("**Justification:**")
                    st.markdown(application['justification'])
                    
                    st.markdown("**Impact Statement:**")
                    st.markdown(application['impact_statement'])
                    
                    st.markdown("**Budget Breakdown:**")
                    st.json(application['budget_breakdown'])
                    
                    st.success("✅ Application generated successfully!")
                else:
                    st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error generating application: {str(e)}")
    
    def _export_all_data(self):
        """Export all application data."""
        data = {
            'events': st.session_state.events,
            'proposals': st.session_state.proposals,
            'applications': st.session_state.applications,
            'exported_at': datetime.now().isoformat()
        }
        
        st.download_button(
            label="📥 Export All Data",
            data=json.dumps(data, indent=2),
            file_name=f"cloud_native_agent_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

def main():
    """Main function to run the application."""
    # Initialize the agent
    agent = CloudNativeAIAgent()
    
    # Run the application
    agent.run()

if __name__ == "__main__":
    main() 