"""
Branding and Theme System for MASS Framework

This module provides intelligent branding capabilities including:
- Logo analysis and color extraction
- Automatic theme generation
- Brand consistency across the platform
- Customizable UI components
"""

import colorsys
import json
import os
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from PIL import Image, ImageStat
import numpy as np
from sklearn.cluster import KMeans
from fastapi import FastAPI, UploadFile, File
import base64
import io


@dataclass
class ColorPalette:
    """Brand color palette"""
    primary: str = "#3B82F6"      # Blue
    secondary: str = "#8B5CF6"     # Purple  
    accent: str = "#10B981"        # Green
    neutral: str = "#6B7280"       # Gray
    success: str = "#059669"       # Green
    warning: str = "#D97706"       # Orange
    error: str = "#DC2626"         # Red
    background: str = "#F9FAFB"    # Light gray
    surface: str = "#FFFFFF"       # White
    text_primary: str = "#111827"  # Dark gray
    text_secondary: str = "#6B7280" # Gray
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for JSON serialization"""
        return {
            'primary': self.primary,
            'secondary': self.secondary,
            'accent': self.accent,
            'neutral': self.neutral,
            'success': self.success,
            'warning': self.warning,
            'error': self.error,
            'background': self.background,
            'surface': self.surface,
            'text_primary': self.text_primary,
            'text_secondary': self.text_secondary
        }


@dataclass
class Typography:
    """Typography settings"""
    font_family_primary: str = "Inter, system-ui, sans-serif"
    font_family_secondary: str = "JetBrains Mono, monospace"
    font_size_xs: str = "0.75rem"    # 12px
    font_size_sm: str = "0.875rem"   # 14px
    font_size_base: str = "1rem"     # 16px
    font_size_lg: str = "1.125rem"   # 18px
    font_size_xl: str = "1.25rem"    # 20px
    font_size_2xl: str = "1.5rem"    # 24px
    font_size_3xl: str = "1.875rem"  # 30px
    font_size_4xl: str = "2.25rem"   # 36px
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            'font_family_primary': self.font_family_primary,
            'font_family_secondary': self.font_family_secondary,
            'font_size_xs': self.font_size_xs,
            'font_size_sm': self.font_size_sm,
            'font_size_base': self.font_size_base,
            'font_size_lg': self.font_size_lg,
            'font_size_xl': self.font_size_xl,
            'font_size_2xl': self.font_size_2xl,
            'font_size_3xl': self.font_size_3xl,
            'font_size_4xl': self.font_size_4xl
        }


@dataclass
class BrandTheme:
    """Complete brand theme"""
    name: str
    logo_url: Optional[str] = None
    colors: ColorPalette = field(default_factory=ColorPalette)
    typography: Typography = field(default_factory=Typography)
    border_radius: str = "0.5rem"
    shadow_sm: str = "0 1px 2px 0 rgb(0 0 0 / 0.05)"
    shadow_md: str = "0 4px 6px -1px rgb(0 0 0 / 0.1)"
    shadow_lg: str = "0 10px 15px -3px rgb(0 0 0 / 0.1)"
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert theme to dictionary"""
        return {
            'name': self.name,
            'logo_url': self.logo_url,
            'colors': self.colors.to_dict(),
            'typography': self.typography.to_dict(),
            'border_radius': self.border_radius,
            'shadow_sm': self.shadow_sm,
            'shadow_md': self.shadow_md,
            'shadow_lg': self.shadow_lg,
            'created_at': self.created_at
        }


