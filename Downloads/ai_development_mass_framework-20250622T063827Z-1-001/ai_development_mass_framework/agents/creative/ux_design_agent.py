"""
UX Design Agent - Specialized agent for user experience design
"""

from core.agent_base import AgentBase, AgentMessage, MessageType
from typing import Dict, Any, List
from data_sources.live_data_orchestrator import LiveDataOrchestrator
import json

class UXDesignAgent(AgentBase):
    """
    ROLE: Create optimal user experience designs and interfaces
    RESPONSIBILITIES:
    - Design user journeys and interaction flows
    - Create wireframes and interface specifications
    - Ensure accessibility and usability standards
    - Optimize for mobile and responsive design
    - Provide UX research and user testing guidance
    """
    
    def __init__(self):
        super().__init__("ux_designer", "user_experience_design")
        self.design_principles = [
            "user_centered_design", "accessibility_first", "mobile_responsive",
            "performance_optimized", "inclusive_design", "data_driven"
        ]
        self.ux_patterns = {
            "navigation": ["breadcrumb", "sidebar", "tab", "hamburger"],
            "forms": ["progressive", "inline_validation", "autocomplete"],
            "feedback": ["toast", "modal", "inline", "progress_indicator"],
            "layouts": ["grid", "flexbox", "card", "masonry"]
        }
        self.accessibility_standards = ["WCAG_2.1_AA", "Section_508", "ADA"]
        self.live_data = LiveDataOrchestrator()
    
    async def process_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        REQUIRED OUTPUTS:
        - user_journey_map: Complete user flow and interaction design
        - wireframes: Detailed interface wireframes and layouts
        - design_system: Colors, typography, components specification
        - accessibility_compliance: Accessibility features and compliance
        - mobile_optimization: Mobile-first responsive design
        - usability_testing_plan: Testing scenarios and success metrics
        """
        
        app_type = task_data.get("app_type", "web_application")
        target_users = task_data.get("target_users", ["general_users"])
        features = task_data.get("features", [])
        
        # Get UX trends from market data
        ux_trends = await self.live_data.get_market_intelligence(
            domain="ux_design", 
            keywords=["user experience", "interface design", app_type]
        )
        
        # Design user journey
        user_journey = await self._design_user_journey(app_type, target_users, features)
        
        # Create wireframes
        wireframes = await self._create_wireframes(app_type, features, ux_trends)
        
        # Design system
        design_system = await self._create_design_system(app_type, target_users)
        
        # Accessibility features
        accessibility = await self._ensure_accessibility(features)
        
        # Mobile optimization
        mobile_design = await self._optimize_for_mobile(wireframes, features)
        
        # Usability testing plan
        testing_plan = await self._create_testing_plan(user_journey, target_users)
        
        return {
            "user_journey_map": user_journey,
            "wireframes": wireframes,
            "design_system": design_system,
            "accessibility_compliance": accessibility,
            "mobile_optimization": mobile_design,
            "usability_testing_plan": testing_plan,
            "ux_score": self._calculate_ux_score(user_journey, accessibility, mobile_design),
            "implementation_guidelines": await self._create_implementation_guidelines(),
            "design_trends": ux_trends.get("trends", []),
            "estimated_development_time": self._estimate_design_implementation_time(wireframes)
        }
    
    async def _design_user_journey(self, app_type: str, target_users: List[str], features: List[str]) -> Dict[str, Any]:
        """Design complete user journey and flow"""
        
        # Common user journey patterns by app type
        journey_templates = {
            "productivity": ["onboarding", "setup", "daily_use", "collaboration", "reporting"],
            "ecommerce": ["discovery", "product_view", "cart", "checkout", "order_tracking"],
            "social": ["registration", "profile_setup", "content_creation", "interaction", "engagement"],
            "education": ["enrollment", "learning_path", "content_consumption", "assessment", "progress"]
        }
        
        base_journey = journey_templates.get(app_type, ["landing", "registration", "main_use", "settings"])
        
        user_journey = {
            "phases": [],
            "touchpoints": [],
            "pain_points": [],
            "opportunities": []
        }
        
        for phase in base_journey:
            phase_details = {
                "phase_name": phase,
                "user_goals": self._get_phase_goals(phase, app_type),
                "user_actions": self._get_phase_actions(phase, features),
                "emotions": self._predict_user_emotions(phase),
                "interface_requirements": self._get_interface_requirements(phase),
                "success_metrics": self._define_success_metrics(phase)
            }
            user_journey["phases"].append(phase_details)
        
        # Identify potential pain points
        user_journey["pain_points"] = [
            "Complex onboarding process",
            "Unclear navigation",
            "Information overload",
            "Mobile usability issues",
            "Slow loading times"
        ]
        
        # Design opportunities
        user_journey["opportunities"] = [
            "Guided tutorials",
            "Progressive disclosure",
            "Personalized experience",
            "Micro-interactions",
            "Smart defaults"
        ]
        
        return user_journey
    
    async def _create_wireframes(self, app_type: str, features: List[str], ux_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed wireframes for all screens"""
        
        wireframes = {
            "screen_flow": [],
            "components": [],
            "layouts": {},
            "responsive_breakpoints": ["mobile", "tablet", "desktop"]
        }
        
        # Common screens by app type
        screen_templates = {
            "productivity": ["dashboard", "task_list", "task_detail", "calendar", "reports", "settings"],
            "ecommerce": ["home", "product_list", "product_detail", "cart", "checkout", "account"],
            "social": ["feed", "profile", "create_post", "messages", "notifications", "settings"],
            "education": ["course_list", "lesson_view", "quiz", "progress", "certificates", "profile"]
        }
        
        screens = screen_templates.get(app_type, ["home", "main", "profile", "settings"])
        
        for screen in screens:
            wireframe = {
                "screen_name": screen,
                "layout_type": self._determine_layout_type(screen, features),
                "components": self._define_screen_components(screen, features),
                "navigation": self._design_navigation(screen),
                "content_hierarchy": self._define_content_hierarchy(screen),
                "interactions": self._define_interactions(screen),
                "responsive_behavior": self._define_responsive_behavior(screen)
            }
            wireframes["screen_flow"].append(wireframe)
        
        # Define reusable components
        wireframes["components"] = [
            {
                "name": "navigation_bar",
                "type": "header",
                "properties": ["logo", "menu", "user_menu", "search"]
            },
            {
                "name": "card_component",
                "type": "content",
                "properties": ["title", "description", "actions", "metadata"]
            },
            {
                "name": "form_input",
                "type": "form",
                "properties": ["label", "validation", "help_text", "error_state"]
            },
            {
                "name": "button_set",
                "type": "action",
                "properties": ["primary", "secondary", "destructive", "disabled"]
            }
        ]
        
        return wireframes
    
    async def _create_design_system(self, app_type: str, target_users: List[str]) -> Dict[str, Any]:
        """Create comprehensive design system"""
        
        # Choose color palette based on app type
        color_palettes = {
            "productivity": {
                "primary": "#2563eb",    # Blue
                "secondary": "#7c3aed",  # Purple
                "accent": "#059669",     # Green
                "neutral": "#6b7280",    # Gray
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            },
            "ecommerce": {
                "primary": "#dc2626",    # Red
                "secondary": "#ea580c",  # Orange
                "accent": "#7c2d12",     # Brown
                "neutral": "#6b7280",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            },
            "social": {
                "primary": "#3b82f6",    # Blue
                "secondary": "#8b5cf6",  # Purple
                "accent": "#ec4899",     # Pink
                "neutral": "#6b7280",
                "success": "#10b981",
                "warning": "#f59e0b",
                "error": "#ef4444"
            }
        }
        
        colors = color_palettes.get(app_type, color_palettes["productivity"])
        
        design_system = {
            "colors": colors,
            "typography": {
                "font_family_primary": "Inter, system-ui, sans-serif",
                "font_family_mono": "JetBrains Mono, monospace",
                "font_sizes": {
                    "xs": "0.75rem",
                    "sm": "0.875rem", 
                    "base": "1rem",
                    "lg": "1.125rem",
                    "xl": "1.25rem",
                    "2xl": "1.5rem",
                    "3xl": "1.875rem",
                    "4xl": "2.25rem"
                },
                "font_weights": {
                    "light": 300,
                    "normal": 400,
                    "medium": 500,
                    "semibold": 600,
                    "bold": 700
                },
                "line_heights": {
                    "tight": 1.25,
                    "normal": 1.5,
                    "relaxed": 1.75
                }
            },
            "spacing": {
                "xs": "0.25rem",
                "sm": "0.5rem",
                "md": "1rem", 
                "lg": "1.5rem",
                "xl": "2rem",
                "2xl": "3rem",
                "3xl": "4rem"
            },
            "borders": {
                "radius": {
                    "none": "0",
                    "sm": "0.25rem",
                    "md": "0.375rem",
                    "lg": "0.5rem",
                    "xl": "0.75rem",
                    "full": "9999px"
                },
                "width": {
                    "thin": "1px",
                    "medium": "2px",
                    "thick": "4px"
                }
            },
            "shadows": {
                "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
                "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1)",
                "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1)",
                "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1)"
            },
            "breakpoints": {
                "sm": "640px",
                "md": "768px", 
                "lg": "1024px",
                "xl": "1280px",
                "2xl": "1536px"
            }
        }
        
        return design_system
    
    async def _ensure_accessibility(self, features: List[str]) -> Dict[str, Any]:
        """Ensure accessibility compliance and features"""
        
        accessibility = {
            "compliance_level": "WCAG_2.1_AA",
            "features": [
                "keyboard_navigation",
                "screen_reader_support", 
                "high_contrast_mode",
                "focus_indicators",
                "alt_text_images",
                "semantic_html",
                "aria_labels",
                "color_contrast_4_5_1"
            ],
            "testing_requirements": [
                "automated_accessibility_scan",
                "screen_reader_testing",
                "keyboard_only_navigation",
                "color_blindness_simulation",
                "mobile_accessibility_testing"
            ],
            "implementation_guidelines": {
                "color_contrast": "Ensure 4.5:1 ratio for normal text, 3:1 for large text",
                "keyboard_navigation": "All interactive elements must be keyboard accessible",
                "focus_management": "Logical focus order and visible focus indicators",
                "screen_readers": "Proper heading structure and ARIA landmarks",
                "error_handling": "Clear error messages and form validation"
            }
        }
        
        return accessibility
    
    async def _optimize_for_mobile(self, wireframes: Dict[str, Any], features: List[str]) -> Dict[str, Any]:
        """Create mobile-first responsive design optimization"""
        
        mobile_optimization = {
            "design_approach": "mobile_first",
            "touch_targets": {
                "minimum_size": "44px",
                "spacing": "8px_minimum"
            },
            "responsive_patterns": [
                "progressive_enhancement",
                "adaptive_images", 
                "flexible_grids",
                "scalable_typography",
                "touch_gestures"
            ],
            "performance_optimization": [
                "lazy_loading",
                "image_compression",
                "critical_css",
                "minimal_javascript",
                "service_worker_caching"
            ],
            "mobile_specific_features": [
                "swipe_gestures",
                "pull_to_refresh",
                "infinite_scroll",
                "bottom_navigation",
                "thumb_friendly_controls"
            ],
            "testing_devices": [
                "iPhone_14", "Samsung_Galaxy_S23", "iPad_Air", 
                "Pixel_7", "iPhone_SE", "tablet_landscape"
            ]
        }
        
        return mobile_optimization
    
    async def _create_testing_plan(self, user_journey: Dict[str, Any], target_users: List[str]) -> Dict[str, Any]:
        """Create comprehensive usability testing plan"""
        
        testing_plan = {
            "testing_methods": [
                "user_interviews",
                "usability_testing",
                "a_b_testing",
                "heuristic_evaluation",
                "accessibility_audit"
            ],
            "test_scenarios": [],
            "success_metrics": {
                "task_completion_rate": ">90%",
                "time_on_task": "<2_minutes_per_task",
                "error_rate": "<5%",
                "satisfaction_score": ">4.5/5",
                "first_click_success": ">80%"
            },
            "user_personas": self._create_user_personas(target_users),
            "testing_schedule": {
                "prototype_testing": "Week 2",
                "alpha_testing": "Week 4", 
                "beta_testing": "Week 6",
                "post_launch_monitoring": "Ongoing"
            }
        }
        
        # Create test scenarios for each journey phase
        for phase in user_journey.get("phases", []):
            scenario = {
                "phase": phase["phase_name"],
                "task": f"Complete {phase['phase_name']} successfully",
                "expected_behavior": phase.get("user_actions", []),
                "success_criteria": phase.get("success_metrics", [])
            }
            testing_plan["test_scenarios"].append(scenario)
        
        return testing_plan
    
    def _calculate_ux_score(self, user_journey: Dict[str, Any], accessibility: Dict[str, Any], mobile_design: Dict[str, Any]) -> int:
        """Calculate overall UX quality score"""
        score = 0
        
        # Journey complexity (simpler is better)
        journey_phases = len(user_journey.get("phases", []))
        if journey_phases <= 5:
            score += 25
        elif journey_phases <= 8:
            score += 20
        else:
            score += 15
        
        # Accessibility compliance
        if accessibility.get("compliance_level") == "WCAG_2.1_AA":
            score += 25
        
        # Mobile optimization
        if mobile_design.get("design_approach") == "mobile_first":
            score += 25
        
        # Feature completeness
        score += 25  # Base score for feature implementation
        
        return min(score, 100)
    
    async def _create_implementation_guidelines(self) -> Dict[str, Any]:
        """Create guidelines for developers implementing the design"""
        
        return {
            "component_library": "Use design system components consistently",
            "responsive_implementation": "Mobile-first CSS with progressive enhancement", 
            "accessibility_implementation": "Semantic HTML with proper ARIA attributes",
            "performance_guidelines": "Optimize images, minimize CSS/JS, use lazy loading",
            "testing_requirements": "Cross-browser testing on all target devices",
            "documentation": "Maintain component documentation and style guide"
        }
    
    # Helper methods
    def _get_phase_goals(self, phase: str, app_type: str) -> List[str]:
        goals = {
            "onboarding": ["understand_app_purpose", "complete_setup", "feel_confident"],
            "setup": ["configure_preferences", "import_data", "customize_interface"],
            "daily_use": ["complete_primary_tasks", "navigate_efficiently", "feel_productive"],
            "collaboration": ["share_content", "communicate_effectively", "track_progress"]
        }
        return goals.get(phase, ["complete_task", "achieve_goal"])
    
    def _get_phase_actions(self, phase: str, features: List[str]) -> List[str]:
        actions = {
            "onboarding": ["view_welcome", "create_account", "verify_email", "tutorial"],
            "setup": ["upload_profile", "set_preferences", "connect_integrations"],
            "daily_use": ["view_dashboard", "create_content", "manage_tasks", "check_notifications"]
        }
        return actions.get(phase, ["interact", "navigate", "complete"])
    
    def _predict_user_emotions(self, phase: str) -> List[str]:
        emotions = {
            "onboarding": ["curious", "slightly_anxious", "hopeful"],
            "setup": ["focused", "determined", "careful"],
            "daily_use": ["confident", "efficient", "satisfied"],
            "collaboration": ["engaged", "social", "productive"]
        }
        return emotions.get(phase, ["neutral", "focused"])
    
    def _get_interface_requirements(self, phase: str) -> List[str]:
        requirements = {
            "onboarding": ["clear_navigation", "progress_indicator", "help_content"],
            "setup": ["form_validation", "clear_labels", "save_progress"],
            "daily_use": ["quick_access", "efficient_layout", "visual_feedback"]
        }
        return requirements.get(phase, ["clear_interface", "intuitive_controls"])
    
    def _define_success_metrics(self, phase: str) -> List[str]:
        metrics = {
            "onboarding": ["completion_rate_>80%", "time_<5_minutes", "satisfaction_>4/5"],
            "setup": ["configuration_completion", "error_rate_<5%", "time_<10_minutes"],
            "daily_use": ["task_completion_>90%", "efficiency_improvement", "retention_>70%"]
        }
        return metrics.get(phase, ["completion_rate", "user_satisfaction"])
    
    def _determine_layout_type(self, screen: str, features: List[str]) -> str:
        layout_types = {
            "dashboard": "grid_layout",
            "list": "vertical_list",
            "detail": "content_focused",
            "settings": "form_layout",
            "profile": "card_layout"
        }
        return layout_types.get(screen, "flexible_layout")
    
    def _define_screen_components(self, screen: str, features: List[str]) -> List[str]:
        components = {
            "dashboard": ["header", "navigation", "stats_cards", "main_content", "sidebar"],
            "list": ["header", "filters", "search", "list_items", "pagination"],
            "detail": ["header", "breadcrumbs", "main_content", "sidebar", "actions"],
            "settings": ["header", "navigation_tabs", "form_sections", "save_controls"]
        }
        return components.get(screen, ["header", "main_content", "footer"])
    
    def _design_navigation(self, screen: str) -> Dict[str, Any]:
        return {
            "type": "breadcrumb" if screen == "detail" else "main_menu",
            "position": "top",
            "style": "horizontal",
            "responsive": "collapse_to_hamburger"
        }
    
    def _define_content_hierarchy(self, screen: str) -> List[str]:
        hierarchy = {
            "dashboard": ["page_title", "key_metrics", "recent_activity", "quick_actions"],
            "list": ["page_title", "filters", "sort_options", "items", "pagination"],
            "detail": ["breadcrumbs", "item_title", "main_content", "metadata", "actions"]
        }
        return hierarchy.get(screen, ["title", "content", "actions"])
    
    def _define_interactions(self, screen: str) -> List[str]:
        interactions = {
            "dashboard": ["click_cards", "hover_tooltips", "drag_widgets"],
            "list": ["click_items", "filter_sort", "bulk_actions"],
            "detail": ["edit_inline", "share_options", "related_actions"]
        }
        return interactions.get(screen, ["click", "hover", "scroll"])
    
    def _define_responsive_behavior(self, screen: str) -> Dict[str, str]:
        return {
            "mobile": "single_column_stack",
            "tablet": "two_column_layout", 
            "desktop": "full_layout_with_sidebar"
        }
    
    def _create_user_personas(self, target_users: List[str]) -> List[Dict[str, Any]]:
        personas = []
        for user_type in target_users:
            persona = {
                "name": f"{user_type.title()} User",
                "goals": [f"efficiently_use_{user_type}_features"],
                "pain_points": ["complex_interfaces", "slow_performance"],
                "tech_comfort": "medium_to_high",
                "device_preference": ["mobile", "desktop"]
            }
            personas.append(persona)
        return personas
    
    def _estimate_design_implementation_time(self, wireframes: Dict[str, Any]) -> str:
        screen_count = len(wireframes.get("screen_flow", []))
        component_count = len(wireframes.get("components", []))
        
        if screen_count <= 5 and component_count <= 10:
            return "1-2 weeks"
        elif screen_count <= 10 and component_count <= 20:
            return "2-4 weeks"
        else:
            return "4-8 weeks"
    
    async def analyze_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze input for UX design requirements"""
        return {
            "ux_complexity": "medium",
            "design_challenges": ["responsive_design", "accessibility", "performance"],
            "recommended_patterns": ["mobile_first", "progressive_disclosure", "clear_navigation"]
        }
    
    async def coordinate_with_agents(self, other_agents: List[str], task_context: Dict[str, Any]) -> Dict[str, Any]:
        """Coordinate with other agents for optimal UX design"""
        coordination_result = {
            "design_constraints": [],
            "technical_requirements": [],
            "performance_considerations": []
        }
        
        if "system_architect" in other_agents:
            coordination_result["technical_requirements"].append(
                "Ensure design is feasible with chosen technology stack"
            )
        
        if "creative_director" in other_agents:
            coordination_result["design_constraints"].append(
                "Align with brand guidelines and creative vision"
            )
        
        return coordination_result
