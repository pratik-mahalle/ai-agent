"""
Proposal Generator Agent

Generates compelling talk proposals for cloud-native conferences using historical data.
"""

import json
import random
from typing import Dict, List, Any, Optional
from datetime import datetime
from .base_agent import BaseAgent

class ProposalGeneratorAgent(BaseAgent):
    """Agent for generating talk proposals."""
    
    def __init__(self):
        super().__init__(
            name="ProposalGeneratorAgent",
            description="Generates compelling talk proposals for cloud-native conferences"
        )
        
        # Historical KubeCon data (simplified - in practice, you'd load from a database)
        self.historical_data = self._load_historical_data()
        
        # Proposal templates
        self.templates = self._load_templates()
        
        # Trending topics
        self.trending_topics = [
            "Kubernetes Operators and Custom Resources",
            "Service Mesh Implementation with Istio",
            "GitOps and ArgoCD",
            "Observability with Prometheus and Grafana",
            "Security in Cloud-Native Applications",
            "Multi-cluster Management",
            "Serverless with Knative",
            "Edge Computing with Kubernetes",
            "Machine Learning on Kubernetes",
            "Cost Optimization in Cloud-Native Environments"
        ]
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process proposal generation requests."""
        request_type = request.get('type', 'generate')
        
        if request_type == 'generate':
            return await self.generate_proposal(request)
        elif request_type == 'analyze_trends':
            return await self.analyze_trends(request)
        elif request_type == 'improve_proposal':
            return await self.improve_proposal(request)
        elif request_type == 'suggest_topics':
            return await self.suggest_topics(request)
        else:
            return {
                'success': False,
                'error': f'Unknown request type: {request_type}'
            }
    
    async def generate_proposal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a new talk proposal."""
        try:
            self.log_activity("Starting proposal generation")
            
            # Extract parameters
            topic = request.get('topic')
            speaker_expertise = request.get('speaker_expertise', [])
            target_audience = request.get('target_audience', 'intermediate')
            talk_type = request.get('talk_type', 'session')
            event_context = request.get('event_context', {})
            
            # If no topic provided, suggest one
            if not topic:
                topic = await self._suggest_topic(speaker_expertise, event_context)
            
            # Generate proposal content
            proposal = await self._create_proposal(
                topic=topic,
                speaker_expertise=speaker_expertise,
                target_audience=target_audience,
                talk_type=talk_type,
                event_context=event_context
            )
            
            # Add to conversation history
            self.add_to_history('assistant', f"Generated proposal for topic: {topic}")
            
            return {
                'success': True,
                'proposal': proposal,
                'topic': topic,
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_activity(f"Error generating proposal: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def analyze_trends(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trending topics and successful proposal patterns."""
        try:
            self.log_activity("Analyzing trends")
            
            # Analyze historical data for trends
            trends = self._analyze_historical_trends()
            
            # Get current trending topics
            current_trends = self._get_current_trends()
            
            # Generate insights
            insights = await self._generate_trend_insights(trends, current_trends)
            
            return {
                'success': True,
                'trends': trends,
                'current_trends': current_trends,
                'insights': insights,
                'recommendations': self._generate_recommendations(trends, current_trends)
            }
            
        except Exception as e:
            self.log_activity(f"Error analyzing trends: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def improve_proposal(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Improve an existing proposal."""
        try:
            self.log_activity("Improving proposal")
            
            original_proposal = request.get('proposal')
            if not original_proposal:
                return {
                    'success': False,
                    'error': 'Original proposal is required'
                }
            
            # Analyze the original proposal
            analysis = self._analyze_proposal(original_proposal)
            
            # Generate improvements
            improvements = await self._generate_improvements(original_proposal, analysis)
            
            # Create improved version
            improved_proposal = self._apply_improvements(original_proposal, improvements)
            
            return {
                'success': True,
                'original_proposal': original_proposal,
                'improved_proposal': improved_proposal,
                'analysis': analysis,
                'improvements': improvements
            }
            
        except Exception as e:
            self.log_activity(f"Error improving proposal: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def suggest_topics(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest topics based on speaker expertise and event context."""
        try:
            self.log_activity("Suggesting topics")
            
            speaker_expertise = request.get('speaker_expertise', [])
            event_context = request.get('event_context', {})
            num_suggestions = request.get('num_suggestions', 5)
            
            # Generate topic suggestions
            suggestions = await self._generate_topic_suggestions(
                speaker_expertise, event_context, num_suggestions
            )
            
            return {
                'success': True,
                'suggestions': suggestions,
                'reasoning': self._explain_suggestions(suggestions, speaker_expertise)
            }
            
        except Exception as e:
            self.log_activity(f"Error suggesting topics: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _create_proposal(self, topic: str, speaker_expertise: List[str], 
                             target_audience: str, talk_type: str, 
                             event_context: Dict[str, Any]) -> Dict[str, Any]:
        """Create a complete proposal."""
        
        # Generate title
        title = await self._generate_title(topic, talk_type)
        
        # Generate abstract
        abstract = await self._generate_abstract(topic, target_audience, speaker_expertise)
        
        # Generate learning objectives
        learning_objectives = await self._generate_learning_objectives(topic, target_audience)
        
        # Generate outline
        outline = await self._generate_outline(topic, talk_type)
        
        # Generate speaker bio
        speaker_bio = await self._generate_speaker_bio(speaker_expertise)
        
        # Generate track suggestions
        track_suggestions = self._suggest_tracks(topic)
        
        return {
            'title': title,
            'abstract': abstract,
            'learning_objectives': learning_objectives,
            'outline': outline,
            'speaker_bio': speaker_bio,
            'track_suggestions': track_suggestions,
            'target_audience': target_audience,
            'talk_type': talk_type,
            'estimated_duration': self._estimate_duration(talk_type),
            'tags': self._generate_tags(topic),
            'submission_tips': self._get_submission_tips()
        }
    
    async def _generate_title(self, topic: str, talk_type: str) -> str:
        """Generate an engaging title."""
        prompt = f"""
        Generate an engaging, SEO-friendly title for a {talk_type} talk about {topic}.
        The title should be:
        - Compelling and clickable
        - Include relevant keywords
        - Be 60 characters or less
        - Avoid clickbait
        - Be specific and actionable
        
        Return only the title, nothing else.
        """
        
        return await self.generate_response(prompt)
    
    async def _generate_abstract(self, topic: str, target_audience: str, 
                               speaker_expertise: List[str]) -> str:
        """Generate an abstract."""
        expertise_text = ", ".join(speaker_expertise) if speaker_expertise else "cloud-native technologies"
        
        prompt = f"""
        Write a compelling abstract for a talk about {topic}.
        
        Target audience: {target_audience}
        Speaker expertise: {expertise_text}
        
        The abstract should:
        - Hook the reader in the first sentence
        - Clearly state what attendees will learn
        - Include specific takeaways
        - Be 150-200 words
        - Use active voice
        - Avoid jargon unless necessary
        
        Format as a single paragraph.
        """
        
        return await self.generate_response(prompt)
    
    async def _generate_learning_objectives(self, topic: str, target_audience: str) -> List[str]:
        """Generate learning objectives."""
        prompt = f"""
        Generate 3-5 specific learning objectives for a {target_audience} level talk about {topic}.
        
        Each objective should:
        - Start with an action verb
        - Be specific and measurable
        - Be achievable in the talk duration
        - Be relevant to the target audience
        
        Return as a numbered list.
        """
        
        response = await self.generate_response(prompt)
        # Parse the numbered list into a list of strings
        objectives = [obj.strip() for obj in response.split('\n') if obj.strip() and obj[0].isdigit()]
        return objectives
    
    async def _generate_outline(self, topic: str, talk_type: str) -> List[Dict[str, Any]]:
        """Generate a talk outline."""
        prompt = f"""
        Create a detailed outline for a {talk_type} talk about {topic}.
        
        Include:
        - Introduction (5-10 minutes)
        - Main content sections with time allocations
        - Key points for each section
        - Conclusion and Q&A
        
        Format as a structured outline with time allocations.
        """
        
        response = await self.generate_response(prompt)
        
        # Parse the outline (simplified parsing)
        outline_sections = []
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if 'introduction' in line.lower() or 'intro' in line.lower():
                    current_section = {
                        'title': 'Introduction',
                        'duration': '5-10 minutes',
                        'key_points': []
                    }
                elif 'conclusion' in line.lower():
                    current_section = {
                        'title': 'Conclusion & Q&A',
                        'duration': '5-10 minutes',
                        'key_points': []
                    }
                elif current_section and line:
                    current_section['key_points'].append(line)
                
                if current_section and current_section not in outline_sections:
                    outline_sections.append(current_section)
        
        return outline_sections
    
    async def _generate_speaker_bio(self, speaker_expertise: List[str]) -> str:
        """Generate a speaker bio."""
        expertise_text = ", ".join(speaker_expertise) if speaker_expertise else "cloud-native technologies"
        
        prompt = f"""
        Write a professional speaker bio for someone with expertise in {expertise_text}.
        
        The bio should:
        - Be 2-3 sentences
        - Highlight relevant experience
        - Be engaging and professional
        - Include current role/company if applicable
        - Focus on cloud-native expertise
        """
        
        return await self.generate_response(prompt)
    
    def _suggest_tracks(self, topic: str) -> List[str]:
        """Suggest appropriate tracks for the topic."""
        track_mapping = {
            'kubernetes': ['Kubernetes', 'Application + Development'],
            'observability': ['Observability + Monitoring'],
            'security': ['Security + Identity + Policy'],
            'networking': ['Networking + Edge'],
            'storage': ['Storage + Data'],
            'machine learning': ['Machine Learning + Data'],
            'gitops': ['GitOps + DevOps'],
            'service mesh': ['Networking + Edge', 'Service Mesh'],
            'operators': ['Kubernetes', 'Operators'],
            'cost': ['Cost Management', 'FinOps']
        }
        
        topic_lower = topic.lower()
        suggested_tracks = []
        
        for keyword, tracks in track_mapping.items():
            if keyword in topic_lower:
                suggested_tracks.extend(tracks)
        
        # Remove duplicates and return
        return list(set(suggested_tracks)) if suggested_tracks else ['General']
    
    def _estimate_duration(self, talk_type: str) -> str:
        """Estimate talk duration."""
        duration_map = {
            'session': '30-45 minutes',
            'lightning': '5-10 minutes',
            'workshop': '2-4 hours',
            'panel': '45-60 minutes',
            'keynote': '20-30 minutes'
        }
        return duration_map.get(talk_type, '30-45 minutes')
    
    def _generate_tags(self, topic: str) -> List[str]:
        """Generate relevant tags for the proposal."""
        # Extract keywords from topic
        keywords = topic.lower().split()
        
        # Common cloud-native tags
        common_tags = [
            'kubernetes', 'cncf', 'cloud-native', 'containers', 'microservices',
            'devops', 'gitops', 'observability', 'security', 'networking',
            'storage', 'machine-learning', 'operators', 'service-mesh'
        ]
        
        # Find matching tags
        matching_tags = [tag for tag in common_tags if tag.replace('-', ' ') in topic.lower()]
        
        # Add topic-specific tags
        if 'kubernetes' in topic.lower():
            matching_tags.extend(['k8s', 'orchestration'])
        if 'observability' in topic.lower():
            matching_tags.extend(['monitoring', 'logging', 'tracing'])
        if 'security' in topic.lower():
            matching_tags.extend(['identity', 'policy', 'compliance'])
        
        return list(set(matching_tags))[:10]  # Limit to 10 tags
    
    def _get_submission_tips(self) -> List[str]:
        """Get tips for successful proposal submission."""
        return [
            "Submit early - CFP committees review proposals as they come in",
            "Be specific about what attendees will learn",
            "Include real-world examples and case studies",
            "Clearly state your expertise and experience",
            "Proofread your proposal carefully",
            "Follow the event's submission guidelines exactly",
            "Consider submitting multiple proposals to increase chances",
            "Include links to previous talks or relevant work",
            "Be authentic and passionate about your topic",
            "Address current industry challenges and trends"
        ]
    
    def _load_historical_data(self) -> Dict[str, Any]:
        """Load historical KubeCon data."""
        # In practice, this would load from a database or API
        return {
            'successful_topics': [
                'Kubernetes Operators: Beyond the Basics',
                'Service Mesh Deep Dive: Istio in Production',
                'GitOps: The Future of DevOps',
                'Observability at Scale: Lessons from Production',
                'Security Best Practices for Cloud-Native Applications'
            ],
            'trending_keywords': [
                'operators', 'service-mesh', 'gitops', 'observability', 'security',
                'multi-cluster', 'edge-computing', 'serverless', 'mlops', 'cost-optimization'
            ],
            'rejection_reasons': [
                'Vague or unclear learning objectives',
                'Too broad or shallow content',
                'Missing real-world examples',
                'Poor title or abstract',
                'Inappropriate for target audience'
            ]
        }
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load proposal templates."""
        return {
            'title_templates': [
                "How to {action} {technology} in Production",
                "{technology}: {benefit} for {audience}",
                "Lessons Learned: {experience} with {technology}",
                "Building {solution} with {technology}",
                "The Future of {domain}: {technology} Deep Dive"
            ],
            'abstract_templates': [
                "In this {talk_type}, we'll explore {topic} and demonstrate {benefit}. Attendees will learn {learning_outcomes}.",
                "Join us for a deep dive into {topic}, where we'll share {experience} and provide {takeaways}.",
                "This session covers {topic} from {perspective}, offering {audience} practical insights into {benefit}."
            ]
        }
    
    async def _suggest_topic(self, speaker_expertise: List[str], event_context: Dict[str, Any]) -> str:
        """Suggest a topic based on expertise and context."""
        # Combine trending topics with speaker expertise
        relevant_topics = []
        
        for topic in self.trending_topics:
            topic_lower = topic.lower()
            for expertise in speaker_expertise:
                if expertise.lower() in topic_lower or any(word in topic_lower for word in expertise.lower().split()):
                    relevant_topics.append(topic)
        
        if relevant_topics:
            return random.choice(relevant_topics)
        else:
            return random.choice(self.trending_topics)
    
    def _analyze_historical_trends(self) -> Dict[str, Any]:
        """Analyze historical data for trends."""
        return {
            'popular_topics': self.historical_data['successful_topics'],
            'trending_keywords': self.historical_data['trending_keywords'],
            'common_rejection_reasons': self.historical_data['rejection_reasons']
        }
    
    def _get_current_trends(self) -> List[str]:
        """Get current trending topics."""
        return self.trending_topics
    
    async def _generate_trend_insights(self, trends: Dict[str, Any], current_trends: List[str]) -> List[str]:
        """Generate insights from trend analysis."""
        insights = []
        
        # Analyze popular topics
        if trends['popular_topics']:
            insights.append("Production-focused talks with real-world examples are highly valued")
        
        # Analyze trending keywords
        if 'operators' in trends['trending_keywords']:
            insights.append("Kubernetes Operators continue to be a hot topic")
        
        if 'observability' in trends['trending_keywords']:
            insights.append("Observability and monitoring solutions are in high demand")
        
        # Analyze rejection reasons
        if trends['common_rejection_reasons']:
            insights.append("Clear learning objectives and specific content are crucial for acceptance")
        
        return insights
    
    def _generate_recommendations(self, trends: Dict[str, Any], current_trends: List[str]) -> List[str]:
        """Generate recommendations based on trends."""
        recommendations = [
            "Focus on practical, production-ready solutions",
            "Include real-world case studies and examples",
            "Target intermediate to advanced audiences",
            "Emphasize hands-on learning and actionable takeaways",
            "Stay current with emerging technologies like GitOps and service mesh"
        ]
        
        return recommendations
    
    def _analyze_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a proposal for strengths and weaknesses."""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'suggestions': []
        }
        
        # Analyze title
        title = proposal.get('title', '')
        if len(title) > 60:
            analysis['weaknesses'].append('Title is too long')
        elif len(title) < 20:
            analysis['weaknesses'].append('Title is too short')
        else:
            analysis['strengths'].append('Good title length')
        
        # Analyze abstract
        abstract = proposal.get('abstract', '')
        if len(abstract) < 100:
            analysis['weaknesses'].append('Abstract is too short')
        elif len(abstract) > 300:
            analysis['weaknesses'].append('Abstract is too long')
        else:
            analysis['strengths'].append('Good abstract length')
        
        # Analyze learning objectives
        objectives = proposal.get('learning_objectives', [])
        if len(objectives) < 3:
            analysis['weaknesses'].append('Too few learning objectives')
        elif len(objectives) > 6:
            analysis['weaknesses'].append('Too many learning objectives')
        else:
            analysis['strengths'].append('Good number of learning objectives')
        
        return analysis
    
    async def _generate_improvements(self, proposal: Dict[str, Any], analysis: Dict[str, Any]) -> List[str]:
        """Generate specific improvements for a proposal."""
        improvements = []
        
        for weakness in analysis['weaknesses']:
            if 'title' in weakness.lower():
                improvements.append("Consider shortening the title to under 60 characters")
            elif 'abstract' in weakness.lower():
                improvements.append("Expand the abstract to 150-200 words with more specific details")
            elif 'objectives' in weakness.lower():
                improvements.append("Aim for 3-5 specific, measurable learning objectives")
        
        # Add general improvements
        improvements.extend([
            "Include more specific examples and case studies",
            "Add metrics or data points to support your claims",
            "Consider adding a demo or hands-on component",
            "Make sure the abstract clearly states what attendees will learn"
        ])
        
        return improvements
    
    def _apply_improvements(self, proposal: Dict[str, Any], improvements: List[str]) -> Dict[str, Any]:
        """Apply improvements to create an enhanced proposal."""
        # This would integrate with the AI to actually improve the content
        # For now, return the original with improvement notes
        improved_proposal = proposal.copy()
        improved_proposal['improvement_notes'] = improvements
        return improved_proposal
    
    async def _generate_topic_suggestions(self, speaker_expertise: List[str], 
                                        event_context: Dict[str, Any], 
                                        num_suggestions: int) -> List[Dict[str, Any]]:
        """Generate topic suggestions."""
        suggestions = []
        
        for topic in self.trending_topics[:num_suggestions]:
            relevance_score = self._calculate_topic_relevance(topic, speaker_expertise)
            
            suggestions.append({
                'topic': topic,
                'relevance_score': relevance_score,
                'reasoning': self._explain_topic_relevance(topic, speaker_expertise),
                'estimated_acceptance_chance': min(relevance_score * 10, 95)
            })
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return suggestions
    
    def _calculate_topic_relevance(self, topic: str, speaker_expertise: List[str]) -> float:
        """Calculate relevance score for a topic based on speaker expertise."""
        score = 0.0
        topic_lower = topic.lower()
        
        for expertise in speaker_expertise:
            expertise_lower = expertise.lower()
            if expertise_lower in topic_lower:
                score += 2.0
            elif any(word in topic_lower for word in expertise_lower.split()):
                score += 1.0
        
        return min(score, 10.0)
    
    def _explain_topic_relevance(self, topic: str, speaker_expertise: List[str]) -> str:
        """Explain why a topic is relevant to the speaker's expertise."""
        matching_expertise = []
        
        for expertise in speaker_expertise:
            if expertise.lower() in topic.lower():
                matching_expertise.append(expertise)
        
        if matching_expertise:
            return f"Directly relates to your expertise in {', '.join(matching_expertise)}"
        else:
            return "General cloud-native topic with broad appeal"
    
    def _explain_suggestions(self, suggestions: List[Dict[str, Any]], speaker_expertise: List[str]) -> str:
        """Explain the reasoning behind topic suggestions."""
        if not suggestions:
            return "No specific suggestions available."
        
        top_suggestion = suggestions[0]
        
        if top_suggestion['relevance_score'] >= 7:
            return f"'{top_suggestion['topic']}' is highly relevant to your expertise in {', '.join(speaker_expertise)}"
        elif top_suggestion['relevance_score'] >= 4:
            return f"'{top_suggestion['topic']}' aligns well with your background and current industry trends"
        else:
            return f"'{top_suggestion['topic']}' is a trending topic that would showcase your adaptability and learning" 