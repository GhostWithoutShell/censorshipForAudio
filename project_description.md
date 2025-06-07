# Project: Сensorship audio for influencers
## Objective:
Create web app using vanilla JavaScript on the client side and FastAPI on the server side.
## Architecture:
- **Client-side**: Pure (vanilla) JavaScript without frameworks.
- **Server-side**: FastAPI (Python 3.11+).
- **Data exchange format**: JSON.
- **Communication**: REST API

## Functionality of front-end:
1. Web application with three pages
   - First page it is page with name of application ("Project: Сensorship audio for influencers"),
     that page has file selection input, language input (dropdown with values : Russian, English),
     after file and language selected button submit is enable
   - Second page with loading bar that shows progress of processing audio file
   - Third page is result of processing audio with output result audio
2. Styles of pages
    - All pages should be in one color style, and layout should use best practises UX/UI
    - Color style should be light-green with black contrast
3. Business rules
    - Input with audio file should shows in exployer only mp3, wav files
    - Button submit should be unenable while fields : language, audio file
    - Input with lanugage`s should have only two options, Russian, English
4. Data formats:
    - All data should be in json format
    - Audio data should be transformed into base64 string
## Functionality of back-end
1. Add endpoint to call python script that will be processing audio
   - Add configs to call python scripts
   - Selected file should be validated to check supporting format (mp3, wa)
   - Api endpoint for sending audio should request json with format :
      {
       "language" : "Example"m
       "audio_base64" : "base64 string with audio data"
      }
## Restrictions:
- **Do not use frameworks as example:  React, Vue, Angular.**
- **Minimum external dependencies on the frontend.**
- **The server on FastAPI should be divided into layers (routes, schemes, logic)**.

## Expencted result:
- `index.html` with connected JS (example `main.js`)
- `main.py` python server with FastAPI library
- `instructions_start.md` with instuctions to start application