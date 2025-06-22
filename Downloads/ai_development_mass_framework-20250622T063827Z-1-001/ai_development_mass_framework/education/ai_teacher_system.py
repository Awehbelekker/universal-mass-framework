"""
AI Teacher/Educational Mode for MASS Framework
Provides step-by-step, toggleable user guidance and educational content
"""

import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, asdict
import random

class LearningLevel(Enum):
    """Learning levels for different user experience"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class GuideStyle(Enum):
    """Different guidance styles"""
    STEP_BY_STEP = "step_by_step"
    INTERACTIVE = "interactive"
    HINTS_ONLY = "hints_only"
    PASSIVE = "passive"
    DISABLED = "disabled"

class LessonCategory(Enum):
    """Categories of lessons/tutorials"""
    GETTING_STARTED = "getting_started"
    VISUAL_BUILDER = "visual_builder"
    API_INTEGRATION = "api_integration"
    DEPLOYMENT = "deployment"
    DATABASE_DESIGN = "database_design"
    AUTHENTICATION = "authentication"
    CLOUD_STORAGE = "cloud_storage"
    PERFORMANCE = "performance"
    SECURITY = "security"
    BEST_PRACTICES = "best_practices"

class InteractionType(Enum):
    """Types of interactions in lessons"""
    EXPLANATION = "explanation"
    DEMONSTRATION = "demonstration"
    HANDS_ON = "hands_on"
    QUIZ = "quiz"
    CHALLENGE = "challenge"
    REVIEW = "review"

@dataclass
class LearningStep:
    """Individual learning step"""
    id: str
    title: str
    description: str
    interaction_type: InteractionType
    content: str
    code_example: Optional[str] = None
    visual_aid: Optional[str] = None
    prerequisites: List[str] = None
    estimated_time: int = 5  # minutes
    difficulty: int = 1  # 1-5 scale
    completion_criteria: Dict[str, Any] = None

@dataclass
class Lesson:
    """Complete lesson with multiple steps"""
    id: str
    title: str
    description: str
    category: LessonCategory
    level: LearningLevel
    steps: List[LearningStep]
    learning_objectives: List[str]
    prerequisites: List[str]
    estimated_duration: int  # minutes
    tags: List[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class UserProgress:
    """User's learning progress"""
    user_id: str
    level: LearningLevel
    completed_lessons: List[str]
    current_lesson: Optional[str]
    current_step: Optional[str]
    preferences: Dict[str, Any]
    learning_streak: int
    total_time_spent: int  # minutes
    achievements: List[str]
    last_activity: datetime

@dataclass
class GuidanceContext:
    """Context for providing guidance"""
    current_action: str
    user_location: str  # e.g., "visual_builder", "deployment_wizard"
    difficulty_detected: bool
    error_count: int
    time_spent: int
    previous_actions: List[str]

