"""
Travel Funding Assistant Agent

Assists with travel funding applications for cloud-native events.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_agent import BaseAgent

class TravelFundingAssistantAgent(BaseAgent):
    """Agent for assisting with travel funding applications."""
    
    def __init__(self):
        super().__init__(
            name="TravelFundingAssistantAgent",
            description="Assists with travel funding applications for cloud-native events"
        )
        
        # Travel funding sources
        self.funding_sources = {
            'cncf_travel': {
                'name': 'CNCF Travel Fund',
                'url': 'https://www.cncf.io/community/travel-fund/',
                'max_amount': 2000,
                'currency': 'USD',
                'requirements': [
                    'CNCF project contributor',
                    'Active participation in community',
                    'Financial need',
                    'Clear justification for travel'
                ],
                'coverage': [
                    'Airfare',
                    'Accommodation',
                    'Ground transportation',
                    'Meals (per diem)'
                ],
                'deadlines': {
                    'application': '6 weeks before travel',
                    'reimbursement': '30 days after travel'
                }
            },
            'linux_foundation_travel': {
                'name': 'Linux Foundation Travel Fund',
                'url': 'https://www.linuxfoundation.org/about/diversity-inclusivity/',
                'max_amount': 1500,
                'currency': 'USD',
                'requirements': [
                    'Underrepresented group in technology',
                    'Demonstrated community involvement',
                    'Financial need',
                    'Event participation (speaking/volunteering)'
                ],
                'coverage': [
                    'Travel expenses',
                    'Accommodation',
                    'Conference registration'
                ],
                'deadlines': {
                    'application': '8 weeks before travel',
                    'reimbursement': '45 days after travel'
                }
            },
            'event_specific': {
                'name': 'Event-Specific Travel Grants',
                'url': 'varies',
                'max_amount': 1000,
                'currency': 'USD',
                'requirements': [
                    'Event participation',
                    'Financial need',
                    'Geographic diversity',
                    'Community contribution'
                ],
                'coverage': [
                    'Partial travel costs',
                    'Accommodation support'
                ],
                'deadlines': {
                    'application': 'varies by event',
                    'reimbursement': 'varies by event'
                }
            }
        }
        
        # Cost estimation data
        self.cost_estimates = {
            'airfare': {
                'domestic': {'min': 300, 'max': 800, 'avg': 550},
                'international': {'min': 800, 'max': 2000, 'avg': 1400}
            },
            'accommodation': {
                'budget': {'per_night': 80, 'description': 'Hostel or shared accommodation'},
                'standard': {'per_night': 150, 'description': 'Hotel room'},
                'premium': {'per_night': 250, 'description': 'Conference hotel'}
            },
            'meals': {
                'per_day': 75,
                'description': 'Three meals plus incidentals'
            },
            'transportation': {
                'airport_transfer': 50,
                'daily_transport': 25,
                'description': 'Public transportation and rideshare'
            }
        }
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process travel funding assistance requests."""
        request_type = request.get('type', 'info')
        
        if request_type == 'info':
            return await self.get_funding_info(request)
        elif request_type == 'estimate_costs':
            return await self.estimate_costs(request)
        elif request_type == 'generate_application':
            return await self.generate_application(request)
        elif request_type == 'budget_planning':
            return await self.plan_budget(request)
        elif request_type == 'track_applications':
            return await self.track_applications(request)
        else:
            return {
                'success': False,
                'error': f'Unknown request type: {request_type}'
            }
    
    async def get_funding_info(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about available travel funding sources."""
        try:
            self.log_activity("Getting travel funding information")
            
            event_location = request.get('event_location', '').lower()
            applicant_type = request.get('applicant_type', 'all')
            
            # Filter funding sources
            if applicant_type == 'all':
                sources = self.funding_sources
            else:
                sources = {k: v for k, v in self.funding_sources.items() 
                          if applicant_type in k or 'general' in k}
            
            # Add eligibility information
            for source_id, source in sources.items():
                source['eligibility_check'] = await self._check_source_eligibility(source, request)
            
            return {
                'success': True,
                'funding_sources': sources,
                'total_sources': len(sources),
                'recommendations': self._get_funding_recommendations(sources, request)
            }
            
        except Exception as e:
            self.log_activity(f"Error getting funding info: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def estimate_costs(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate travel costs for an event."""
        try:
            self.log_activity("Estimating travel costs")
            
            event_details = request.get('event_details', {})
            travel_preferences = request.get('travel_preferences', {})
            
            # Extract key information
            event_location = event_details.get('location', '')
            event_duration = event_details.get('duration_days', 3)
            departure_location = travel_preferences.get('departure_location', '')
            accommodation_preference = travel_preferences.get('accommodation', 'standard')
            
            # Calculate costs
            airfare_cost = self._estimate_airfare(departure_location, event_location)
            accommodation_cost = self._estimate_accommodation(event_duration, accommodation_preference)
            meals_cost = self._estimate_meals(event_duration)
            transportation_cost = self._estimate_transportation(event_duration)
            
            total_cost = airfare_cost + accommodation_cost + meals_cost + transportation_cost
            
            cost_breakdown = {
                'airfare': {
                    'amount': airfare_cost,
                    'description': f'Round-trip from {departure_location} to {event_location}',
                    'estimate_confidence': 'medium'
                },
                'accommodation': {
                    'amount': accommodation_cost,
                    'description': f'{event_duration} nights at {accommodation_preference} level',
                    'estimate_confidence': 'high'
                },
                'meals': {
                    'amount': meals_cost,
                    'description': f'{event_duration} days of meals and incidentals',
                    'estimate_confidence': 'high'
                },
                'transportation': {
                    'amount': transportation_cost,
                    'description': f'Local transportation for {event_duration} days',
                    'estimate_confidence': 'medium'
                }
            }
            
            return {
                'success': True,
                'total_cost': total_cost,
                'cost_breakdown': cost_breakdown,
                'currency': 'USD',
                'estimated_at': datetime.now().isoformat(),
                'cost_saving_tips': self._get_cost_saving_tips(cost_breakdown)
            }
            
        except Exception as e:
            self.log_activity(f"Error estimating costs: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_application(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a travel funding application."""
        try:
            self.log_activity("Generating travel funding application")
            
            applicant_info = request.get('applicant_info', {})
            event_details = request.get('event_details', {})
            funding_source = request.get('funding_source')
            
            if not funding_source or funding_source not in self.funding_sources:
                return {
                    'success': False,
                    'error': 'Invalid funding source'
                }
            
            source_info = self.funding_sources[funding_source]
            
            # Generate application components
            justification = await self._generate_justification(applicant_info, event_details, source_info)
            budget_breakdown = await self._generate_budget_breakdown(request)
            impact_statement = await self._generate_impact_statement(applicant_info, event_details)
            
            application = {
                'funding_source': source_info['name'],
                'justification': justification,
                'budget_breakdown': budget_breakdown,
                'impact_statement': impact_statement,
                'submission_requirements': self._get_submission_requirements(source_info),
                'deadlines': source_info['deadlines']
            }
            
            return {
                'success': True,
                'application': application,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_activity(f"Error generating application: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def plan_budget(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Help plan a budget for travel funding."""
        try:
            self.log_activity("Planning budget")
            
            total_budget = request.get('total_budget', 0)
            event_details = request.get('event_details', {})
            funding_sources = request.get('funding_sources', [])
            
            # Calculate total available funding
            total_funding = sum(
                self.funding_sources.get(source, {}).get('max_amount', 0)
                for source in funding_sources
            )
            
            # Estimate costs
            cost_estimate = await self.estimate_costs({
                'event_details': event_details,
                'travel_preferences': request.get('travel_preferences', {})
            })
            
            if not cost_estimate['success']:
                return cost_estimate
            
            estimated_cost = cost_estimate['total_cost']
            
            # Calculate gap
            funding_gap = estimated_cost - total_funding
            
            # Generate budget plan
            budget_plan = {
                'estimated_cost': estimated_cost,
                'available_funding': total_funding,
                'funding_gap': funding_gap,
                'is_affordable': funding_gap <= 0,
                'recommendations': self._get_budget_recommendations(funding_gap, estimated_cost),
                'cost_optimization': self._get_cost_optimization_suggestions(cost_estimate['cost_breakdown'])
            }
            
            return {
                'success': True,
                'budget_plan': budget_plan,
                'cost_breakdown': cost_estimate['cost_breakdown']
            }
            
        except Exception as e:
            self.log_activity(f"Error planning budget: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def track_applications(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Track travel funding applications."""
        try:
            self.log_activity("Tracking applications")
            
            # This would typically integrate with a database
            # For now, return a template structure
            applications = request.get('applications', [])
            
            tracked_applications = []
            for app in applications:
                status = self._determine_application_status(app)
                tracked_applications.append({
                    'funding_source': app.get('funding_source'),
                    'event': app.get('event'),
                    'submission_date': app.get('submission_date'),
                    'status': status,
                    'next_action': self._get_next_action(status, app),
                    'deadline': app.get('deadline')
                })
            
            return {
                'success': True,
                'applications': tracked_applications,
                'summary': {
                    'total_applications': len(tracked_applications),
                    'pending': len([a for a in tracked_applications if a['status'] == 'pending']),
                    'approved': len([a for a in tracked_applications if a['status'] == 'approved']),
                    'rejected': len([a for a in tracked_applications if a['status'] == 'rejected'])
                }
            }
            
        except Exception as e:
            self.log_activity(f"Error tracking applications: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _check_source_eligibility(self, source: Dict[str, Any], request: Dict[str, Any]) -> Dict[str, Any]:
        """Check eligibility for a funding source."""
        applicant_info = request.get('applicant_info', {})
        requirements = source.get('requirements', [])
        
        eligibility_results = []
        overall_eligible = True
        
        for requirement in requirements:
            is_eligible = await self._check_funding_requirement(requirement, applicant_info)
            eligibility_results.append({
                'requirement': requirement,
                'eligible': is_eligible,
                'notes': self._get_funding_requirement_notes(requirement, applicant_info)
            })
            
            if not is_eligible:
                overall_eligible = False
        
        return {
            'eligible': overall_eligible,
            'requirements_check': eligibility_results
        }
    
    async def _check_funding_requirement(self, requirement: str, applicant_info: Dict[str, Any]) -> bool:
        """Check if applicant meets a funding requirement."""
        requirement_lower = requirement.lower()
        
        if 'contributor' in requirement_lower:
            return applicant_info.get('is_contributor', False)
        elif 'community' in requirement_lower:
            return applicant_info.get('community_involvement', False)
        elif 'financial need' in requirement_lower:
            return applicant_info.get('financial_need', False)
        elif 'underrepresented' in requirement_lower:
            return applicant_info.get('is_underrepresented', False)
        elif 'participation' in requirement_lower:
            return applicant_info.get('event_participation', False)
        else:
            return True
    
    def _get_funding_requirement_notes(self, requirement: str, applicant_info: Dict[str, Any]) -> str:
        """Get notes about a funding requirement."""
        requirement_lower = requirement.lower()
        
        if 'contributor' in requirement_lower:
            if applicant_info.get('is_contributor'):
                return "You are a project contributor"
            else:
                return "You need to contribute to CNCF projects"
        elif 'community' in requirement_lower:
            if applicant_info.get('community_involvement'):
                return "You have community involvement"
            else:
                return "You need to demonstrate community involvement"
        else:
            return "Requirement check completed"
    
    def _get_funding_recommendations(self, sources: Dict[str, Any], request: Dict[str, Any]) -> List[str]:
        """Get recommendations for funding sources."""
        recommendations = []
        
        eligible_sources = [s for s in sources.values() if s.get('eligibility_check', {}).get('eligible', False)]
        
        if eligible_sources:
            recommendations.append(f"You are eligible for {len(eligible_sources)} funding sources")
            
            # Recommend highest amount first
            eligible_sources.sort(key=lambda x: x.get('max_amount', 0), reverse=True)
            top_source = eligible_sources[0]
            recommendations.append(f"Apply to {top_source['name']} first (up to ${top_source['max_amount']})")
        else:
            recommendations.append("Consider alternative funding sources or cost-saving measures")
        
        return recommendations
    
    def _estimate_airfare(self, departure: str, destination: str) -> float:
        """Estimate airfare costs."""
        # Simplified estimation - in practice, you'd use a flight API
        if not departure or not destination:
            return 600  # Default estimate
        
        # Check if domestic or international
        is_domestic = self._is_domestic_flight(departure, destination)
        
        if is_domestic:
            return self.cost_estimates['airfare']['domestic']['avg']
        else:
            return self.cost_estimates['airfare']['international']['avg']
    
    def _estimate_accommodation(self, duration: int, preference: str) -> float:
        """Estimate accommodation costs."""
        nightly_rate = self.cost_estimates['accommodation'].get(preference, {}).get('per_night', 150)
        return nightly_rate * duration
    
    def _estimate_meals(self, duration: int) -> float:
        """Estimate meal costs."""
        daily_rate = self.cost_estimates['meals']['per_day']
        return daily_rate * duration
    
    def _estimate_transportation(self, duration: int) -> float:
        """Estimate transportation costs."""
        airport_transfer = self.cost_estimates['transportation']['airport_transfer']
        daily_transport = self.cost_estimates['transportation']['daily_transport']
        return airport_transfer + (daily_transport * duration)
    
    def _is_domestic_flight(self, departure: str, destination: str) -> bool:
        """Check if flight is domestic (simplified)."""
        # This is a simplified check - in practice, you'd use a proper country/region database
        us_cities = ['new york', 'san francisco', 'chicago', 'los angeles', 'boston', 'seattle']
        return any(city in departure.lower() for city in us_cities) and any(city in destination.lower() for city in us_cities)
    
    def _get_cost_saving_tips(self, cost_breakdown: Dict[str, Any]) -> List[str]:
        """Get cost-saving tips based on cost breakdown."""
        tips = []
        
        airfare = cost_breakdown.get('airfare', {}).get('amount', 0)
        accommodation = cost_breakdown.get('accommodation', {}).get('amount', 0)
        
        if airfare > 800:
            tips.append("Consider booking flights 2-3 months in advance for better rates")
        
        if accommodation > 200:
            tips.append("Look for shared accommodation or conference hotel discounts")
        
        tips.extend([
            "Use public transportation instead of rideshare when possible",
            "Pack snacks to reduce meal costs",
            "Check for student or group discounts",
            "Consider staying with local community members"
        ])
        
        return tips
    
    async def _generate_justification(self, applicant_info: Dict[str, Any], 
                                    event_details: Dict[str, Any], 
                                    source_info: Dict[str, Any]) -> str:
        """Generate a justification for travel funding."""
        prompt = f"""
        Write a compelling justification for travel funding to attend {event_details.get('name', 'the event')}.
        
        Applicant background:
        - Role: {applicant_info.get('current_role', 'Not specified')}
        - Experience: {applicant_info.get('years_experience', 0)} years
        - Community involvement: {applicant_info.get('community_involvement', 'Not specified')}
        
        Event details:
        - Location: {event_details.get('location', 'Not specified')}
        - Duration: {event_details.get('duration_days', 0)} days
        - Participation: {event_details.get('participation_type', 'Not specified')}
        
        Funding source: {source_info['name']}
        Maximum amount: ${source_info.get('max_amount', 0)}
        
        The justification should:
        - Be 200-300 words
        - Explain why the travel is necessary
        - Show how it benefits the community
        - Demonstrate financial need
        - Be specific and compelling
        """
        
        return await self.generate_response(prompt)
    
    async def _generate_budget_breakdown(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a detailed budget breakdown."""
        cost_estimate = await self.estimate_costs(request)
        
        if not cost_estimate['success']:
            return {}
        
        return {
            'total_requested': cost_estimate['total_cost'],
            'breakdown': cost_estimate['cost_breakdown'],
            'justification': 'Detailed cost breakdown based on current market rates'
        }
    
    async def _generate_impact_statement(self, applicant_info: Dict[str, Any], 
                                       event_details: Dict[str, Any]) -> str:
        """Generate an impact statement."""
        prompt = f"""
        Write an impact statement explaining how attending {event_details.get('name', 'this event')} will benefit the community.
        
        Applicant background:
        - Role: {applicant_info.get('current_role', 'Not specified')}
        - Community involvement: {applicant_info.get('community_involvement', 'Not specified')}
        - Plans for sharing knowledge: {applicant_info.get('knowledge_sharing_plans', 'Not specified')}
        
        The impact statement should:
        - Be 150-200 words
        - Explain specific benefits to the community
        - Include plans for sharing knowledge
        - Show long-term impact
        - Be realistic and achievable
        """
        
        return await self.generate_response(prompt)
    
    def _get_submission_requirements(self, source_info: Dict[str, Any]) -> List[str]:
        """Get submission requirements for a funding source."""
        return [
            "Completed application form",
            "Detailed budget breakdown",
            "Justification statement",
            "Impact statement",
            "Resume/CV",
            "References (if required)",
            "Proof of event participation",
            "Financial need documentation"
        ]
    
    def _get_budget_recommendations(self, funding_gap: float, total_cost: float) -> List[str]:
        """Get recommendations based on budget gap."""
        recommendations = []
        
        if funding_gap <= 0:
            recommendations.append("Your funding sources cover the estimated costs")
        elif funding_gap <= 500:
            recommendations.append("Consider cost-saving measures to reduce the gap")
            recommendations.append("Look for additional funding sources")
        else:
            recommendations.append("Significant funding gap - consider multiple funding sources")
            recommendations.append("Explore cost-saving alternatives")
            recommendations.append("Consider partial funding or self-funding the difference")
        
        return recommendations
    
    def _get_cost_optimization_suggestions(self, cost_breakdown: Dict[str, Any]) -> List[str]:
        """Get suggestions for cost optimization."""
        suggestions = []
        
        airfare = cost_breakdown.get('airfare', {}).get('amount', 0)
        accommodation = cost_breakdown.get('accommodation', {}).get('amount', 0)
        
        if airfare > 600:
            suggestions.append("Book flights early and consider alternative airports")
        
        if accommodation > 150:
            suggestions.append("Look for shared accommodation or extended stay options")
        
        suggestions.extend([
            "Use public transportation instead of rideshare",
            "Pack meals when possible",
            "Check for conference discounts on accommodation",
            "Consider staying with local community members"
        ])
        
        return suggestions
    
    def _determine_application_status(self, application: Dict[str, Any]) -> str:
        """Determine the status of an application."""
        # This would typically check against a database
        # For now, return a default status
        return application.get('status', 'pending')
    
    def _get_next_action(self, status: str, application: Dict[str, Any]) -> str:
        """Get the next action based on application status."""
        if status == 'pending':
            return "Wait for review decision"
        elif status == 'approved':
            return "Submit reimbursement documentation"
        elif status == 'rejected':
            return "Consider alternative funding sources"
        else:
            return "Check application portal for updates" 