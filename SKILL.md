---
name: travel-journal
description: "Generate travel journals (游记) from Apple Calendar events and local Apple Photos. This skill should be used when the user wants to create a travel journal, travelogue, or trip report based on their calendar itinerary, local photos, and a specified writing style. Triggers include: 'write a travel journal', 'create a travelogue', '写游记', '编制游记', '旅行记录', or any request combining calendar data with photo content to produce a narrative."
---

# Travel Journal Generator (旅行游记生成器)

## Overview

A workflow-based skill for generating travel journals by combining two data sources: Apple Calendar (itinerary) and Apple Photos (local photo library). The output is a clean HTML file with minimal styling, suitable for publishing on Zhihu, WeChat Official Accounts, Xiaohongshu, or other platforms.

## Prerequisites

This skill depends on two other skills that must be available:

1. **apple-calendar** — for reading calendar events
2. **apple-photos** — for accessing local photo library

Load each skill as needed during the workflow. If a skill is unavailable, inform the user and suggest manual alternatives.

## Workflow

### Phase 1: Gather Parameters

Collect the following from the user. Use sensible defaults where possible.

| Parameter | Required | Example |
|-----------|----------|---------|
| Date range | Yes | 2025-10-02 ~ 2025-10-08 |
| Destination region | Yes | 日本北陆 |
| Writing style reference URL | No | A public article URL (Zhihu, blog, etc.) |
| Output filename | No | default: `travel-journal-{destination}-{year-month}.html` |

If no style reference URL is provided, use the default style defined in `references/writing-style-guide.md`.

### Phase 2: Collect Itinerary from Apple Calendar

1. Load the **apple-calendar** skill
2. Query calendar events for the specified date range
3. Extract: event titles, times, locations, notes
4. Organize events by date to form the day-by-day itinerary skeleton
5. Store the structured itinerary for use in Phase 5

### Phase 3: Collect Local Photos from Apple Photos

1. Load the **apple-photos** skill
2. Search for photos matching:
   - Date range of the trip
   - Geographic region of the destination (use location/GPS data)
3. Select a diverse set of photos:
   - **Prefer favorited photos**: prioritize photos the user has marked as favorites (♥) in Apple Photos
   - **No faces**: exclude photos where human faces are the primary subject; landscapes, architecture, food, objects, and wide shots are preferred
   - Include landmarks, scenic shots, food, transit, and detail/texture shots
   - Prioritize variety across locations and times of day
4. Export selected photos to the working directory

### Phase 4: Extract Writing Style (if reference URL provided)

If the user provides a style reference URL:

1. Use the default **web search** capability to fetch the article content from the URL
2. Analyze the article for:
   - Punctuation style (English vs Chinese punctuation)
   - Sentence length and structure patterns
   - Level of emotional expression (restrained vs effusive)
   - Use of practical information (transport, logistics)
   - Humor style and frequency
   - Section/heading structure
   - What the author avoids (purple prose, clichés, etc.)
3. Create a concise style profile to guide generation
4. The extracted style OVERRIDES the default style in `references/writing-style-guide.md`

If no URL is provided, read and follow `references/writing-style-guide.md` as-is.

### Phase 5: Generate the Journal

Using the collected itinerary, photos, and style guide:

1. **Structure**: Create a day-by-day narrative following the calendar itinerary
2. **Photo-driven narration** (critical rule):
   - The narrative must revolve around the selected photos — each photo is a narrative anchor
   - For scenes/locations captured in photos: describe what is shown, expand with relevant context
   - For itinerary items NOT covered by any photo: include only a minimal mention (one or two sentences) based on the calendar event; do NOT fabricate visual details or elaborate descriptions for unphoto'd events
   - The ratio of photo-backed content to calendar-only content should be heavily skewed toward photos
3. **Content per day**:
   - Opening: Where, basic logistics
   - Body: Walk through the day anchored by photos, in chronological order
   - Photos: Insert images at the point in the narrative where they are discussed
   - Practical info: Weave in transport and logistics naturally
4. **Writing rules** (apply the style guide strictly):
   - Match the identified or default punctuation style
   - Match the identified or default tone and restraint level
   - No unsupported flourishes — only write about what the data supports
   - No discussion of prices, costs, money-saving tips, or budget topics
4. **Photos in HTML**:
   - Use `<img>` tags with local file paths or base64 encoding
   - Add brief captions using `<p class="photo-caption">` when appropriate
   - Use Apple Photos as the image source
   - Ensure good coverage across all days and locations

### Phase 6: Assemble HTML Output

1. Read the HTML template from `assets/journal-template.html`
2. Replace `{{TITLE}}` with the journal title (e.g., "2025-10 日本北陆游记")
3. Replace `{{CONTENT}}` with the generated HTML content
4. For images: use relative paths if images are in a subdirectory, or embed as base64 for single-file portability
5. Save the final HTML file
6. Present the result using preview_url

### Phase 7: Review and Iterate

After presenting the initial draft:

1. Ask the user for feedback
2. Common adjustments:
   - Add/remove photos
   - Adjust tone (more/less detail, more/less humor)
   - Fix factual inaccuracies
   - Rearrange sections
3. Regenerate affected sections only, preserving the rest

## Style Reference

The default writing style guide is at `references/writing-style-guide.md`. Key principles:

- **English punctuation throughout** (commas, periods, not ，。)
- **Photo-driven narration**: anchor the story around photos; minimize elaboration on events not captured in photos
- **Factual narration**: record what happened, skip the feelings
- **Composed and steady tone**: no internet slang, no trendy buzzwords (e.g. "yyds", "绝绝子", "氛围感", "打卡")
- **Short sentences**, calm and conversational
- **No purple prose**: no metaphors, no life lessons, no poetry quotes
- **No price/cost discussion**: do not mention prices, expenses, budgets, or money-saving tips
- **Logistics only**: transport methods, booking/reservation info where relevant
- **Occasional dry humor**: self-deprecating, never forced

## HTML Output

The HTML template at `assets/journal-template.html` provides:

- Clean, responsive layout (max-width 720px)
- System font stack with Chinese font support
- Minimal styling that works across platforms
- Image handling with auto-sizing and optional captions

The output HTML should be self-contained enough to paste into any publishing platform's editor.

## Tips for Best Results

- Calendar events with detailed notes/locations produce better itineraries
- If web search cannot retrieve the style reference article content, do not attempt to log in or use a browser agent — simply ask the user to paste key excerpts
- For multi-city trips, use city names as h2 headers within each day
- Keep the journal length proportional to the trip: ~500-800 words per day is a good target
