"""
Personalized UI System - AI-Powered Dynamic User Interface
Transforms the UI based on user behavior, preferences, and AI recommendations
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
from enum import Enum
import logging

# Optional ML dependencies - graceful fallback if not available
try:
    import numpy as np
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    ml_available = True
except ImportError:
    ml_available = False
    # Create mock classes for when ML libraries aren't available
    class MockScaler:
        def fit_transform(self, data: Any) -> Any: 
            return data
        def transform(self, data: Any) -> Any: 
            return data
    
    class MockKMeans:
        def __init__(self, n_clusters: int = 5, random_state: int = 42): 
            pass
        def fit_predict(self, data: Any) -> List[int]: 
            return [0] * (len(data) if hasattr(data, '__len__') else 1)
    
    StandardScaler = MockScaler
    KMeans = MockKMeans

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UIPersonalizationType(Enum):
    LAYOUT_OPTIMIZATION = "layout_optimization"
    COLOR_SCHEME_ADAPTATION = "color_scheme_adaptation"
    NAVIGATION_PERSONALIZATION = "navigation_personalization"
    CONTENT_PRIORITIZATION = "content_prioritization"
    ACCESSIBILITY_ENHANCEMENT = "accessibility_enhancement"
    WORKFLOW_CUSTOMIZATION = "workflow_customization"

class PersonalizationTrigger(Enum):
    USER_BEHAVIOR = "user_behavior"
    TIME_OF_DAY = "time_of_day"
    DEVICE_TYPE = "device_type"
    USAGE_PATTERN = "usage_pattern"
    PERFORMANCE_METRICS = "performance_metrics"
    AI_RECOMMENDATION = "ai_recommendation"

@dataclass
class UIPersonalizationRule:
    rule_id: str
    trigger: PersonalizationTrigger
    condition: Dict[str, Any]
    personalization_type: UIPersonalizationType
    ui_changes: Dict[str, Any]
    priority: int
    confidence_score: float
    created_at: datetime
    last_applied: Optional[datetime] = None
    effectiveness_score: float = 0.0

@dataclass
class PersonalizedUIComponent:
    component_id: str
    original_config: Dict[str, Any]
    personalized_config: Dict[str, Any]
    personalization_reasons: List[str]
    adaptation_score: float
    last_updated: datetime

class PersonalizedUISystem:
    """Advanced AI-powered UI personalization system"""
    
    def __init__(self):
        self.personalization_rules: Dict[str, UIPersonalizationRule] = {}
        self.user_ui_profiles: Dict[str, Dict[str, Any]] = {}
        self.component_templates: Dict[str, Dict[str, Any]] = {}
        self.adaptation_history: List[Dict[str, Any]] = []
        self.ml_scaler = StandardScaler()
        self.ui_clusterer = KMeans(n_clusters=5, random_state=42)
        self._initialize_default_rules()
        self._initialize_component_templates()
    
    def _initialize_default_rules(self):
        """Initialize default personalization rules"""
        default_rules = [
            UIPersonalizationRule(
                rule_id="mobile_simplified_nav",
                trigger=PersonalizationTrigger.DEVICE_TYPE,
                condition={"device_type": "mobile"},
                personalization_type=UIPersonalizationType.NAVIGATION_PERSONALIZATION,
                ui_changes={
                    "navigation_style": "hamburger_menu",
                    "menu_items": "condensed",
                    "touch_targets": "enlarged"
                },
                priority=8,
                confidence_score=0.9,
                created_at=datetime.now()
            ),
            UIPersonalizationRule(
                rule_id="dark_mode_evening",
                trigger=PersonalizationTrigger.TIME_OF_DAY,
                condition={"time_range": "18:00-06:00"},
                personalization_type=UIPersonalizationType.COLOR_SCHEME_ADAPTATION,
                ui_changes={
                    "theme": "dark",
                    "contrast": "high",
                    "blue_light_reduction": True
                },
                priority=6,
                confidence_score=0.85,
                created_at=datetime.now()
            ),
            UIPersonalizationRule(
                rule_id="beginner_guided_layout",
                trigger=PersonalizationTrigger.USER_BEHAVIOR,
                condition={"experience_level": "beginner", "session_count": "<5"},
                personalization_type=UIPersonalizationType.LAYOUT_OPTIMIZATION,
                ui_changes={
                    "guided_tours": True,
                    "tooltips": "extensive",
                    "simplified_interface": True,
                    "help_prominence": "high"
                },
                priority=9,
                confidence_score=0.95,
                created_at=datetime.now()
            ),
            UIPersonalizationRule(
                rule_id="power_user_advanced",
                trigger=PersonalizationTrigger.USAGE_PATTERN,
                condition={"daily_actions": ">50", "feature_usage": "advanced"},
                personalization_type=UIPersonalizationType.WORKFLOW_CUSTOMIZATION,
                ui_changes={
                    "shortcuts_visible": True,
                    "advanced_features": "prominently_displayed",
                    "bulk_operations": True,
                    "keyboard_navigation": "enhanced"
                },
                priority=7,
                confidence_score=0.88,
                created_at=datetime.now()
            )
        ]
        
        for rule in default_rules:
            self.personalization_rules[rule.rule_id] = rule
    
    def _initialize_component_templates(self):
        """Initialize UI component templates for personalization"""
        self.component_templates = {
            "dashboard": {
                "beginner": {
                    "layout": "guided",
                    "widgets": ["welcome_card", "quick_start", "recent_projects"],
                    "complexity": "low"
                },
                "intermediate": {
                    "layout": "balanced",
                    "widgets": ["overview", "analytics", "shortcuts", "recent_activity"],
                    "complexity": "medium"
                },
                "expert": {
                    "layout": "information_dense",
                    "widgets": ["detailed_metrics", "advanced_controls", "system_status"],
                    "complexity": "high"
                }
            },
            "navigation": {
                "mobile": {
                    "style": "bottom_tabs",
                    "items": "essential_only",
                    "search": "prominent"
                },
                "tablet": {
                    "style": "sidebar_collapsible",
                    "items": "categorized",
                    "search": "header"
                },
                "desktop": {
                    "style": "full_sidebar",
                    "items": "complete",
                    "search": "always_visible"
                }
            },
            "forms": {
                "accessibility_high": {
                    "labels": "verbose",
                    "validation": "immediate",
                    "help_text": "extensive",
                    "error_handling": "detailed"
                },
                "speed_optimized": {
                    "auto_complete": True,
                    "smart_defaults": True,
                    "progressive_disclosure": True,
                    "keyboard_shortcuts": True
                }
            }
        }
    
    def analyze_user_behavior(self, user_id: str, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user behavior patterns for personalization"""
        try:
            # Extract behavior features
            features = {
                "session_duration": behavior_data.get("session_duration", 0),
                "clicks_per_session": behavior_data.get("clicks_per_session", 0),
                "feature_usage_diversity": len(behavior_data.get("features_used", [])),
                "error_rate": behavior_data.get("error_rate", 0),
                "mobile_usage_ratio": behavior_data.get("mobile_sessions", 0) / max(behavior_data.get("total_sessions", 1), 1),
                "time_of_day_preference": self._calculate_time_preference(behavior_data.get("session_times", [])),
                "workflow_efficiency": behavior_data.get("task_completion_rate", 0)
            }
            
            # Calculate user segment
            user_segment = self._determine_user_segment(features)
            
            # Generate personalization insights
            insights = {
                "user_segment": user_segment,
                "behavior_features": features,
                "personalization_opportunities": self._identify_personalization_opportunities(features),
                "ui_preferences": self._infer_ui_preferences(behavior_data),
                "optimization_potential": self._calculate_optimization_potential(features)
            }
            
            # Store user profile
            self.user_ui_profiles[user_id] = {
                "insights": insights,
                "last_analyzed": datetime.now(),
                "personalization_history": self.user_ui_profiles.get(user_id, {}).get("personalization_history", [])
            }
            
            logger.info(f"Analyzed user behavior for {user_id}: segment={user_segment}")
            return insights
            
        except Exception as e:
            logger.error(f"Error analyzing user behavior: {e}")
            return {"error": str(e)}
    
    def generate_personalized_ui(self, user_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate personalized UI configuration"""
        try:
            user_profile = self.user_ui_profiles.get(user_id, {})
            current_time = datetime.now()
            
            # Collect applicable personalization rules
            applicable_rules = self._find_applicable_rules(user_profile, context, current_time)
            
            # Generate base UI configuration
            base_ui = self._get_base_ui_config(context.get("page_type", "dashboard"))
            
            # Apply personalization rules
            personalized_ui = self._apply_personalization_rules(base_ui, applicable_rules)
            
            # Add AI-driven enhancements
            ai_enhancements = self._generate_ai_enhancements(user_profile, context)
            personalized_ui.update(ai_enhancements)
            
            # Track personalization application
            self._track_personalization_application(user_id, applicable_rules, personalized_ui)
            
            logger.info(f"Generated personalized UI for {user_id}: {len(applicable_rules)} rules applied")
            return {
                "ui_config": personalized_ui,
                "applied_rules": [rule.rule_id for rule in applicable_rules],
                "personalization_score": self._calculate_personalization_score(applicable_rules),
                "generated_at": current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating personalized UI: {e}")
            return {"error": str(e)}
    
    def adapt_ui_component(self, component_id: str, user_id: str, component_config: Dict[str, Any]) -> PersonalizedUIComponent:
        """Adapt a specific UI component for a user"""
        try:
            user_profile = self.user_ui_profiles.get(user_id, {})
            
            # Analyze component usage patterns
            usage_patterns = self._analyze_component_usage(component_id, user_id)
            
            # Generate personalized configuration
            personalized_config = component_config.copy()
            adaptation_reasons = []
            
            # Apply user segment adaptations
            if user_profile and "insights" in user_profile:
                segment = user_profile["insights"].get("user_segment", "intermediate")
                
                if component_id in self.component_templates:
                    template = self.component_templates[component_id].get(segment, {})
                    personalized_config.update(template)
                    adaptation_reasons.append(f"Adapted for {segment} user segment")
            
            # Apply accessibility adaptations
            if self._needs_accessibility_adaptation(user_profile):
                accessibility_config = self._generate_accessibility_adaptations(component_config)
                personalized_config.update(accessibility_config)
                adaptation_reasons.append("Applied accessibility enhancements")
            
            # Calculate adaptation score
            adaptation_score = self._calculate_adaptation_score(component_config, personalized_config)
            
            personalized_component = PersonalizedUIComponent(
                component_id=component_id,
                original_config=component_config,
                personalized_config=personalized_config,
                personalization_reasons=adaptation_reasons,
                adaptation_score=adaptation_score,
                last_updated=datetime.now()
            )
            
            logger.info(f"Adapted component {component_id} for user {user_id}: score={adaptation_score}")
            return personalized_component
            
        except Exception as e:
            logger.error(f"Error adapting UI component: {e}")
            return PersonalizedUIComponent(
                component_id=component_id,
                original_config=component_config,
                personalized_config=component_config,
                personalization_reasons=[f"Error: {str(e)}"],
                adaptation_score=0.0,
                last_updated=datetime.now()
            )
    
    def optimize_ui_performance(self, user_id: str, performance_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize UI based on performance metrics"""
        try:
            optimizations = []
            
            # Analyze performance bottlenecks
            if performance_data.get("load_time", 0) > 3000:  # > 3 seconds
                optimizations.append({
                    "type": "lazy_loading",
                    "description": "Enable lazy loading for non-critical components",
                    "expected_improvement": "40-60% faster initial load"
                })
            
            if performance_data.get("interaction_delay", 0) > 100:  # > 100ms
                optimizations.append({
                    "type": "ui_simplification",
                    "description": "Reduce visual complexity and animations",
                    "expected_improvement": "Smoother interactions"
                })
            
            if performance_data.get("memory_usage", 0) > 100:  # > 100MB
                optimizations.append({
                    "type": "component_virtualization",
                    "description": "Virtualize large lists and data displays",
                    "expected_improvement": "50-70% memory reduction"
                })
            
            # Device-specific optimizations
            device_type = performance_data.get("device_type", "desktop")
            if device_type == "mobile":
                optimizations.extend([
                    {
                        "type": "touch_optimization",
                        "description": "Optimize touch targets and gestures",
                        "expected_improvement": "Better mobile usability"
                    },
                    {
                        "type": "battery_optimization",
                        "description": "Reduce CPU-intensive animations",
                        "expected_improvement": "Extended battery life"
                    }
                ])
            
            # Generate optimization configuration
            optimization_config = self._generate_optimization_config(optimizations)
            
            logger.info(f"Generated {len(optimizations)} UI optimizations for user {user_id}")
            return {
                "optimizations": optimizations,
                "config": optimization_config,
                "performance_score": self._calculate_performance_score(performance_data),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing UI performance: {e}")
            return {"error": str(e)}
    
    def _determine_user_segment(self, features: Dict[str, Any]) -> str:
        """Determine user segment based on behavior features"""
        try:
            # Simple rule-based segmentation
            if features["session_duration"] < 300:  # < 5 minutes
                return "casual"
            elif features["clicks_per_session"] > 50 and features["feature_usage_diversity"] > 10:
                return "power_user"
            elif features["error_rate"] > 0.1:
                return "beginner"
            elif features["workflow_efficiency"] > 0.8:
                return "expert"
            else:
                return "intermediate"
                
        except Exception as e:
            logger.error(f"Error determining user segment: {e}")
            return "intermediate"
    
    def _identify_personalization_opportunities(self, features: Dict[str, Any]) -> List[str]:
        """Identify personalization opportunities based on behavior"""
        opportunities = []
        
        if features["mobile_usage_ratio"] > 0.7:
            opportunities.append("mobile_first_optimization")
        
        if features["error_rate"] > 0.15:
            opportunities.append("enhanced_guidance")
        
        if features["workflow_efficiency"] < 0.5:
            opportunities.append("workflow_simplification")
        
        if features["session_duration"] > 1800:  # > 30 minutes
            opportunities.append("advanced_features_exposure")
        
        return opportunities
    
    def _infer_ui_preferences(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """Infer UI preferences from behavior data"""
        preferences = {}
        
        # Color scheme preference
        session_times = behavior_data.get("session_times", [])
        evening_sessions = sum(1 for t in session_times if 18 <= t <= 23 or 0 <= t <= 6)
        if evening_sessions / max(len(session_times), 1) > 0.6:
            preferences["color_scheme"] = "dark"
        else:
            preferences["color_scheme"] = "light"
        
        # Layout density preference
        if behavior_data.get("clicks_per_session", 0) > 30:
            preferences["layout_density"] = "compact"
        else:
            preferences["layout_density"] = "spacious"
        
        # Navigation style preference
        if behavior_data.get("navigation_clicks", 0) > behavior_data.get("content_clicks", 1):
            preferences["navigation_style"] = "prominent"
        else:
            preferences["navigation_style"] = "minimal"
        
        return preferences
    
    def _calculate_time_preference(self, session_times: List[int]) -> str:
        """Calculate preferred time of day for usage"""
        if not session_times:
            return "mixed"
        
        morning = sum(1 for t in session_times if 6 <= t <= 12)
        afternoon = sum(1 for t in session_times if 12 <= t <= 18)
        evening = sum(1 for t in session_times if 18 <= t <= 24 or 0 <= t <= 6)
        
        max_usage = max(morning, afternoon, evening)
        if max_usage == morning:
            return "morning"
        elif max_usage == afternoon:
            return "afternoon"
        else:
            return "evening"
    
    def _calculate_optimization_potential(self, features: Dict[str, Any]) -> float:
        """Calculate the potential for UI optimization"""
        factors = [
            min(features["error_rate"] * 2, 1.0),  # Higher error rate = more potential
            1.0 - features["workflow_efficiency"],  # Lower efficiency = more potential
            min(features["session_duration"] / 3600, 1.0)  # Longer sessions = more potential
        ]
        return sum(factors) / len(factors)
    
    def _find_applicable_rules(self, user_profile: Dict[str, Any], context: Dict[str, Any], current_time: datetime) -> List[UIPersonalizationRule]:
        """Find personalization rules applicable to current context"""
        applicable_rules = []
        
        for rule in self.personalization_rules.values():
            if self._rule_matches_context(rule, user_profile, context, current_time):
                applicable_rules.append(rule)
        
        # Sort by priority and confidence
        applicable_rules.sort(key=lambda r: (r.priority, r.confidence_score), reverse=True)
        return applicable_rules
    
    def _rule_matches_context(self, rule: UIPersonalizationRule, user_profile: Dict[str, Any], context: Dict[str, Any], current_time: datetime) -> bool:
        """Check if a rule matches the current context"""
        try:
            if rule.trigger == PersonalizationTrigger.DEVICE_TYPE:
                return context.get("device_type") == rule.condition.get("device_type")
            
            elif rule.trigger == PersonalizationTrigger.TIME_OF_DAY:
                current_hour = current_time.hour
                time_range = rule.condition.get("time_range", "").split("-")
                if len(time_range) == 2:
                    start_hour = int(time_range[0].split(":")[0])
                    end_hour = int(time_range[1].split(":")[0])
                    if start_hour > end_hour:  # Overnight range
                        return current_hour >= start_hour or current_hour <= end_hour
                    else:
                        return start_hour <= current_hour <= end_hour
            
            elif rule.trigger == PersonalizationTrigger.USER_BEHAVIOR:
                if not user_profile or "insights" not in user_profile:
                    return False
                
                insights = user_profile["insights"]
                for key, value in rule.condition.items():
                    if key == "experience_level":
                        if insights.get("user_segment") != value:
                            return False
                    elif key == "session_count":
                        operator, threshold = value[0], int(value[1:])
                        session_count = insights.get("session_count", 0)
                        if operator == "<" and session_count >= threshold:
                            return False
                        elif operator == ">" and session_count <= threshold:
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error matching rule {rule.rule_id}: {e}")
            return False
    
    def _get_base_ui_config(self, page_type: str) -> Dict[str, Any]:
        """Get base UI configuration for a page type"""
        base_configs = {
            "dashboard": {
                "layout": "grid",
                "theme": "light",
                "navigation": "sidebar",
                "density": "medium"
            },
            "editor": {
                "layout": "focused",
                "theme": "light",
                "navigation": "minimal",
                "density": "compact"
            },
            "settings": {
                "layout": "form",
                "theme": "light",
                "navigation": "breadcrumb",
                "density": "spacious"
            }
        }
        return base_configs.get(page_type, base_configs["dashboard"])
    
    def _apply_personalization_rules(self, base_ui: Dict[str, Any], rules: List[UIPersonalizationRule]) -> Dict[str, Any]:
        """Apply personalization rules to base UI configuration"""
        personalized_ui = base_ui.copy()
        
        for rule in rules:
            for key, value in rule.ui_changes.items():
                personalized_ui[key] = value
        
        return personalized_ui
    
    def _generate_ai_enhancements(self, user_profile: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-driven UI enhancements"""
        enhancements = {}
        
        if user_profile and "insights" in user_profile:
            insights = user_profile["insights"]
            
            # Smart defaults based on usage patterns
            if "ui_preferences" in insights:
                prefs = insights["ui_preferences"]
                enhancements.update({
                    "smart_theme": prefs.get("color_scheme", "light"),
                    "smart_density": prefs.get("layout_density", "medium"),
                    "smart_navigation": prefs.get("navigation_style", "standard")
                })
            
            # Predictive features
            if insights.get("optimization_potential", 0) > 0.7:
                enhancements["predictive_suggestions"] = True
                enhancements["auto_optimization"] = True
        
        return enhancements
    
    def _track_personalization_application(self, user_id: str, rules: List[UIPersonalizationRule], ui_config: Dict[str, Any]):
        """Track the application of personalization rules"""
        application_record = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "rules_applied": [rule.rule_id for rule in rules],
            "ui_config": ui_config,
            "personalization_score": self._calculate_personalization_score(rules)
        }
        
        self.adaptation_history.append(application_record)
        
        # Update rule effectiveness (simplified)
        for rule in rules:
            rule.last_applied = datetime.now()
            rule.effectiveness_score = min(rule.effectiveness_score + 0.1, 1.0)
    
    def _calculate_personalization_score(self, rules: List[UIPersonalizationRule]) -> float:
        """Calculate overall personalization score"""
        if not rules:
            return 0.0
        
        weighted_score = sum(rule.confidence_score * (rule.priority / 10) for rule in rules)
        return min(weighted_score / len(rules), 1.0)
    
    def _analyze_component_usage(self, component_id: str, user_id: str) -> Dict[str, Any]:
        """Analyze usage patterns for a specific component"""
        # Simplified usage analysis
        return {
            "usage_frequency": "high",
            "interaction_patterns": ["click", "hover", "focus"],
            "error_prone_areas": [],
            "efficiency_score": 0.8
        }
    
    def _needs_accessibility_adaptation(self, user_profile: Dict[str, Any]) -> bool:
        """Check if user needs accessibility adaptations"""
        if not user_profile or "insights" not in user_profile:
            return False
        
        insights = user_profile["insights"]
        return (
            insights.get("error_rate", 0) > 0.2 or
            insights.get("session_duration", 0) > 3600 or
            insights.get("accessibility_needs", False)
        )
    
    def _generate_accessibility_adaptations(self, component_config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate accessibility adaptations for a component"""
        return {
            "high_contrast": True,
            "larger_text": True,
            "keyboard_navigation": True,
            "screen_reader_support": True,
            "reduced_motion": True
        }
    
    def _calculate_adaptation_score(self, original: Dict[str, Any], adapted: Dict[str, Any]) -> float:
        """Calculate how much a component was adapted"""
        changes = sum(1 for key in adapted if adapted.get(key) != original.get(key))
        total_properties = len(set(original.keys()) | set(adapted.keys()))
        return changes / max(total_properties, 1)
    
    def _generate_optimization_config(self, optimizations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate configuration for performance optimizations"""
        config = {}
        
        for optimization in optimizations:
            opt_type = optimization["type"]
            if opt_type == "lazy_loading":
                config["lazy_loading"] = {
                    "enabled": True,
                    "threshold": 0.5,
                    "components": ["images", "charts", "tables"]
                }
            elif opt_type == "ui_simplification":
                config["ui_simplification"] = {
                    "animations": "reduced",
                    "shadows": "minimal",
                    "transitions": "fast"
                }
            elif opt_type == "component_virtualization":
                config["virtualization"] = {
                    "enabled": True,
                    "buffer_size": 10,
                    "item_height": "auto"
                }
        
        return config
    
    def _calculate_performance_score(self, performance_data: Dict[str, Any]) -> float:
        """Calculate UI performance score"""
        factors = {
            "load_time": min(5000 / max(performance_data.get("load_time", 1000), 1000), 1.0),
            "interaction_delay": min(200 / max(performance_data.get("interaction_delay", 50), 50), 1.0),
            "memory_usage": min(200 / max(performance_data.get("memory_usage", 50), 50), 1.0)
        }
        return sum(factors.values()) / len(factors)

# Demo and testing classes
class PersonalizedUISystemDemo:
    """Demonstration of the Personalized UI System"""
    
    def __init__(self):
        self.ui_system = PersonalizedUISystem()
    
    def run_comprehensive_demo(self) -> Dict[str, Any]:
        """Run a comprehensive demonstration"""
        results = {}
        
        # Demo 1: User behavior analysis
        behavior_data = {
            "session_duration": 1800,
            "clicks_per_session": 45,
            "features_used": ["dashboard", "editor", "settings", "analytics"],
            "error_rate": 0.08,
            "mobile_sessions": 15,
            "total_sessions": 50,
            "session_times": [9, 14, 20, 22, 8, 15, 19],
            "task_completion_rate": 0.85,
            "navigation_clicks": 120,
            "content_clicks": 200
        }
        
        results["behavior_analysis"] = self.ui_system.analyze_user_behavior("demo_user", behavior_data)
        
        # Demo 2: Personalized UI generation
        context = {
            "page_type": "dashboard",
            "device_type": "desktop",
            "time_of_day": "evening"
        }
        
        results["personalized_ui"] = self.ui_system.generate_personalized_ui("demo_user", context)
        
        # Demo 3: Component adaptation
        component_config = {
            "type": "navigation",
            "style": "horizontal",
            "items": ["home", "projects", "settings"],
            "theme": "light"
        }
        
        results["component_adaptation"] = self.ui_system.adapt_ui_component(
            "main_nav", "demo_user", component_config
        ).__dict__
        
        # Demo 4: Performance optimization
        performance_data = {
            "load_time": 4000,
            "interaction_delay": 150,
            "memory_usage": 120,
            "device_type": "mobile"
        }
        
        results["performance_optimization"] = self.ui_system.optimize_ui_performance("demo_user", performance_data)
        
        return results

def main():
    """Main function for testing"""
    demo = PersonalizedUISystemDemo()
    results = demo.run_comprehensive_demo()
    
    print("🎨 Personalized UI System Demo Results:")
    print("=" * 50)
    
    for section, data in results.items():
        print(f"\n📊 {section.replace('_', ' ').title()}:")
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (dict, list)) and len(str(value)) > 100:
                    print(f"  {key}: [Complex data structure]")
                else:
                    print(f"  {key}: {value}")
        else:
            print(f"  {data}")

if __name__ == "__main__":
    main()
