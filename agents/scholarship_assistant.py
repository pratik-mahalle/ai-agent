"""
Scholarship Assistant Agent

Assists with scholarship applications for cloud-native events.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from .base_agent import BaseAgent

class ScholarshipAssistantAgent(BaseAgent):
    """Agent for assisting with scholarship applications."""
    
    def __init__(self):
        super().__init__(
            name="ScholarshipAssistantAgent",
            description="Assists with scholarship applications for cloud-native events"
        )
        
        # Scholarship programs
        self.scholarship_programs = {
            'kubecon': {
                'name': 'KubeCon + CloudNativeCon Scholarship',
                'url': 'https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/attend/scholarships/',
                'deadlines': {
                    'early': '3 months before event',
                    'regular': '2 months before event',
                    'late': '1 month before event'
                },
                'requirements': [
                    'Student or early career professional',
                    'Demonstrated interest in cloud-native technologies',
                    'Financial need',
                    'Not previously awarded a scholarship'
                ],
                'coverage': [
                    'Conference registration',
                    'Travel expenses (up to $500)',
                    'Accommodation (shared room)',
                    'Meals during conference'
                ]
            },
            'linux_foundation': {
                'name': 'Linux Foundation Diversity Scholarship',
                'url': 'https://www.linuxfoundation.org/about/diversity-inclusivity/',
                'deadlines': {
                    'early': '4 months before event',
                    'regular': '3 months before event'
                },
                'requirements': [
                    'Underrepresented group in technology',
                    'Demonstrated interest in open source',
                    'Financial need',
                    'Commitment to community involvement'
                ],
                'coverage': [
                    'Conference registration',
                    'Travel expenses',
                    'Accommodation',
                    'Mentorship opportunities'
                ]
            }
        }
        
        # Application templates
        self.templates = self._load_templates()
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process scholarship assistance requests."""
        request_type = request.get('type', 'info')
        
        if request_type == 'info':
            return await self.get_scholarship_info(request)
        elif request_type == 'check_eligibility':
            return await self.check_eligibility(request)
        elif request_type == 'generate_application':
            return await self.generate_application(request)
        elif request_type == 'review_application':
            return await self.review_application(request)
        elif request_type == 'track_deadlines':
            return await self.track_deadlines(request)
        else:
            return {
                'success': False,
                'error': f'Unknown request type: {request_type}'
            }
    
    async def get_scholarship_info(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Get information about available scholarships."""
        try:
            self.log_activity("Getting scholarship information")
            
            event_name = request.get('event_name', '').lower()
            program_type = request.get('program_type', 'all')
            
            if program_type == 'all':
                programs = self.scholarship_programs
            else:
                programs = {k: v for k, v in self.scholarship_programs.items() 
                           if program_type in k}
            
            # Filter by event if specified
            if event_name:
                filtered_programs = {}
                for key, program in programs.items():
                    if event_name in program['name'].lower():
                        filtered_programs[key] = program
                programs = filtered_programs
            
            return {
                'success': True,
                'programs': programs,
                'total_programs': len(programs),
                'next_deadlines': self._get_next_deadlines(programs)
            }
            
        except Exception as e:
            self.log_activity(f"Error getting scholarship info: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def check_eligibility(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Check eligibility for scholarship programs."""
        try:
            self.log_activity("Checking eligibility")
            
            applicant_info = request.get('applicant_info', {})
            program_id = request.get('program_id')
            
            if not program_id or program_id not in self.scholarship_programs:
                return {
                    'success': False,
                    'error': 'Invalid program ID'
                }
            
            program = self.scholarship_programs[program_id]
            requirements = program['requirements']
            
            # Check each requirement
            eligibility_results = []
            overall_eligible = True
            
            for requirement in requirements:
                is_eligible = await self._check_requirement(requirement, applicant_info)
                eligibility_results.append({
                    'requirement': requirement,
                    'eligible': is_eligible,
                    'notes': self._get_requirement_notes(requirement, applicant_info)
                })
                
                if not is_eligible:
                    overall_eligible = False
            
            return {
                'success': True,
                'program': program,
                'eligible': overall_eligible,
                'requirements_check': eligibility_results,
                'recommendations': self._get_eligibility_recommendations(eligibility_results)
            }
            
        except Exception as e:
            self.log_activity(f"Error checking eligibility: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def generate_application(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a scholarship application."""
        try:
            self.log_activity("Generating scholarship application")
            
            applicant_info = request.get('applicant_info', {})
            program_id = request.get('program_id')
            
            if not program_id or program_id not in self.scholarship_programs:
                return {
                    'success': False,
                    'error': 'Invalid program ID'
                }
            
            program = self.scholarship_programs[program_id]
            
            # Generate application components
            personal_statement = await self._generate_personal_statement(applicant_info, program)
            financial_need_statement = await self._generate_financial_statement(applicant_info)
            goals_statement = await self._generate_goals_statement(applicant_info, program)
            
            application = {
                'program': program['name'],
                'personal_statement': personal_statement,
                'financial_need_statement': financial_need_statement,
                'goals_statement': goals_statement,
                'submission_checklist': self._get_submission_checklist(program),
                'tips': self._get_application_tips()
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
    
    async def review_application(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Review a scholarship application."""
        try:
            self.log_activity("Reviewing application")
            
            application = request.get('application', {})
            
            if not application:
                return {
                    'success': False,
                    'error': 'Application content is required'
                }
            
            # Analyze application components
            analysis = {
                'personal_statement': self._analyze_personal_statement(application.get('personal_statement', '')),
                'financial_statement': self._analyze_financial_statement(application.get('financial_need_statement', '')),
                'goals_statement': self._analyze_goals_statement(application.get('goals_statement', '')),
                'overall_score': 0
            }
            
            # Calculate overall score
            scores = [analysis['personal_statement']['score'], 
                     analysis['financial_statement']['score'],
                     analysis['goals_statement']['score']]
            analysis['overall_score'] = sum(scores) / len(scores)
            
            # Generate improvement suggestions
            suggestions = self._generate_improvement_suggestions(analysis)
            
            return {
                'success': True,
                'analysis': analysis,
                'suggestions': suggestions,
                'estimated_chance': self._estimate_acceptance_chance(analysis['overall_score'])
            }
            
        except Exception as e:
            self.log_activity(f"Error reviewing application: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def track_deadlines(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Track scholarship deadlines."""
        try:
            self.log_activity("Tracking deadlines")
            
            upcoming_deadlines = []
            current_date = datetime.now()
            
            for program_id, program in self.scholarship_programs.items():
                for deadline_type, deadline_desc in program['deadlines'].items():
                    # Estimate deadline date (simplified)
                    estimated_date = self._estimate_deadline_date(deadline_desc)
                    
                    if estimated_date and estimated_date > current_date:
                        days_until = (estimated_date - current_date).days
                        
                        upcoming_deadlines.append({
                            'program': program['name'],
                            'program_id': program_id,
                            'deadline_type': deadline_type,
                            'deadline_date': estimated_date.isoformat(),
                            'days_until': days_until,
                            'urgency': 'high' if days_until <= 30 else 'medium' if days_until <= 60 else 'low'
                        })
            
            # Sort by urgency and days until
            upcoming_deadlines.sort(key=lambda x: (x['days_until'], x['urgency']))
            
            return {
                'success': True,
                'upcoming_deadlines': upcoming_deadlines,
                'total_deadlines': len(upcoming_deadlines),
                'urgent_deadlines': [d for d in upcoming_deadlines if d['urgency'] == 'high']
            }
            
        except Exception as e:
            self.log_activity(f"Error tracking deadlines: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _check_requirement(self, requirement: str, applicant_info: Dict[str, Any]) -> bool:
        """Check if applicant meets a specific requirement."""
        requirement_lower = requirement.lower()
        
        if 'student' in requirement_lower:
            return applicant_info.get('is_student', False)
        elif 'early career' in requirement_lower:
            years_experience = applicant_info.get('years_experience', 0)
            return years_experience <= 3
        elif 'financial need' in requirement_lower:
            return applicant_info.get('financial_need', False)
        elif 'underrepresented' in requirement_lower:
            return applicant_info.get('is_underrepresented', False)
        elif 'not previously awarded' in requirement_lower:
            return not applicant_info.get('previously_awarded', False)
        else:
            # Default to true for other requirements
            return True
    
    def _get_requirement_notes(self, requirement: str, applicant_info: Dict[str, Any]) -> str:
        """Get notes about a specific requirement."""
        requirement_lower = requirement.lower()
        
        if 'student' in requirement_lower:
            if applicant_info.get('is_student'):
                return "You meet the student requirement"
            else:
                return "You need to be currently enrolled as a student"
        elif 'early career' in requirement_lower:
            years = applicant_info.get('years_experience', 0)
            if years <= 3:
                return f"You qualify with {years} years of experience"
            else:
                return f"You have {years} years of experience, but early career typically means ≤3 years"
        elif 'financial need' in requirement_lower:
            if applicant_info.get('financial_need'):
                return "You have indicated financial need"
            else:
                return "You need to demonstrate financial need"
        else:
            return "Requirement check completed"
    
    def _get_eligibility_recommendations(self, eligibility_results: List[Dict[str, Any]]) -> List[str]:
        """Get recommendations based on eligibility results."""
        recommendations = []
        
        ineligible_requirements = [r for r in eligibility_results if not r['eligible']]
        
        for req in ineligible_requirements:
            if 'student' in req['requirement'].lower():
                recommendations.append("Consider enrolling in a relevant course or program")
            elif 'early career' in req['requirement'].lower():
                recommendations.append("Look for programs that don't have experience restrictions")
            elif 'financial need' in req['requirement'].lower():
                recommendations.append("Document your financial situation clearly")
            elif 'underrepresented' in req['requirement'].lower():
                recommendations.append("Consider other scholarship programs without diversity requirements")
        
        if not ineligible_requirements:
            recommendations.append("You appear eligible! Focus on writing a strong application")
        
        return recommendations
    
    async def _generate_personal_statement(self, applicant_info: Dict[str, Any], program: Dict[str, Any]) -> str:
        """Generate a personal statement."""
        prompt = f"""
        Write a compelling personal statement for a {program['name']} scholarship application.
        
        Applicant background:
        - Experience: {applicant_info.get('years_experience', 0)} years
        - Current role: {applicant_info.get('current_role', 'Not specified')}
        - Education: {applicant_info.get('education', 'Not specified')}
        - Interests: {', '.join(applicant_info.get('interests', []))}
        
        The statement should:
        - Be 300-500 words
        - Show passion for cloud-native technologies
        - Demonstrate how the scholarship would help
        - Include specific examples and achievements
        - Be personal and authentic
        """
        
        return await self.generate_response(prompt)
    
    async def _generate_financial_statement(self, applicant_info: Dict[str, Any]) -> str:
        """Generate a financial need statement."""
        prompt = f"""
        Write a financial need statement for a scholarship application.
        
        Financial situation:
        - Income: {applicant_info.get('income', 'Not specified')}
        - Expenses: {applicant_info.get('expenses', 'Not specified')}
        - Other funding sources: {applicant_info.get('other_funding', 'None')}
        
        The statement should:
        - Be honest and specific about financial need
        - Explain why the scholarship is necessary
        - Show how the funds would be used
        - Be professional and respectful
        - Be 150-250 words
        """
        
        return await self.generate_response(prompt)
    
    async def _generate_goals_statement(self, applicant_info: Dict[str, Any], program: Dict[str, Any]) -> str:
        """Generate a goals statement."""
        prompt = f"""
        Write a goals statement for a {program['name']} scholarship application.
        
        Applicant goals:
        - Short-term goals: {', '.join(applicant_info.get('short_term_goals', []))}
        - Long-term goals: {', '.join(applicant_info.get('long_term_goals', []))}
        - How attending would help: {applicant_info.get('how_attending_helps', 'Not specified')}
        
        The statement should:
        - Be 200-300 words
        - Show clear, achievable goals
        - Explain how the event helps achieve those goals
        - Demonstrate commitment to the community
        - Include specific plans for sharing knowledge
        """
        
        return await self.generate_response(prompt)
    
    def _get_submission_checklist(self, program: Dict[str, Any]) -> List[str]:
        """Get a checklist for application submission."""
        return [
            "Personal statement completed",
            "Financial need statement completed",
            "Goals statement completed",
            "Resume/CV updated",
            "References identified",
            "All required documents gathered",
            "Application form filled out completely",
            "Proofread all materials",
            "Submit before deadline",
            "Keep copies of all submitted materials"
        ]
    
    def _get_application_tips(self) -> List[str]:
        """Get tips for successful scholarship applications."""
        return [
            "Start early - don't wait until the last minute",
            "Be specific about your financial need",
            "Show passion for the technology and community",
            "Include concrete examples and achievements",
            "Explain how you'll give back to the community",
            "Proofread everything carefully",
            "Follow all formatting requirements",
            "Submit complete applications only",
            "Keep copies of all submitted materials",
            "Follow up if you don't hear back within the expected timeframe"
        ]
    
    def _analyze_personal_statement(self, statement: str) -> Dict[str, Any]:
        """Analyze a personal statement."""
        if not statement:
            return {'score': 0, 'strengths': [], 'weaknesses': ['No statement provided']}
        
        score = 5.0  # Base score
        strengths = []
        weaknesses = []
        
        # Check length
        word_count = len(statement.split())
        if 300 <= word_count <= 500:
            strengths.append("Good length")
        elif word_count < 300:
            weaknesses.append("Too short")
            score -= 1
        elif word_count > 500:
            weaknesses.append("Too long")
            score -= 0.5
        
        # Check for key elements
        if 'cloud' in statement.lower() or 'kubernetes' in statement.lower():
            strengths.append("Mentions relevant technologies")
        else:
            weaknesses.append("Missing technology focus")
            score -= 1
        
        if 'passion' in statement.lower() or 'excited' in statement.lower():
            strengths.append("Shows enthusiasm")
        else:
            weaknesses.append("Could show more passion")
            score -= 0.5
        
        return {
            'score': max(0, score),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'word_count': word_count
        }
    
    def _analyze_financial_statement(self, statement: str) -> Dict[str, Any]:
        """Analyze a financial need statement."""
        if not statement:
            return {'score': 0, 'strengths': [], 'weaknesses': ['No statement provided']}
        
        score = 5.0
        strengths = []
        weaknesses = []
        
        # Check length
        word_count = len(statement.split())
        if 150 <= word_count <= 250:
            strengths.append("Good length")
        elif word_count < 150:
            weaknesses.append("Too short")
            score -= 1
        elif word_count > 250:
            weaknesses.append("Too long")
            score -= 0.5
        
        # Check for financial need indicators
        if any(word in statement.lower() for word in ['need', 'cannot afford', 'financial']):
            strengths.append("Clearly states financial need")
        else:
            weaknesses.append("Doesn't clearly state financial need")
            score -= 1
        
        return {
            'score': max(0, score),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'word_count': word_count
        }
    
    def _analyze_goals_statement(self, statement: str) -> Dict[str, Any]:
        """Analyze a goals statement."""
        if not statement:
            return {'score': 0, 'strengths': [], 'weaknesses': ['No statement provided']}
        
        score = 5.0
        strengths = []
        weaknesses = []
        
        # Check length
        word_count = len(statement.split())
        if 200 <= word_count <= 300:
            strengths.append("Good length")
        elif word_count < 200:
            weaknesses.append("Too short")
            score -= 1
        elif word_count > 300:
            weaknesses.append("Too long")
            score -= 0.5
        
        # Check for goal indicators
        if any(word in statement.lower() for word in ['goal', 'plan', 'achieve', 'learn']):
            strengths.append("Mentions specific goals")
        else:
            weaknesses.append("Missing specific goals")
            score -= 1
        
        return {
            'score': max(0, score),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'word_count': word_count
        }
    
    def _generate_improvement_suggestions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        for component, component_analysis in analysis.items():
            if component == 'overall_score':
                continue
            
            for weakness in component_analysis.get('weaknesses', []):
                if 'short' in weakness.lower():
                    suggestions.append(f"Expand your {component.replace('_', ' ')} with more details")
                elif 'long' in weakness.lower():
                    suggestions.append(f"Make your {component.replace('_', ' ')} more concise")
                elif 'missing' in weakness.lower():
                    suggestions.append(f"Add more specific content to your {component.replace('_', ' ')}")
        
        return suggestions
    
    def _estimate_acceptance_chance(self, overall_score: float) -> str:
        """Estimate acceptance chance based on overall score."""
        if overall_score >= 8:
            return "High (80-90%)"
        elif overall_score >= 6:
            return "Good (60-80%)"
        elif overall_score >= 4:
            return "Fair (40-60%)"
        else:
            return "Low (20-40%)"
    
    def _get_next_deadlines(self, programs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get the next deadlines for programs."""
        deadlines = []
        
        for program_id, program in programs.items():
            for deadline_type, deadline_desc in program['deadlines'].items():
                estimated_date = self._estimate_deadline_date(deadline_desc)
                if estimated_date:
                    deadlines.append({
                        'program': program['name'],
                        'type': deadline_type,
                        'date': estimated_date.isoformat(),
                        'description': deadline_desc
                    })
        
        # Sort by date
        deadlines.sort(key=lambda x: x['date'])
        return deadlines[:5]  # Return top 5
    
    def _estimate_deadline_date(self, deadline_desc: str) -> Optional[datetime]:
        """Estimate the actual date from a deadline description."""
        # This is a simplified estimation - in practice, you'd parse actual dates
        current_date = datetime.now()
        
        if '3 months' in deadline_desc:
            return current_date + timedelta(days=90)
        elif '2 months' in deadline_desc:
            return current_date + timedelta(days=60)
        elif '1 month' in deadline_desc:
            return current_date + timedelta(days=30)
        elif '4 months' in deadline_desc:
            return current_date + timedelta(days=120)
        
        return None
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load application templates."""
        return {
            'personal_statement_template': """
            I am passionate about {technology} and have been working with {specific_experience} for {duration}. 
            My interest in cloud-native technologies began when {motivation_story}. 
            Attending {event_name} would allow me to {specific_benefits} and help me achieve my goal of {long_term_goal}.
            """,
            'financial_statement_template': """
            As a {role} with {income_situation}, I face significant financial constraints that make attending {event_name} challenging. 
            My current expenses include {expenses}, leaving limited funds for professional development. 
            This scholarship would enable me to {specific_use_of_funds} and advance my career in cloud-native technologies.
            """,
            'goals_statement_template': """
            My short-term goal is to {short_term_goal}, and attending {event_name} would provide me with {specific_skills}. 
            In the long term, I aim to {long_term_goal} and contribute to the cloud-native community by {contribution_plan}. 
            I plan to share my learnings through {sharing_method}.
            """
        } 