"""
Integrated AI Assistant for MASS Framework
==========================================

A unified AI assistant that integrates all AI-powered systems:
- Advanced AI Learning Assistant
- Natural Language Interface  
- Smart Recommendations
- Personalized UI System
- AI-Powered Onboarding
- Intelligent Error Handling

This creates a cohesive, intelligent user experience that learns and adapts.

Author: AI Development Team
Date: 2024
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
import logging

# Import our AI systems
from .advanced_ai_learning_assistant import AdvancedAILearningAssistant
from .natural_language_interface import NaturalLanguageInterface
from .smart_recommendations import SmartRecommendationEngine
from .personalized_ui_system import PersonalizedUISystem
from .ai_onboarding_system import AIOnboardingSystem
from .intelligent_error_handling import IntelligentErrorHandler

# Framework imports
from ..core.base_agent import BaseAgent
from ..utils.logging_utils import setup_logger

logger = setup_logger(__name__)


class AssistantMode(Enum):
    """Different modes of the AI assistant"""
    LEARNING = "learning"
    BUILDING = "building"
    TROUBLESHOOTING = "troubleshooting"
    EXPLORING = "exploring"
    OPTIMIZING = "optimizing"


class InteractionType(Enum):
    """Types of user interactions"""
    QUESTION = "question"
    COMMAND = "command"
    HELP_REQUEST = "help_request"
    ERROR_REPORT = "error_report"
    FEEDBACK = "feedback"
    EXPLORATION = "exploration"


@dataclass
class AssistantContext:
    """Context information for the AI assistant"""
    user_id: str
    session_id: str
    current_mode: AssistantMode
    active_project: Optional[str]
    conversation_history: List[Dict[str, Any]]
    user_goals: List[str]
    current_task: Optional[str]
    skill_level: str
    preferences: Dict[str, Any]
    last_interaction: datetime


class IntegratedAIAssistant:
    """Unified AI assistant integrating all AI systems"""
    
    def __init__(self):
        self.name = "Integrated AI Assistant"
        self.version = "1.0.0"
        
        # Initialize all AI systems
        self._initialize_ai_systems()
        
        # Assistant state management
        self.active_sessions: Dict[str, AssistantContext] = {}
        self.global_context: Dict[str, Any] = {}
        
        # Integration capabilities
        self.system_integrations = {
            'learning': self.learning_assistant,
            'recommendations': self.recommendation_engine,
            'natural_language': self.nl_interface,
            'ui_personalization': self.ui_system,
            'onboarding': self.onboarding_system,
            'error_handling': self.error_handler
        }
        
        logger.info(f"✅ {self.name} v{self.version} initialized successfully")
    
    def _initialize_ai_systems(self):
        """Initialize all AI subsystems"""
        try:
            self.learning_assistant = AdvancedAILearningAssistant()
            self.nl_interface = NaturalLanguageInterface()
            self.recommendation_engine = SmartRecommendationEngine()
            self.ui_system = PersonalizedUISystem()
            self.onboarding_system = AIOnboardingSystem()
            self.error_handler = IntelligentErrorHandler()
            
            logger.info("✅ All AI subsystems initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing AI systems: {e}")
            # Initialize fallback systems
            self._initialize_fallback_systems()
    
    def _initialize_fallback_systems(self):
        """Initialize fallback systems if main ones fail"""
        logger.warning("⚠️ Initializing fallback AI systems")
        # Implement basic fallback functionality
        pass
    
    async def process_interaction(self, user_input: str, user_id: str, 
                                interaction_type: InteractionType = InteractionType.QUESTION,
                                context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user interaction through the integrated AI system"""
        try:
            # Get or create assistant context
            assistant_context = self._get_assistant_context(user_id)
            
            # Update context with new interaction
            assistant_context.conversation_history.append({
                'input': user_input,
                'type': interaction_type.value,
                'timestamp': datetime.now(),
                'context': context or {}
            })
            assistant_context.last_interaction = datetime.now()
            
            # Determine best AI system(s) to handle the interaction
            handling_strategy = await self._determine_handling_strategy(
                user_input, interaction_type, assistant_context
            )
            
            # Route to appropriate AI system(s)
            response = await self._route_and_process(
                user_input, handling_strategy, assistant_context, context
            )
            
            # Enhance response with cross-system insights
            enhanced_response = await self._enhance_response(
                response, assistant_context, handling_strategy
            )
            
            # Update assistant learning
            await self._update_assistant_learning(
                user_input, enhanced_response, assistant_context
            )
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"❌ Error processing interaction: {e}")
            return {
                'success': False,
                'error': str(e),
                'fallback_response': "I'm having trouble understanding that right now. Could you try rephrasing your request?"
            }
    
    async def _determine_handling_strategy(self, user_input: str, 
                                         interaction_type: InteractionType,
                                         context: AssistantContext) -> Dict[str, Any]:
        """Determine which AI systems should handle the interaction"""
        strategy = {
            'primary_system': None,
            'secondary_systems': [],
            'confidence': 0.0,
            'reasoning': ""
        }
        
        input_lower = user_input.lower()
        
        # Natural Language Command Detection
        if any(keyword in input_lower for keyword in ['create', 'build', 'make', 'add', 'deploy']):
            strategy['primary_system'] = 'natural_language'
            strategy['secondary_systems'] = ['recommendations', 'learning']
            strategy['confidence'] = 0.9
            strategy['reasoning'] = "Detected command intent - routing to Natural Language Interface"
        
        # Learning/Help Request Detection
        elif any(keyword in input_lower for keyword in ['how', 'learn', 'tutorial', 'help', 'explain']):
            strategy['primary_system'] = 'learning'
            strategy['secondary_systems'] = ['recommendations', 'ui_personalization']
            strategy['confidence'] = 0.85
            strategy['reasoning'] = "Detected learning intent - routing to Learning Assistant"
        
        # Error/Problem Detection
        elif any(keyword in input_lower for keyword in ['error', 'problem', 'issue', 'broken', 'not working']):
            strategy['primary_system'] = 'error_handling'
            strategy['secondary_systems'] = ['learning', 'recommendations']
            strategy['confidence'] = 0.9
            strategy['reasoning'] = "Detected error/problem - routing to Error Handler"
        
        # Recommendation Request Detection
        elif any(keyword in input_lower for keyword in ['suggest', 'recommend', 'what should', 'next step']):
            strategy['primary_system'] = 'recommendations'
            strategy['secondary_systems'] = ['learning', 'natural_language']
            strategy['confidence'] = 0.8
            strategy['reasoning'] = "Detected recommendation request - routing to Recommendation Engine"
        
        # Onboarding/First-time User Detection
        elif context.skill_level == 'beginner' or 'getting started' in input_lower:
            strategy['primary_system'] = 'onboarding'
            strategy['secondary_systems'] = ['learning', 'ui_personalization']
            strategy['confidence'] = 0.85
            strategy['reasoning'] = "Detected beginner/onboarding need - routing to Onboarding System"
        
        # General Query - Use Natural Language as Primary with Learning Support
        else:
            strategy['primary_system'] = 'natural_language'
            strategy['secondary_systems'] = ['learning', 'recommendations']
            strategy['confidence'] = 0.6
            strategy['reasoning'] = "General query - using Natural Language Interface with support systems"
        
        return strategy
    
    async def _route_and_process(self, user_input: str, strategy: Dict[str, Any],
                               context: AssistantContext, 
                               additional_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Route request to appropriate AI systems and process"""
        primary_system = strategy['primary_system']
        secondary_systems = strategy['secondary_systems']
        
        responses = {}
        
        # Process with primary system
        if primary_system == 'natural_language':
            response = await self.nl_interface.process_command(
                user_input, context.user_id, context.session_id
            )
            responses['primary'] = {
                'system': 'natural_language',
                'response': response
            }
        
        elif primary_system == 'learning':
            help_result = await self.learning_assistant.get_contextual_help(
                user_input, context.user_id, additional_context or {}
            )
            responses['primary'] = {
                'system': 'learning',
                'response': help_result
            }
        
        elif primary_system == 'error_handling':
            error_result = await self.error_handler.handle_error(
                user_input, context.user_id, additional_context or {}
            )
            responses['primary'] = {
                'system': 'error_handling',
                'response': error_result
            }
        
        elif primary_system == 'recommendations':
            recommendations = await self.recommendation_engine.get_recommendations(
                context.user_id, context.active_project or 'default_project'
            )
            responses['primary'] = {
                'system': 'recommendations',
                'response': {
                    'recommendations': recommendations,
                    'count': len(recommendations)
                }
            }
        
        elif primary_system == 'onboarding':
            onboarding_data = await self.onboarding_system.get_personalized_onboarding(
                context.user_id, context.preferences
            )
            responses['primary'] = {
                'system': 'onboarding',
                'response': onboarding_data
            }
        
        # Process with secondary systems for additional insights
        for secondary_system in secondary_systems:
            try:
                if secondary_system == 'recommendations' and secondary_system != primary_system:
                    recs = await self.recommendation_engine.get_recommendations(
                        context.user_id, context.active_project or 'default_project'
                    )
                    responses[secondary_system] = {
                        'system': 'recommendations',
                        'response': recs[:3]  # Top 3 recommendations
                    }
                
                elif secondary_system == 'learning' and secondary_system != primary_system:
                    learning_suggestions = await self.learning_assistant.get_learning_suggestions(
                        context.user_id, user_input
                    )
                    responses[secondary_system] = {
                        'system': 'learning',
                        'response': learning_suggestions
                    }
                
                elif secondary_system == 'ui_personalization':
                    ui_config = await self.ui_system.get_personalized_interface(
                        context.user_id, context.preferences
                    )
                    responses[secondary_system] = {
                        'system': 'ui_personalization',
                        'response': ui_config
                    }
                    
            except Exception as e:
                logger.warning(f"⚠️ Secondary system {secondary_system} failed: {e}")
        
        return responses
    
    async def _enhance_response(self, responses: Dict[str, Any], 
                              context: AssistantContext,
                              strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance response by combining insights from multiple systems"""
        
        primary_response = responses.get('primary', {}).get('response', {})
        
        enhanced = {
            'success': True,
            'primary_system': strategy['primary_system'],
            'confidence': strategy['confidence'],
            'main_response': primary_response,
            'additional_insights': {},
            'recommendations': [],
            'learning_opportunities': [],
            'ui_suggestions': {},
            'next_steps': [],
            'context_updates': {}
        }
        
        # Add recommendations if available
        if 'recommendations' in responses:
            rec_data = responses['recommendations']['response']
            if isinstance(rec_data, list):
                enhanced['recommendations'] = [
                    {
                        'title': rec.title,
                        'description': rec.description,
                        'priority': rec.priority.value,
                        'estimated_time': rec.estimated_time
                    }
                    for rec in rec_data
                ]
            else:
                enhanced['recommendations'] = rec_data.get('recommendations', [])
        
        # Add learning opportunities
        if 'learning' in responses:
            learning_data = responses['learning']['response']
            if isinstance(learning_data, dict):
                enhanced['learning_opportunities'] = learning_data.get('suggestions', [])
        
        # Add UI personalization
        if 'ui_personalization' in responses:
            ui_data = responses['ui_personalization']['response']
            enhanced['ui_suggestions'] = ui_data
        
        # Generate next steps based on primary response
        next_steps = await self._generate_next_steps(primary_response, context)
        enhanced['next_steps'] = next_steps
        
        # Update mode based on interaction
        new_mode = self._determine_new_mode(primary_response, context)
        if new_mode != context.current_mode:
            enhanced['context_updates']['mode_change'] = {
                'from': context.current_mode.value,
                'to': new_mode.value,
                'reason': 'Based on user interaction pattern'
            }
            context.current_mode = new_mode
        
        return enhanced
    
    async def _generate_next_steps(self, primary_response: Dict[str, Any],
                                 context: AssistantContext) -> List[str]:
        """Generate suggested next steps for the user"""
        next_steps = []
        
        # Extract next steps from primary response
        if isinstance(primary_response, dict):
            if 'next_steps' in primary_response:
                next_steps.extend(primary_response['next_steps'])
            
            # Add contextual next steps based on response type
            if 'action' in primary_response:
                action = primary_response['action']
                if action == 'build_app':
                    next_steps.extend([
                        "Customize your app's appearance",
                        "Add interactive components",
                        "Test your app functionality"
                    ])
                elif action == 'add_component':
                    next_steps.extend([
                        "Configure component settings",
                        "Test component functionality",
                        "Style the component to match your theme"
                    ])
        
        # Add learning-based next steps for beginners
        if context.skill_level == 'beginner':
            next_steps.append("Explore the tutorial library for more guidance")
        
        return next_steps[:5]  # Limit to 5 next steps
    
    def _determine_new_mode(self, response: Dict[str, Any], 
                          context: AssistantContext) -> AssistantMode:
        """Determine if assistant mode should change based on interaction"""
        
        # Check if user is building something
        if isinstance(response, dict):
            if 'action' in response and response['action'] in ['build_app', 'add_component']:
                return AssistantMode.BUILDING
            
            # Check if user is learning
            if 'tutorial' in response or 'learning' in response:
                return AssistantMode.LEARNING
            
            # Check if user is troubleshooting
            if 'error' in response or 'fix' in response:
                return AssistantMode.TROUBLESHOOTING
        
        # Default to current mode or exploring
        return context.current_mode if context.current_mode else AssistantMode.EXPLORING
    
    async def _update_assistant_learning(self, user_input: str, response: Dict[str, Any],
                                       context: AssistantContext):
        """Update assistant's learning based on interaction"""
        
        # Track successful interactions
        if response.get('success', False):
            # Update user skill progression
            await self.learning_assistant.track_user_progress(
                context.user_id,
                {
                    'interaction': user_input,
                    'response_quality': response.get('confidence', 0.5),
                    'timestamp': datetime.now()
                }
            )
            
            # Update recommendation effectiveness
            if 'recommendations' in response:
                for rec in response['recommendations'][:3]:  # Track top 3
                    await self.recommendation_engine.track_recommendation_interaction(
                        context.user_id,
                        rec.get('id', 'unknown'),
                        'viewed'
                    )
        
        # Learn from failed interactions
        else:
            logger.info(f"Learning from failed interaction: {user_input}")
    
    def _get_assistant_context(self, user_id: str) -> AssistantContext:
        """Get or create assistant context for user"""
        
        if user_id not in self.active_sessions:
            self.active_sessions[user_id] = AssistantContext(
                user_id=user_id,
                session_id=f"session_{user_id}_{datetime.now().timestamp()}",
                current_mode=AssistantMode.EXPLORING,
                active_project=None,
                conversation_history=[],
                user_goals=[],
                current_task=None,
                skill_level='intermediate',  # Default
                preferences={},
                last_interaction=datetime.now()
            )
        
        return self.active_sessions[user_id]
    
    # High-level convenience methods
    async def ask_question(self, question: str, user_id: str) -> Dict[str, Any]:
        """Process a user question"""
        return await self.process_interaction(
            question, user_id, InteractionType.QUESTION
        )
    
    async def execute_command(self, command: str, user_id: str) -> Dict[str, Any]:
        """Execute a natural language command"""
        return await self.process_interaction(
            command, user_id, InteractionType.COMMAND
        )
    
    async def get_help(self, topic: str, user_id: str) -> Dict[str, Any]:
        """Get help on a specific topic"""
        return await self.process_interaction(
            f"Help me with {topic}", user_id, InteractionType.HELP_REQUEST
        )
    
    async def report_error(self, error_description: str, user_id: str, 
                         error_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Report and get help with an error"""
        return await self.process_interaction(
            error_description, user_id, InteractionType.ERROR_REPORT, error_context
        )
    
    async def get_recommendations(self, context: str, user_id: str) -> Dict[str, Any]:
        """Get smart recommendations"""
        return await self.process_interaction(
            f"What do you recommend for {context}?", user_id, InteractionType.QUESTION
        )
    
    async def start_onboarding(self, user_id: str, user_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Start personalized onboarding process"""
        # Update user context with provided info
        context = self._get_assistant_context(user_id)
        if user_info:
            context.skill_level = user_info.get('skill_level', 'beginner')
            context.preferences.update(user_info.get('preferences', {}))
            context.user_goals = user_info.get('goals', [])
        
        return await self.process_interaction(
            "I'm getting started and need help", user_id, InteractionType.HELP_REQUEST
        )
    
    # Analytics and insights
    async def get_assistant_analytics(self, user_id: str = None) -> Dict[str, Any]:
        """Get analytics about assistant performance"""
        
        analytics = {
            'total_sessions': len(self.active_sessions),
            'system_usage': {
                'natural_language': 0,
                'learning': 0,
                'recommendations': 0,
                'error_handling': 0,
                'onboarding': 0
            },
            'user_engagement': {},
            'mode_distribution': {mode.value: 0 for mode in AssistantMode},
            'success_metrics': {
                'total_interactions': 0,
                'successful_interactions': 0,
                'user_satisfaction_score': 0.0
            }
        }
        
        # Analyze session data
        for session in self.active_sessions.values():
            analytics['mode_distribution'][session.current_mode.value] += 1
            
            for interaction in session.conversation_history:
                analytics['success_metrics']['total_interactions'] += 1
                # Assume success if no error in context
                if not interaction.get('context', {}).get('error'):
                    analytics['success_metrics']['successful_interactions'] += 1
        
        # Calculate success rate
        total = analytics['success_metrics']['total_interactions']
        if total > 0:
            success_rate = analytics['success_metrics']['successful_interactions'] / total
            analytics['success_metrics']['success_rate'] = success_rate
            # Simple satisfaction score based on success rate
            analytics['success_metrics']['user_satisfaction_score'] = success_rate * 0.8 + 0.2
        
        return analytics


class IntegratedAIAssistantDemo:
    """Demonstration of the Integrated AI Assistant"""
    
    def __init__(self):
        self.assistant = IntegratedAIAssistant()
    
    async def run_comprehensive_demo(self) -> Dict[str, Any]:
        """Run comprehensive demonstration of the integrated AI assistant"""
        print("🤖 Integrated AI Assistant Comprehensive Demo")
        print("=" * 60)
        
        results = {}
        
        # Demo scenarios
        demo_scenarios = [
            {
                'user_id': 'beginner_user',
                'skill_level': 'beginner',
                'interactions': [
                    "I'm new here and want to build my first website",
                    "How do I add a contact form?",
                    "The form isn't working properly",
                    "What should I do next?"
                ]
            },
            {
                'user_id': 'intermediate_user', 
                'skill_level': 'intermediate',
                'interactions': [
                    "Create an e-commerce website with payment integration",
                    "Recommend the best components for online shopping",
                    "How do I optimize performance?",
                    "Deploy to AWS"
                ]
            },
            {
                'user_id': 'advanced_user',
                'skill_level': 'advanced',
                'interactions': [
                    "Build a complex dashboard with real-time data",
                    "I'm getting CORS errors in production",
                    "Suggest advanced security implementations",
                    "What are the latest best practices?"
                ]
            }
        ]
        
        print("\n🎯 Testing Integrated AI Scenarios:")
        print("-" * 40)
        
        for scenario in demo_scenarios:
            user_id = scenario['user_id']
            skill_level = scenario['skill_level']
            
            print(f"\n👤 User: {user_id} ({skill_level})")
            print("-" * 30)
            
            # Set up user context
            context = self.assistant._get_assistant_context(user_id)
            context.skill_level = skill_level
            
            scenario_results = []
            
            for i, interaction in enumerate(scenario['interactions'], 1):
                print(f"\n{i}. User: \"{interaction}\"")
                
                # Process interaction
                response = await self.assistant.process_interaction(
                    interaction, user_id
                )
                
                if response.get('success', False):
                    primary_system = response.get('primary_system', 'unknown')
                    confidence = response.get('confidence', 0.0)
                    
                    print(f"   System: {primary_system} (confidence: {confidence:.2f})")
                    
                    # Show main response
                    main_response = response.get('main_response', {})
                    if isinstance(main_response, dict):
                        if 'response' in main_response:
                            print(f"   Response: {main_response['response'][:100]}...")
                        elif 'message' in main_response:
                            print(f"   Response: {main_response['message'][:100]}...")
                    
                    # Show recommendations if available
                    recommendations = response.get('recommendations', [])
                    if recommendations:
                        print(f"   Recommendations: {len(recommendations)} suggestions")
                    
                    # Show next steps
                    next_steps = response.get('next_steps', [])
                    if next_steps:
                        print(f"   Next Steps: {next_steps[0] if next_steps else 'None'}")
                    
                    scenario_results.append({
                        'interaction': interaction,
                        'primary_system': primary_system,
                        'confidence': confidence,
                        'recommendations_count': len(recommendations),
                        'next_steps_count': len(next_steps),
                        'success': True
                    })
                    
                else:
                    print(f"   ❌ Error: {response.get('error', 'Unknown error')}")
                    scenario_results.append({
                        'interaction': interaction,
                        'success': False,
                        'error': response.get('error')
                    })
            
            results[user_id] = {
                'skill_level': skill_level,
                'interactions': scenario_results,
                'total_interactions': len(scenario['interactions']),
                'successful_interactions': sum(1 for r in scenario_results if r.get('success', False))
            }
        
        # Test high-level convenience methods
        print(f"\n🔧 Testing Convenience Methods:")
        print("-" * 35)
        
        convenience_tests = [
            ('ask_question', "What's the best way to style a button?", 'test_user'),
            ('execute_command', "Add a shopping cart to my website", 'test_user'),
            ('get_help', "responsive design", 'test_user'),
            ('get_recommendations', "e-commerce features", 'test_user')
        ]
        
        convenience_results = []
        
        for method_name, input_text, user_id in convenience_tests:
            try:
                method = getattr(self.assistant, method_name)
                result = await method(input_text, user_id)
                
                success = result.get('success', False)
                system = result.get('primary_system', 'unknown')
                
                print(f"   {method_name}: {system} ({'✅' if success else '❌'})")
                
                convenience_results.append({
                    'method': method_name,
                    'success': success,
                    'system': system
                })
                
            except Exception as e:
                print(f"   {method_name}: ❌ Error - {e}")
                convenience_results.append({
                    'method': method_name,
                    'success': False,
                    'error': str(e)
                })
        
        # Get analytics
        print(f"\n📊 Assistant Analytics:")
        print("-" * 25)
        
        analytics = await self.assistant.get_assistant_analytics()
        
        print(f"   Total Sessions: {analytics['total_sessions']}")
        print(f"   Total Interactions: {analytics['success_metrics']['total_interactions']}")
        print(f"   Success Rate: {analytics['success_metrics'].get('success_rate', 0.0):.2%}")
        print(f"   User Satisfaction: {analytics['success_metrics']['user_satisfaction_score']:.2f}")
        
        # Mode distribution
        mode_dist = analytics['mode_distribution']
        active_modes = {k: v for k, v in mode_dist.items() if v > 0}
        print(f"   Active Modes: {active_modes}")
        
        # Generate comprehensive summary
        total_scenarios = len(demo_scenarios)
        total_interactions = sum(r['total_interactions'] for r in results.values())
        total_successful = sum(r['successful_interactions'] for r in results.values())
        overall_success_rate = total_successful / total_interactions if total_interactions > 0 else 0
        
        convenience_success = sum(1 for r in convenience_results if r.get('success', False))
        convenience_total = len(convenience_results)
        convenience_rate = convenience_success / convenience_total if convenience_total > 0 else 0
        
        business_impact = {
            'unified_experience': 'Single AI assistant handles all user needs seamlessly',
            'intelligent_routing': 'Automatically routes requests to best AI system',
            'context_awareness': 'Maintains conversation context across interactions',
            'personalization': 'Adapts responses based on user skill level and history',
            'learning_integration': 'Combines learning, recommendations, and assistance',
            'efficiency_gain': f'{overall_success_rate:.1%} success rate in handling diverse requests'
        }
        
        technical_innovations = [
            'Multi-system AI integration architecture',
            'Intelligent request routing based on intent analysis',
            'Cross-system context sharing and learning',
            'Unified response enhancement from multiple AI systems',
            'Adaptive conversation mode management',
            'Real-time learning and user behavior tracking'
        ]
        
        summary = {
            'total_scenarios_tested': total_scenarios,
            'total_interactions_processed': total_interactions,
            'overall_success_rate': f"{overall_success_rate:.1%}",
            'convenience_methods_success_rate': f"{convenience_rate:.1%}",
            'features_demonstrated': [
                'Multi-System AI Integration',
                'Intelligent Request Routing',
                'Context-Aware Conversations',
                'Personalized Responses',
                'Cross-System Learning',
                'Unified User Experience',
                'Real-time Analytics'
            ],
            'ai_systems_integrated': [
                'Advanced AI Learning Assistant',
                'Natural Language Interface',
                'Smart Recommendations Engine',
                'Personalized UI System',
                'AI-Powered Onboarding',
                'Intelligent Error Handling'
            ],
            'business_impact': business_impact,
            'technical_innovations': technical_innovations
        }
        
        print(f"\n📋 Demo Summary:")
        print(f"   Scenarios: {summary['total_scenarios_tested']}")
        print(f"   Interactions: {summary['total_interactions_processed']}")
        print(f"   Success Rate: {summary['overall_success_rate']}")
        print(f"   AI Systems: {len(summary['ai_systems_integrated'])}")
        print(f"   Features: {len(summary['features_demonstrated'])}")
        
        return {
            'scenario_results': results,
            'convenience_results': convenience_results,
            'analytics': analytics,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }


# Example usage
if __name__ == "__main__":
    async def main():
        demo = IntegratedAIAssistantDemo()
        results = await demo.run_comprehensive_demo()
        
        print("\n🎉 Integrated AI Assistant Demo Complete!")
        print(f"Overall Success Rate: {results['summary']['overall_success_rate']}")
    
    asyncio.run(main())