class LogoAnalyzer:
    """Analyzes logos to extract colors and generate themes"""
    
    def __init__(self):
        self.supported_formats = ['PNG', 'JPEG', 'JPG', 'SVG', 'WEBP']
    
    def extract_colors_from_logo(self, image_path: str, num_colors: int = 5) -> List[str]:
        """Extract dominant colors from logo using K-means clustering"""
        try:
            # Open and process image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize for faster processing
            image = image.resize((150, 150))
            
            # Convert to numpy array
            data = np.array(image)
            data = data.reshape((-1, 3))
            
            # Remove transparent/white backgrounds
            data = data[~np.all(data == [255, 255, 255], axis=1)]
            
            if len(data) == 0:
                return self._get_default_colors()
            
            # Use K-means to find dominant colors
            kmeans = KMeans(n_clusters=min(num_colors, len(data)), random_state=42)
            kmeans.fit(data)
            
            # Convert to hex colors
            colors = []
            for center in kmeans.cluster_centers_:
                hex_color = self._rgb_to_hex(int(center[0]), int(center[1]), int(center[2]))
                colors.append(hex_color)
            
            return colors
            
        except Exception as e:
            print(f"Error extracting colors from logo: {e}")
            return self._get_default_colors()
    
    def generate_palette_from_colors(self, dominant_colors: List[str]) -> ColorPalette:
        """Generate a complete color palette from dominant colors"""
        if not dominant_colors:
            return ColorPalette()
        
        # Use the most vibrant color as primary
        primary_color = self._find_most_vibrant_color(dominant_colors)
        
        # Generate complementary colors
        secondary_color = self._generate_complementary_color(primary_color)
        accent_color = self._generate_accent_color(primary_color)
        
        # Create neutral tones
        neutral_color = self._generate_neutral_from_primary(primary_color)
        
        # Generate semantic colors
        success_color = self._adjust_hue(primary_color, 120)  # Green-ish
        warning_color = self._adjust_hue(primary_color, 45)   # Orange-ish
        error_color = self._adjust_hue(primary_color, 0)      # Red-ish
        
        # Background and text colors
        background_color = self._lighten_color(primary_color, 0.95)
        surface_color = "#FFFFFF"
        text_primary = "#111827"
        text_secondary = neutral_color
        
        return ColorPalette(
            primary=primary_color,
            secondary=secondary_color,
            accent=accent_color,
            neutral=neutral_color,
            success=success_color,
            warning=warning_color,
            error=error_color,
            background=background_color,
            surface=surface_color,
            text_primary=text_primary,
            text_secondary=text_secondary
        )
    
    def _find_most_vibrant_color(self, colors: List[str]) -> str:
        """Find the most vibrant/saturated color"""
        max_saturation = 0
        most_vibrant = colors[0]
        
        for color in colors:
            r, g, b = self._hex_to_rgb(color)
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            
            if s > max_saturation:
                max_saturation = s
                most_vibrant = color
        
        return most_vibrant
    
    def _generate_complementary_color(self, hex_color: str) -> str:
        """Generate complementary color"""
        r, g, b = self._hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Shift hue by 180 degrees for complementary
        h = (h + 0.5) % 1.0
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def _generate_accent_color(self, hex_color: str) -> str:
        """Generate accent color (triadic)"""
        r, g, b = self._hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Shift hue by 120 degrees for triadic
        h = (h + 0.33) % 1.0
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def _generate_neutral_from_primary(self, hex_color: str) -> str:
        """Generate neutral color from primary"""
        r, g, b = self._hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Reduce saturation for neutral
        s = s * 0.3
        v = v * 0.7
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def _adjust_hue(self, hex_color: str, hue_shift: int) -> str:
        """Adjust hue by degrees"""
        r, g, b = self._hex_to_rgb(hex_color)
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Adjust hue
        h = (h + hue_shift/360) % 1.0
        
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return self._rgb_to_hex(int(r*255), int(g*255), int(b*255))
    
    def _lighten_color(self, hex_color: str, factor: float) -> str:
        """Lighten color by factor"""
        r, g, b = self._hex_to_rgb(hex_color)
        
        # Lighten by moving towards white
        r = int(r + (255 - r) * factor)
        g = int(g + (255 - g) * factor)
        b = int(b + (255 - b) * factor)
        
        return self._rgb_to_hex(r, g, b)
    
    def _hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def _rgb_to_hex(self, r: int, g: int, b: int) -> str:
        """Convert RGB to hex"""
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _get_default_colors(self) -> List[str]:
        """Get default color palette"""
        return ["#3B82F6", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"]


class ThemeGenerator:
    """Generates complete themes from logos or color preferences"""
    
    def __init__(self):
        self.logo_analyzer = LogoAnalyzer()
        self.themes_storage = {}
    
    def create_theme_from_logo(self, logo_file: str, theme_name: str) -> BrandTheme:
        """Create a complete theme from uploaded logo"""
        try:
            # Extract colors from logo
            dominant_colors = self.logo_analyzer.extract_colors_from_logo(logo_file)
            
            # Generate color palette
            color_palette = self.logo_analyzer.generate_palette_from_colors(dominant_colors)
            
            # Create theme
            theme = BrandTheme(
                name=theme_name,
                logo_url=logo_file,
                colors=color_palette
            )
            
            # Store theme
            self.themes_storage[theme_name] = theme
            
            return theme
            
        except Exception as e:
            print(f"Error creating theme from logo: {e}")
            return self._create_default_theme(theme_name)
    
    def create_custom_theme(self, theme_name: str, primary_color: str, 
                          secondary_color: str = None) -> BrandTheme:
        """Create theme from custom color choices"""
        colors = [primary_color]
        if secondary_color:
            colors.append(secondary_color)
        
        color_palette = self.logo_analyzer.generate_palette_from_colors(colors)
        
        theme = BrandTheme(
            name=theme_name,
            colors=color_palette
        )
        
        self.themes_storage[theme_name] = theme
        return theme
    
    def get_theme(self, theme_name: str) -> Optional[BrandTheme]:
        """Get stored theme by name"""
        return self.themes_storage.get(theme_name)
    
    def list_themes(self) -> List[str]:
        """List all available themes"""
        return list(self.themes_storage.keys())
    
    def generate_css_variables(self, theme: BrandTheme) -> str:
        """Generate CSS custom properties from theme"""
        css_vars = ":root {\n"
        
        # Colors
        for color_name, color_value in theme.colors.to_dict().items():
            css_vars += f"  --color-{color_name.replace('_', '-')}: {color_value};\n"
        
        # Typography
        for font_prop, font_value in theme.typography.to_dict().items():
            css_vars += f"  --{font_prop.replace('_', '-')}: {font_value};\n"
        
        # Other properties
        css_vars += f"  --border-radius: {theme.border_radius};\n"
        css_vars += f"  --shadow-sm: {theme.shadow_sm};\n"
        css_vars += f"  --shadow-md: {theme.shadow_md};\n"
        css_vars += f"  --shadow-lg: {theme.shadow_lg};\n"
        
        css_vars += "}\n"
        return css_vars
    
    def generate_tailwind_config(self, theme: BrandTheme) -> Dict[str, Any]:
        """Generate Tailwind CSS configuration from theme"""
        return {
            "theme": {
                "extend": {
                    "colors": theme.colors.to_dict(),
                    "fontFamily": {
                        "primary": theme.typography.font_family_primary.split(','),
                        "secondary": theme.typography.font_family_secondary.split(',')
                    },
                    "fontSize": {
                        "xs": theme.typography.font_size_xs,
                        "sm": theme.typography.font_size_sm,
                        "base": theme.typography.font_size_base,
                        "lg": theme.typography.font_size_lg,
                        "xl": theme.typography.font_size_xl,
                        "2xl": theme.typography.font_size_2xl,
                        "3xl": theme.typography.font_size_3xl,
                        "4xl": theme.typography.font_size_4xl
                    },
                    "borderRadius": {
                        "DEFAULT": theme.border_radius
                    },
                    "boxShadow": {
                        "sm": theme.shadow_sm,
                        "md": theme.shadow_md,
                        "lg": theme.shadow_lg
                    }
                }
            }
        }
    
    def _create_default_theme(self, theme_name: str) -> BrandTheme:
        """Create default theme"""
        return BrandTheme(name=theme_name)


# Example usage and demo
def demo_branding_system():
    """Demonstrate the branding system capabilities"""
    print("=== MASS Framework Branding System Demo ===")
    
    # Initialize theme generator
    theme_gen = ThemeGenerator()
    
    # Create custom theme
    custom_theme = theme_gen.create_custom_theme(
        theme_name="MASS Framework",
        primary_color="#3B82F6",
        secondary_color="#8B5CF6"
    )
    
    print(f"✓ Created theme: {custom_theme.name}")
    print(f"✓ Primary color: {custom_theme.colors.primary}")
    print(f"✓ Secondary color: {custom_theme.colors.secondary}")
    print(f"✓ Accent color: {custom_theme.colors.accent}")
    
    # Generate CSS variables
    css_vars = theme_gen.generate_css_variables(custom_theme)
    print(f"\n✓ Generated CSS variables ({len(css_vars.split('\\n'))} lines)")
    
    # Generate Tailwind config
    tailwind_config = theme_gen.generate_tailwind_config(custom_theme)
    print(f"✓ Generated Tailwind config with {len(tailwind_config['theme']['extend']['colors'])} colors")
    
    print(f"\n✓ Branding system ready for production!")
    
    return custom_theme


if __name__ == "__main__":
    demo_branding_system()
