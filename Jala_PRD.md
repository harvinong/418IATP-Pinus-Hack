# Product Requirements Document: Jala

## 1. Introduction

### 1.1. Problem Statement
The physical art market suffers from a significant information gap. Artists struggle to describe their work comprehensively, often missing nuances that could attract the right buyers. Conversely, customers often don't know the specific vocabulary to describe the art they desire; they recognize their "vibe" or "style" only when they see it. This disconnect makes it difficult for unique, physical art to find an appreciative home and for buyers to discover pieces that truly resonate with them.

### 1.2. Vision & Solution
**Jala** (Indonesian for "Net") is a mobile-first platform designed to bridge this gap. It acts as a smart net, capturing the abstract essence of art and the subjective tastes of users to create perfect matches.

Our solution is twofold:
1.  **For Artists:** We empower artists by using AI to analyze their uploaded artwork. The AI generates a rich set of descriptive meta tags (covering style, subject, color, mood, composition, etc.), far exceeding what could be manually entered. This ensures their art is discoverable by a wider, more relevant audience.
2.  **For Buyers:** We decode a user's abstract taste. Through an initial "style quiz" and continuous learning from their interactions, Jala builds a "Style Profile" for each user.

By matching the artwork's detailed tags with the user's Style Profile, Jala connects customers to art they will love, creating a more efficient and emotionally resonant market for everyone.

## 2. Goals and Objectives

*   **For Artists:** Increase visibility and sales by connecting their art to a targeted, appreciative audience with minimal descriptive effort.
*   **For Buyers:** Create a delightful discovery experience that helps them find and purchase physical art that perfectly matches their personal aesthetic.
*   **For the Platform:** Become the leading marketplace for discovering and purchasing physical art based on nuanced, AI-driven taste-matching.

## 3. Target Audience

*   **Art Sellers (Artists):** Independent artists, galleries, and crafters who create physical artwork and want to expand their market reach.
*   **Art Buyers (Customers):** Individuals looking to purchase art for their homes or offices. They value aesthetics and personal expression but may lack the formal vocabulary to define their taste.

## 4. Features & Functional Requirements

### 4.1. Core Platform

**FR1: User Account Management**
*   Users can sign up and log in using email/password or OAuth (Google, Facebook).
*   Users must select a role upon signup: "Artist" or "Buyer".
*   Users can edit their profile information (name, profile picture, bio).

**FR2: Art Upload & Management (Artist Role)**
*   Artists can upload high-resolution images of their artwork.
*   A simple form will accompany the upload, requiring basic information:
    *   Title
    *   Dimensions (Height x Width x Depth)
    *   Medium (e.g., Oil on Canvas, Watercolor)
    *   Price
    *   Optional artist notes.
*   Artists can view and manage their uploaded art in a personal dashboard.

**FR3: AI-Powered Tagging Engine**
*   Upon image upload, the backend shall process the image through an AI vision model.
*   The model will generate a comprehensive set of tags, including but not limited to:
    *   **Subject:** *Portrait, Landscape, Abstract, Still Life...*
    *   **Style:** *Impressionist, Cubist, Modern, Surrealist...*
    *   **Color Palette:** *Primary Colors, Warm Tones, Monochromatic, Muted...*
    *   **Mood/Feeling:** *Calm, Energetic, Melancholy, Joyful...*
    *   **Composition:** *Symmetrical, Asymmetrical, Minimalist...*
*   Tags will be stored and linked to the artwork in the database.
*   Artists can view the AI-generated tags and have the option to add or remove tags.

**FR4: User Style Profile Creation**
*   **Onboarding Quiz:** First-time buyers will be shown a sequence of 10-15 diverse art images and asked to select the ones they are drawn to.
*   **Profile Generation:** The system will aggregate the tags from the user's selected images to form their initial "Style Profile."
*   **Dynamic Updates:** The Style Profile will be continuously refined based on user activity (likes, saves, time spent viewing certain pieces).

**FR5: Personalized Art Discovery Feed**
*   The main screen for buyers will be a Pinterest-style, infinitely scrolling feed of artwork.
*   The recommendation algorithm will prioritize showing art with tags that strongly match the user's Style Profile.
*   Users can "like" or "save" art to their collections.

**FR6: Search & Filtering**
*   A dedicated search page will allow users to search for art using text queries.
*   The search will match against artwork titles, artist names, and AI-generated tags.
*   Filters will be available to refine results by:
    *   Price Range
    *   Size
    *   Orientation (Horizontal, Vertical, Square)
    *   Primary Color

### 4.2. Non-Functional Requirements

*   **Performance:** The feed must load quickly and scroll smoothly. Image loading should be optimized for mobile devices.
*   **Usability:** The UI must be clean, intuitive, and visually appealing, encouraging browsing and discovery.
*   **Scalability:** The architecture must support a growing number of users, artworks, and API calls for AI analysis.
*   **Security:** All user data, especially login credentials, must be securely stored.

## 5. Success Metrics

*   **Engagement:** Daily/Monthly Active Users (DAU/MAU) for both artist and buyer roles.
*   **Content Growth:** Number of new artworks uploaded per week/month.
*   **Matching Success:** Average number of "likes" or "saves" per user session.
*   **Marketplace Viability:** Number of "Contact Artist" or "Purchase Inquiry" clicks (or a similar metric to track transaction intent).
*   **User Satisfaction:** App store ratings and qualitative feedback from users.
