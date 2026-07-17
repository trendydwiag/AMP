# AMP Studio — Design Tokens

## Overview

All visual properties in AMP Studio are defined as CSS custom properties in `static/css/amp-studio/design-tokens.css`. This ensures consistency and enables theme switching.

## Color Tokens

### Coffee Palette (Brand)
```css
--amp-coffee-50:  #FAF7F3;   /* Lightest — page backgrounds */
--amp-coffee-100: #F5F0EA;   /* Light — card backgrounds */
--amp-coffee-200: #E7DDD3;   /* Medium light — borders */
--amp-coffee-300: #C89B6D;   /* Medium — icons, accents */
--amp-coffee-400: #8C5A3C;   /* Medium dark — hover states */
--amp-coffee-500: #6B4226;   /* Dark — active states */
--amp-coffee-600: #4E2F1F;   /* Primary — buttons, links */
--amp-coffee-700: #3A2318;   /* Darker — active text */
--amp-coffee-800: #2B1A13;   /* Very dark — headings */
--amp-coffee-900: #1A0F0B;   /* Darkest — text on light */
```

### Semantic Colors
```css
/* Backgrounds */
--amp-surface-primary:    #FFFFFF;    /* Cards, sidebar */
--amp-surface-secondary:  #FAF7F3;   /* Page background */
--amp-surface-tertiary:   #F5F0EA;   /* Hover states */

/* Text */
--amp-text-primary:    #1A0F0B;   /* Headings, important */
--amp-text-secondary:  #4E2F1F;   /* Body text */
--amp-text-tertiary:   #8C5A3C;   /* Timestamps, hints */
--amp-text-inverse:    #FFFFFF;   /* On dark backgrounds */

/* Borders */
--amp-border-light:  #E7DDD3;   /* Default borders */
--amp-border-medium: #C89B6D;   /* Emphasis borders */

/* Status */
--amp-success: #2F9E44;   /* Published, online */
--amp-warning: #E67700;   /* Pending, caution */
--amp-danger:  #E53935;   /* Error, offline, live */
--amp-info:    #339AF0;   /* Informational */

/* Status Light Variants */
--amp-success-light: #EAFBE7;
--amp-warning-light: #FFF9DB;
--amp-danger-light:  #FFF5F5;
--amp-info-light:    #E7F5FF;
```

## Spacing Tokens
```css
--amp-space-0:  0px;
--amp-space-1:  4px;
--amp-space-2:  8px;
--amp-space-3:  12px;
--amp-space-4:  16px;
--amp-space-5:  20px;
--amp-space-6:  24px;
--amp-space-8:  32px;
--amp-space-10: 40px;
--amp-space-12: 48px;
--amp-space-16: 64px;
```

## Typography Tokens
```css
--amp-font-heading: 'Poppins', sans-serif;
--amp-font-body:    'Inter', sans-serif;
--amp-font-mono:    'JetBrains Mono', monospace;

--amp-weight-normal:   400;
--amp-weight-medium:   500;
--amp-weight-semibold: 600;
--amp-weight-bold:     700;

--amp-text-xs:  0.75rem;   /* 12px */
--amp-text-sm:  0.875rem;  /* 14px */
--amp-text-base: 1rem;     /* 16px */
--amp-text-lg:  1.125rem;  /* 18px */
--amp-text-xl:  1.25rem;   /* 20px */
--amp-text-2xl: 1.5rem;    /* 24px */
--amp-text-3xl: 1.875rem;  /* 30px */
```

## Radius Tokens
```css
--amp-radius-sm:   6px;
--amp-radius-md:   8px;
--amp-radius-lg:   12px;
--amp-radius-xl:   16px;
--amp-radius-2xl:  20px;
--amp-radius-full: 9999px;
```

## Shadow Tokens
```css
--amp-shadow-sm:       0 1px 2px rgba(0,0,0,0.05);
--amp-shadow-md:       0 4px 6px rgba(0,0,0,0.07);
--amp-shadow-lg:       0 10px 15px rgba(0,0,0,0.1);
--amp-shadow-xl:       0 20px 25px rgba(0,0,0,0.15);
--amp-shadow-dropdown: 0 10px 30px rgba(0,0,0,0.12);
--amp-shadow-modal:    0 25px 50px rgba(0,0,0,0.25);
```

## Transition Tokens
```css
--amp-transition-fast:   150ms ease;
--amp-transition-base:   200ms ease;
--amp-transition-slow:   300ms ease;
--amp-transition-spring: 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

## Layout Tokens
```css
--amp-sidebar-width:          260px;
--amp-sidebar-collapsed-width: 72px;
--amp-header-height:          64px;
--amp-player-height:          64px;
--amp-content-max-width:      1440px;
```

## Z-Index Tokens
```css
--amp-z-base:     1;
--amp-z-dropdown: 1000;
--amp-z-sticky:   1020;
--amp-z-fixed:    1030;
--amp-z-modal:    1050;
--amp-z-popover:  1060;
--amp-z-tooltip:  1070;
--amp-z-toast:    1080;
--amp-z-sidebar:  1040;
--amp-z-header:   1035;
--amp-z-player:   1025;
```
