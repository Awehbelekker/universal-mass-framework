import React from 'react';

interface LogoProps {
  size?: 'small' | 'medium' | 'large';
  className?: string;
  theme?: 'dark' | 'light';
}

const LOGO_SOURCES = {
  dark: '/assets/logo-dark.png',
  light: '/assets/logo.png',
};

const sizeStyles: Record<string, React.CSSProperties> = {
  small: { width: 40, height: 40 },
  medium: { width: 64, height: 64 },
  large: { width: 96, height: 96 },
};

const Logo: React.FC<LogoProps> = ({ size = 'medium', className = '', theme = 'dark' }) => {
  const src = theme === 'light' ? LOGO_SOURCES.light : LOGO_SOURCES.dark;
  return (
    <img
      src={src}
      alt="MASS Framework Logo"
      style={sizeStyles[size]}
      className={className}
      draggable={false}
    />
  );
};

export default Logo; 