class AITeacher:
    """AI-powered teaching and guidance system"""
    
    def __init__(self):
        self.lessons = self._initialize_lessons()
        self.guidance_rules = self._initialize_guidance_rules()
        self.user_sessions = {}
        self.active_guidance = {}
        
    def _initialize_lessons(self) -> Dict[str, Lesson]:
        """Initialize the lesson library"""
        lessons = {}
        
        # Getting Started Lessons
        getting_started_lessons = [
            Lesson(
                id="intro_to_mass",
                title="Introduction to MASS Framework",
                description="Learn the basics of the MASS Framework and its capabilities",
                category=LessonCategory.GETTING_STARTED,
                level=LearningLevel.BEGINNER,
                steps=[
                    LearningStep(
                        id="welcome",
                        title="Welcome to MASS Framework",
                        description="Understanding what MASS Framework can do for you",
                        interaction_type=InteractionType.EXPLANATION,
                        content="""
Welcome to the MASS Framework! 🚀

MASS (Multi-Agent AI System for Software development) is a powerful no-code platform that lets you build professional applications without writing code.

Key capabilities:
• 🎨 Visual drag-and-drop builder
• 🔐 Built-in authentication & user management  
• ☁️ Cloud storage integration
• 🚀 One-click deployment
• 🔌 Hardware/API integrations
• 📱 Mobile-responsive designs

Let's start your journey to becoming a no-code expert!
""",
                        estimated_time=3,
                        difficulty=1
                    ),
                    LearningStep(
                        id="interface_tour",
                        title="Interface Tour",
                        description="Get familiar with the MASS Framework interface",
                        interaction_type=InteractionType.DEMONSTRATION,
                        content="""
Let's explore the main interface:

1. **Navigation Bar**: Access different tools and features
2. **Visual Builder**: Drag-and-drop components to build your app
3. **Component Library**: Pre-built components ready to use
4. **Properties Panel**: Customize selected components
5. **Preview Mode**: See how your app looks to users
6. **Deployment Panel**: Publish your app to the web

Click on each area as I highlight it!
""",
                        estimated_time=5,
                        difficulty=1,
                        completion_criteria={"areas_clicked": 6}
                    ),
                    LearningStep(
                        id="first_component",
                        title="Adding Your First Component",
                        description="Learn to add and customize a component",
                        interaction_type=InteractionType.HANDS_ON,
                        content="""
Now let's add your first component:

1. Look for the **Button** component in the library
2. Drag it onto the canvas
3. Click the button to select it
4. In the properties panel, change the text to "Hello World!"
5. Change the color to blue

This is the foundation of building in MASS Framework - drag, drop, customize!
""",
                        code_example="""
// This is what the system generates behind the scenes:
<button 
    className="btn btn-primary"
    onClick={handleClick}
    style={{backgroundColor: 'blue'}}
>
    Hello World!
</button>
""",
                        estimated_time=7,
                        difficulty=2,
                        completion_criteria={"component_added": True, "text_changed": True, "color_changed": True}
                    )
                ],
                learning_objectives=[
                    "Understand MASS Framework capabilities",
                    "Navigate the interface confidently",
                    "Add and customize basic components"
                ],
                prerequisites=[],
                estimated_duration=15,
                tags=["beginner", "introduction", "basics"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            Lesson(
                id="building_first_app",
                title="Building Your First App",
                description="Create a complete app from start to finish",
                category=LessonCategory.GETTING_STARTED,
                level=LearningLevel.BEGINNER,
                steps=[
                    LearningStep(
                        id="app_planning",
                        title="Planning Your App",
                        description="Learn to plan before building",
                        interaction_type=InteractionType.EXPLANATION,
                        content="""
Before we start building, let's plan our app! 📋

We'll create a "Personal Task Manager":
• ✅ Task list with add/remove functionality
• 🎨 Beautiful, modern design
• 📱 Mobile-friendly layout
• 💾 Data persistence

Good planning leads to better apps. Always think about:
1. What problem does this solve?
2. Who will use it?
3. What features are essential?
4. How should it look and feel?
""",
                        estimated_time=3,
                        difficulty=1
                    ),
                    LearningStep(
                        id="layout_creation",
                        title="Creating the Layout",
                        description="Build the basic structure",
                        interaction_type=InteractionType.HANDS_ON,
                        content="""
Let's create the basic layout:

1. Add a **Header** component and set title to "My Tasks"
2. Add a **Container** component for the main content
3. Inside the container, add an **Input** field for new tasks
4. Add a **Button** next to the input labeled "Add Task"
5. Add a **List** component below for displaying tasks

Your layout should look like a typical task management app!
""",
                        estimated_time=10,
                        difficulty=2,
                        completion_criteria={"header_added": True, "input_added": True, "button_added": True, "list_added": True}
                    ),
                    LearningStep(
                        id="styling_basics",
                        title="Making It Look Good",
                        description="Apply styling and themes",
                        interaction_type=InteractionType.HANDS_ON,
                        content="""
Now let's make it beautiful! 🎨

1. Select the header and choose a modern color scheme
2. Add spacing around components using the margin/padding controls
3. Make the input field and button the same height
4. Choose a clean font from the typography options
5. Add a subtle shadow to the main container

Remember: Good design makes users want to use your app!
""",
                        estimated_time=8,
                        difficulty=2
                    ),
                    LearningStep(
                        id="adding_functionality",
                        title="Adding Functionality",
                        description="Make the app interactive",
                        interaction_type=InteractionType.HANDS_ON,
                        content="""
Time to make it work! ⚡

1. Select the "Add Task" button
2. In the Actions panel, add an "Add Item to List" action
3. Connect it to your input field and task list
4. Add a "Clear Input" action to empty the field after adding
5. Test it out - add a few tasks!

No coding required - MASS Framework handles all the complexity!
""",
                        code_example="""
// Behind the scenes, MASS Framework generates:
const addTask = () => {
    const taskText = inputRef.current.value;
    if (taskText.trim()) {
        setTasks([...tasks, {
            id: Date.now(),
            text: taskText,
            completed: false
        }]);
        inputRef.current.value = '';
    }
};
""",
                        estimated_time=12,
                        difficulty=3,
                        completion_criteria={"action_added": True, "task_added": True}
                    )
                ],
                learning_objectives=[
                    "Plan an app before building",
                    "Create structured layouts",
                    "Apply professional styling",
                    "Add interactive functionality"
                ],
                prerequisites=["intro_to_mass"],
                estimated_duration=35,
                tags=["beginner", "hands-on", "complete-app"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Visual Builder Lessons
        visual_builder_lessons = [
            Lesson(
                id="advanced_components",
                title="Mastering Advanced Components",
                description="Learn to use complex components effectively",
                category=LessonCategory.VISUAL_BUILDER,
                level=LearningLevel.INTERMEDIATE,
                steps=[
                    LearningStep(
                        id="data_components",
                        title="Working with Data Components",
                        description="Tables, charts, and data visualization",
                        interaction_type=InteractionType.DEMONSTRATION,
                        content="""
Data components help you display information beautifully:

📊 **Chart Component**:
- Bar charts, line charts, pie charts
- Automatic data binding
- Interactive legends and tooltips

📋 **Table Component**:
- Sortable columns
- Pagination
- Search and filtering
- Responsive design

📈 **Data Grid**:
- Advanced data manipulation
- Inline editing
- Export capabilities
""",
                        estimated_time=8,
                        difficulty=3
                    ),
                    LearningStep(
                        id="form_components",
                        title="Building Complex Forms",
                        description="Multi-step forms, validation, and submission",
                        interaction_type=InteractionType.HANDS_ON,
                        content="""
Let's build a multi-step registration form:

1. Add a **Form Container** component
2. Create steps: Personal Info → Account Details → Preferences
3. Add **Step Indicator** to show progress
4. Use **Validation Rules** for each field
5. Add **Conditional Logic** to show/hide sections
6. Configure **Form Submission** to your database

Practice with our guided form builder!
""",
                        estimated_time=15,
                        difficulty=4,
                        completion_criteria={"form_created": True, "validation_added": True, "submission_configured": True}
                    )
                ],
                learning_objectives=[
                    "Master complex data components",
                    "Build professional forms",
                    "Implement validation and logic"
                ],
                prerequisites=["building_first_app"],
                estimated_duration=25,
                tags=["intermediate", "components", "data"],
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        ]
        
        # Add all lessons to the dictionary
        for lesson in getting_started_lessons + visual_builder_lessons:
            lessons[lesson.id] = lesson
        
        return lessons
    
    def _initialize_guidance_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize smart guidance rules"""
        return {
            "new_user": {
                "triggers": ["first_login", "empty_workspace"],
                "response": "welcome_tutorial",
                "priority": 10
            },
            "stuck_on_component": {
                "triggers": ["same_component_selected_5min", "multiple_failed_drops"],
                "response": "component_help",
                "priority": 8
            },
            "repeated_errors": {
                "triggers": ["error_count > 3", "same_error_type"],
                "response": "targeted_help",
                "priority": 9
            },
            "exploration_mode": {
                "triggers": ["clicking_multiple_items", "browsing_components"],
                "response": "discovery_tips",
                "priority": 3
            },
            "almost_complete": {
                "triggers": ["app_90_percent_complete", "deployment_ready"],
                "response": "completion_encouragement",
                "priority": 6
            }
        }
    
    def start_guided_session(self, user_id: str, lesson_id: str) -> Dict[str, Any]:
        """Start a guided learning session"""
        
        if lesson_id not in self.lessons:
            return {"error": "Lesson not found"}
        
        lesson = self.lessons[lesson_id]
        
        # Initialize user session
        session = {
            "user_id": user_id,
            "lesson_id": lesson_id,
            "current_step": 0,
            "started_at": datetime.now(),
            "completed_steps": [],
            "context": {},
            "guidance_enabled": True
        }
        
        self.user_sessions[user_id] = session
        
        # Return first step
        first_step = lesson.steps[0] if lesson.steps else None
        
        return {
            "session_started": True,
            "lesson": {
                "title": lesson.title,
                "description": lesson.description,
                "level": lesson.level.value,
                "estimated_duration": lesson.estimated_duration,
                "total_steps": len(lesson.steps)
            },
            "current_step": {
                "step_number": 1,
                "title": first_step.title,
                "description": first_step.description,
                "content": first_step.content,
                "interaction_type": first_step.interaction_type.value,
                "estimated_time": first_step.estimated_time,
                "code_example": first_step.code_example
            } if first_step else None
        }
    
    def get_next_step(self, user_id: str, completed_criteria: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get the next step in the current lesson"""
        
        if user_id not in self.user_sessions:
            return {"error": "No active session"}
        
        session = self.user_sessions[user_id]
        lesson = self.lessons[session["lesson_id"]]
        
        current_step_index = session["current_step"]
        
        # Mark current step as completed if criteria met
        if completed_criteria and current_step_index < len(lesson.steps):
            current_step = lesson.steps[current_step_index]
            if self._check_completion_criteria(current_step, completed_criteria):
                session["completed_steps"].append(current_step.id)
                session["current_step"] += 1
                current_step_index += 1
        
        # Check if lesson is complete
        if current_step_index >= len(lesson.steps):
            return self._complete_lesson(user_id)
        
        # Get next step
        next_step = lesson.steps[current_step_index]
        
        return {
            "step_number": current_step_index + 1,
            "total_steps": len(lesson.steps),
            "title": next_step.title,
            "description": next_step.description,
            "content": next_step.content,
            "interaction_type": next_step.interaction_type.value,
            "estimated_time": next_step.estimated_time,
            "code_example": next_step.code_example,
            "visual_aid": next_step.visual_aid,
            "completion_criteria": next_step.completion_criteria,
            "progress": (current_step_index + 1) / len(lesson.steps) * 100
        }
    
    def provide_contextual_help(self, user_id: str, context: GuidanceContext) -> Dict[str, Any]:
        """Provide smart, contextual help based on user's current situation"""
        
        guidance = self._analyze_context(context)
        
        # Store guidance session
        self.active_guidance[user_id] = {
            "context": context,
            "guidance": guidance,
            "timestamp": datetime.now()
        }
        
        return guidance
    
    def _analyze_context(self, context: GuidanceContext) -> Dict[str, Any]:
        """Analyze context and provide appropriate guidance"""
        
        guidance_type = "general"
        content = ""
        actions = []
        
        # Detect user difficulty patterns
        if context.error_count > 3:
            guidance_type = "error_help"
            content = """
I notice you're running into some issues. Let me help! 🤝

Common solutions:
1. **Check component connections** - Make sure components are properly linked
2. **Verify data sources** - Ensure your data is correctly formatted
3. **Review permissions** - Check if all required permissions are set
4. **Try the preview mode** - See how users will experience your app

Would you like me to guide you through troubleshooting?
"""
            actions = ["show_troubleshooting_guide", "open_help_center", "schedule_help_session"]
        
        elif context.time_spent > 15 and context.current_action == "component_selection":
            guidance_type = "component_help"
            content = """
Looking for the right component? 🔍

**Quick Tips:**
• Use the **search bar** in the component library
• Components are organized by category (Layout, Input, Display, etc.)
• **Hover** over components to see descriptions
• Check the **Recently Used** section for components you've used before

**Popular choices for beginners:**
• **Button** - For actions and navigation
• **Text** - For headings and content
• **Input** - For user data collection
• **Container** - For organizing other components
"""
            actions = ["show_component_guide", "open_component_search", "suggest_components"]
        
        elif context.current_action == "deployment" and context.difficulty_detected:
            guidance_type = "deployment_help"
            content = """
Ready to deploy? Let me make this easy! 🚀

**Quick Deployment Steps:**
1. **Review your app** - Use preview mode to test everything
2. **Choose hosting** - Vercel and Netlify are great for beginners
3. **Configure settings** - I'll help you with the technical details
4. **One-click deploy** - Just hit the deploy button!

**Pre-deployment checklist:**
✅ All pages load correctly
✅ Forms submit properly  
✅ Images and assets are optimized
✅ Mobile responsiveness tested
"""
            actions = ["run_pre_deployment_check", "show_hosting_options", "start_deployment_wizard"]
        
        else:
            # General encouragement and tips
            tips = [
                "💡 Tip: Use Ctrl+Z to undo any changes you're not happy with",
                "🎨 Tip: Preview your app frequently to see the user experience",
                "📱 Tip: Test your app on different screen sizes using the responsive preview",
                "⚡ Tip: Save your work regularly using Ctrl+S",
                "🔍 Tip: Use the search function to quickly find components or features"
            ]
            
            content = f"""
You're doing great! 👍

{random.choice(tips)}

**Need help with anything specific?**
• Component selection and customization
• Layout and design principles
• Adding functionality and interactions
• Deployment and publishing
"""
            actions = ["show_tips", "open_tutorial", "contact_support"]
        
        return {
            "type": guidance_type,
            "content": content,
            "actions": actions,
            "context_aware": True,
            "timestamp": datetime.now().isoformat()
        }
    
    def _check_completion_criteria(self, step: LearningStep, user_actions: Dict[str, Any]) -> bool:
        """Check if step completion criteria are met"""
        
        if not step.completion_criteria:
            return True  # No specific criteria, consider completed
        
        for criterion, expected_value in step.completion_criteria.items():
            if criterion not in user_actions:
                return False
            
            if user_actions[criterion] != expected_value:
                return False
        
        return True
    
    def _complete_lesson(self, user_id: str) -> Dict[str, Any]:
        """Complete the current lesson and provide celebration/next steps"""
        
        session = self.user_sessions[user_id]
        lesson = self.lessons[session["lesson_id"]]
        
        # Calculate performance metrics
        time_taken = datetime.now() - session["started_at"]
        completion_time = int(time_taken.total_seconds() / 60)  # minutes
        
        # Determine next lesson recommendations
        next_lessons = self._get_recommended_lessons(lesson, user_id)
        
        # Award achievements
        achievements = self._award_achievements(user_id, lesson, completion_time)
        
        return {
            "lesson_completed": True,
            "celebration": f"🎉 Congratulations! You've completed '{lesson.title}'!",
            "performance": {
                "time_taken": completion_time,
                "estimated_time": lesson.estimated_duration,
                "efficiency": min(100, int((lesson.estimated_duration / completion_time) * 100)) if completion_time > 0 else 100
            },
            "achievements": achievements,
            "skills_learned": lesson.learning_objectives,
            "next_steps": {
                "recommended_lessons": next_lessons,
                "practice_suggestions": self._get_practice_suggestions(lesson),
                "advanced_topics": self._get_advanced_topics(lesson)
            }
        }
    
    def _get_recommended_lessons(self, completed_lesson: Lesson, user_id: str) -> List[Dict[str, Any]]:
        """Get recommended next lessons based on what was just completed"""
        
        recommendations = []
        
        # Find lessons that have this lesson as a prerequisite
        for lesson_id, lesson in self.lessons.items():
            if completed_lesson.id in lesson.prerequisites:
                recommendations.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "description": lesson.description,
                    "level": lesson.level.value,
                    "duration": lesson.estimated_duration,
                    "reason": "Next in sequence"
                })
        
        # Add lessons in the same category but higher level
        for lesson_id, lesson in self.lessons.items():
            if (lesson.category == completed_lesson.category and 
                lesson.level.value != completed_lesson.level.value and
                lesson.id != completed_lesson.id):
                
                recommendations.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "description": lesson.description,
                    "level": lesson.level.value,
                    "duration": lesson.estimated_duration,
                    "reason": f"More advanced {lesson.category.value.replace('_', ' ')}"
                })
        
        return recommendations[:3]  # Limit to top 3 recommendations
    
    def _get_practice_suggestions(self, lesson: Lesson) -> List[str]:
        """Get practice suggestions based on lesson content"""
        
        practice_ideas = {
            LessonCategory.GETTING_STARTED: [
                "Try building a different type of app (e.g., portfolio, blog, landing page)",
                "Experiment with different color schemes and fonts",
                "Add more interactive elements to your existing app"
            ],
            LessonCategory.VISUAL_BUILDER: [
                "Create a complex dashboard with multiple data visualizations",
                "Build a multi-page application with navigation",
                "Design a mobile-first responsive layout"
            ],
            LessonCategory.API_INTEGRATION: [
                "Connect to a different API service",
                "Build an app that combines multiple APIs",
                "Create error handling for API failures"
            ]
        }
        
        return practice_ideas.get(lesson.category, [
            "Apply what you learned to a personal project",
            "Share your work with others for feedback",
            "Explore related features and tools"
        ])
    
    def _get_advanced_topics(self, lesson: Lesson) -> List[str]:
        """Get advanced topics related to the lesson"""
        
        advanced_topics = {
            LessonCategory.GETTING_STARTED: [
                "Advanced component customization",
                "State management and data flow",
                "Performance optimization techniques"
            ],
            LessonCategory.VISUAL_BUILDER: [
                "Custom component creation",
                "Advanced animations and transitions",
                "Plugin development and integration"
            ],
            LessonCategory.API_INTEGRATION: [
                "Webhook configuration and handling",
                "Real-time data synchronization",
                "API authentication and security"
            ]
        }
        
        return advanced_topics.get(lesson.category, [
            "Advanced system architecture",
            "Scalability and performance",
            "Enterprise-level features"
        ])
    
    def _award_achievements(self, user_id: str, lesson: Lesson, completion_time: int) -> List[Dict[str, str]]:
        """Award achievements based on lesson completion"""
        
        achievements = []
        
        # First lesson achievement
        if lesson.category == LessonCategory.GETTING_STARTED:
            achievements.append({
                "title": "🎓 First Steps",
                "description": "Completed your first MASS Framework lesson!"
            })
        
        # Speed achievement
        if completion_time <= lesson.estimated_duration * 0.75:
            achievements.append({
                "title": "⚡ Quick Learner",
                "description": "Completed the lesson faster than expected!"
            })
        
        # Category-specific achievements
        category_achievements = {
            LessonCategory.VISUAL_BUILDER: {
                "title": "🎨 Design Master",
                "description": "Mastered visual design and component usage!"
            },
            LessonCategory.API_INTEGRATION: {
                "title": "🔌 Integration Expert",
                "description": "Successfully integrated external services!"
            },
            LessonCategory.DEPLOYMENT: {
                "title": "🚀 Deployment Pro",
                "description": "Launched your app to the world!"
            }
        }
        
        if lesson.category in category_achievements:
            achievements.append(category_achievements[lesson.category])
        
        return achievements
    
    def toggle_guidance(self, user_id: str, enabled: bool) -> Dict[str, Any]:
        """Toggle guidance on/off for a user"""
        
        if user_id in self.user_sessions:
            self.user_sessions[user_id]["guidance_enabled"] = enabled
        
        return {
            "guidance_enabled": enabled,
            "message": f"AI guidance {'enabled' if enabled else 'disabled'}",
            "options": {
                "style_options": [style.value for style in GuideStyle],
                "can_customize": True,
                "can_resume_anytime": True
            }
        }
    
    def get_available_lessons(self, level: LearningLevel = None, category: LessonCategory = None) -> List[Dict[str, Any]]:
        """Get list of available lessons with filtering"""
        
        lessons = []
        
        for lesson_id, lesson in self.lessons.items():
            # Apply filters
            if level and lesson.level != level:
                continue
            if category and lesson.category != category:
                continue
            
            lessons.append({
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "category": lesson.category.value,
                "level": lesson.level.value,
                "duration": lesson.estimated_duration,
                "steps": len(lesson.steps),
                "objectives": lesson.learning_objectives,
                "prerequisites": lesson.prerequisites,
                "tags": lesson.tags
            })
        
        # Sort by level and then by category
        level_order = {level.value: i for i, level in enumerate(LearningLevel)}
        lessons.sort(key=lambda x: (level_order.get(x["level"], 999), x["category"]))
        
        return lessons
    
    def get_learning_path(self, user_level: LearningLevel, goals: List[str]) -> Dict[str, Any]:
        """Generate a personalized learning path"""
        
        # Define learning sequences
        paths = {
            "web_app_builder": [
                "intro_to_mass",
                "building_first_app", 
                "advanced_components",
                "api_integration_basics",
                "deployment_fundamentals"
            ],
            "mobile_app_creator": [
                "intro_to_mass",
                "mobile_first_design",
                "responsive_components",
                "touch_interactions",
                "app_store_deployment"
            ],
            "business_automator": [
                "intro_to_mass",
                "workflow_builder",
                "api_integrations",
                "database_management",
                "automation_rules"
            ]
        }
        
        # Match goals to paths
        recommended_path = []
        if "web development" in goals:
            recommended_path.extend(paths.get("web_app_builder", []))
        if "mobile apps" in goals:
            recommended_path.extend(paths.get("mobile_app_creator", []))
        if "business automation" in goals:
            recommended_path.extend(paths.get("business_automator", []))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_path = []
        for lesson_id in recommended_path:
            if lesson_id not in seen and lesson_id in self.lessons:
                seen.add(lesson_id)
                unique_path.append(lesson_id)
        
        # Convert to lesson details
        path_lessons = []
        total_duration = 0
        
        for lesson_id in unique_path:
            lesson = self.lessons[lesson_id]
            path_lessons.append({
                "id": lesson.id,
                "title": lesson.title,
                "description": lesson.description,
                "duration": lesson.estimated_duration,
                "level": lesson.level.value
            })
            total_duration += lesson.estimated_duration
        
        return {
            "personalized_path": path_lessons,
            "total_duration": total_duration,
            "estimated_completion": f"{total_duration // 60}h {total_duration % 60}m",
            "difficulty_progression": "Beginner → Intermediate → Advanced",
            "goals_addressed": goals,
            "path_benefits": [
                "Structured learning progression",
                "Hands-on practice with real projects",
                "Progressive skill building",
                "Industry best practices",
                "Portfolio-ready applications"
            ]
        }

class GuidanceUI:
    """UI components for the AI Teacher system"""
    
    @staticmethod
    def generate_lesson_card(lesson: Lesson) -> str:
        """Generate HTML for a lesson card"""
        
        level_colors = {
            "beginner": "#10B981",
            "intermediate": "#F59E0B", 
            "advanced": "#EF4444",
            "expert": "#8B5CF6"
        }
        
        return f"""
<div class="lesson-card" data-lesson-id="{lesson.id}">
    <div class="lesson-header">
        <h3 class="lesson-title">{lesson.title}</h3>
        <span class="lesson-level" style="background-color: {level_colors.get(lesson.level.value, '#6B7280')}">
            {lesson.level.value.title()}
        </span>
    </div>
    <p class="lesson-description">{lesson.description}</p>
    <div class="lesson-meta">
        <span class="lesson-duration">⏱️ {lesson.estimated_duration} min</span>
        <span class="lesson-steps">📚 {len(lesson.steps)} steps</span>
        <span class="lesson-category">🏷️ {lesson.category.value.replace('_', ' ').title()}</span>
    </div>
    <div class="lesson-objectives">
        <h4>You'll learn:</h4>
        <ul>
            {chr(10).join([f'<li>{obj}</li>' for obj in lesson.learning_objectives[:3]])}
        </ul>
    </div>
    <button class="start-lesson-btn" onclick="startLesson('{lesson.id}')">
        Start Lesson 🚀
    </button>
</div>
"""
    
    @staticmethod
    def generate_guidance_panel(guidance: Dict[str, Any]) -> str:
        """Generate HTML for contextual guidance panel"""
        
        return f"""
<div class="guidance-panel {guidance['type']}">
    <div class="guidance-header">
        <span class="guidance-icon">🤖</span>
        <h4 class="guidance-title">AI Teacher</h4>
        <button class="close-guidance" onclick="toggleGuidance(false)">×</button>
    </div>
    <div class="guidance-content">
        <div class="guidance-message">
            {guidance['content'].replace(chr(10), '<br>')}
        </div>
        {f'''
        <div class="guidance-actions">
            {chr(10).join([f'<button class="guidance-action" onclick="executeAction("{action}")">{action.replace("_", " ").title()}</button>' for action in guidance.get("actions", [])])}
        </div>
        ''' if guidance.get("actions") else ''}
    </div>
    <div class="guidance-footer">
        <small>💡 Tip: You can toggle guidance anytime with Ctrl+H</small>
    </div>
</div>
"""
    
    @staticmethod
    def generate_progress_tracker(session: Dict[str, Any], lesson: Lesson) -> str:
        """Generate HTML for lesson progress tracker"""
        
        current_step = session.get("current_step", 0)
        total_steps = len(lesson.steps)
        progress_percent = (current_step / total_steps) * 100 if total_steps > 0 else 0
        
        return f"""
<div class="progress-tracker">
    <div class="progress-header">
        <h4>{lesson.title}</h4>
        <span class="progress-text">Step {current_step + 1} of {total_steps}</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress_percent}%"></div>
    </div>
    <div class="step-indicators">
        {chr(10).join([
            f'<span class="step-indicator {"completed" if i < current_step else "current" if i == current_step else "pending"}">{i+1}</span>'
            for i in range(total_steps)
        ])}
    </div>
</div>
"""

# Demo function
async def demo_ai_teacher():
    """Demo of AI Teacher system"""
    
    teacher = AITeacher()
    ui = GuidanceUI()
    
    print("🤖 MASS Framework AI Teacher Demo")
    print("=" * 50)
    
    # Show available lessons
    print("\n📚 Available Lessons:")
    lessons = teacher.get_available_lessons()
    for i, lesson in enumerate(lessons[:3], 1):  # Show first 3
        print(f"{i}. {lesson['title']} ({lesson['level']})")
        print(f"   {lesson['description']}")
        print(f"   Duration: {lesson['duration']} min | Steps: {lesson['steps']}")
        print()
    
    # Start a guided session
    print("🎓 Starting 'Introduction to MASS Framework' lesson...")
    session_result = teacher.start_guided_session("demo_user", "intro_to_mass")
    
    if "current_step" in session_result:
        step = session_result["current_step"]
        print(f"\n📖 Step {step['step_number']}: {step['title']}")
        print(f"Description: {step['description']}")
        print(f"Estimated time: {step['estimated_time']} minutes")
        print("\nContent:")
        print(step['content'])
    
    # Simulate step completion
    print("\n✅ Simulating step completion...")
    next_step = teacher.get_next_step("demo_user", {"step_completed": True})
    
    if "title" in next_step:
        print(f"\n📖 Next Step: {next_step['title']}")
        print(f"Progress: {next_step.get('progress', 0):.1f}%")
    
    # Demo contextual help
    print("\n🆘 Demonstrating contextual help...")
    context = GuidanceContext(
        current_action="component_selection",
        user_location="visual_builder",
        difficulty_detected=True,
        error_count=2,
        time_spent=10,
        previous_actions=["clicked_button", "dragged_component", "failed_drop"]
    )
    
    help_response = teacher.provide_contextual_help("demo_user", context)
    print(f"Guidance Type: {help_response['type']}")
    print(f"Content:\n{help_response['content']}")
    
    if help_response.get('actions'):
        print(f"Available Actions: {', '.join(help_response['actions'])}")
    
    # Generate learning path
    print("\n🛤️ Generating personalized learning path...")
    learning_path = teacher.get_learning_path(
        LearningLevel.BEGINNER,
        ["web development", "mobile apps"]
    )
    
    print(f"Total Duration: {learning_path['estimated_completion']}")
    print(f"Path includes {len(learning_path['personalized_path'])} lessons:")
    
    for i, lesson in enumerate(learning_path['personalized_path'][:3], 1):
        print(f"{i}. {lesson['title']} ({lesson['duration']} min)")
    
    # Show UI examples
    print("\n🎨 Generated UI Components:")
    
    # Sample lesson from our library
    sample_lesson = teacher.lessons["intro_to_mass"]
    
    # Generate lesson card HTML (show first 200 chars)
    lesson_card = ui.generate_lesson_card(sample_lesson)
    print(f"Lesson Card HTML: {lesson_card[:200]}...")
    
    # Generate guidance panel HTML (show first 200 chars)
    guidance_panel = ui.generate_guidance_panel(help_response)
    print(f"Guidance Panel HTML: {guidance_panel[:200]}...")
    
    print("\n🎉 AI Teacher system demonstrates:")
    print("• 📚 Structured lesson library with step-by-step guidance")
    print("• 🤖 Smart contextual help based on user behavior")
    print("• 🛤️ Personalized learning paths")
    print("• 🎯 Achievement system and progress tracking")
    print("• 🎨 Ready-to-use UI components")
    print("• 🔄 Toggleable guidance that adapts to user needs")
    
    return {
        "teacher": teacher,
        "ui": ui,
        "sample_session": session_result,
        "learning_path": learning_path,
        "lessons_count": len(teacher.lessons)
    }

if __name__ == "__main__":
    # Run demo
    import asyncio
    asyncio.run(demo_ai_teacher())
