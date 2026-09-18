<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>School Workspace Lounge</title>
  <style>
    /* 1. Global Reset & Immersive Background Canvas */
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    body, html {
        background-color: #121214; /* Your custom midnight theme background */
        height: 100vh;
        width: 100vw;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. Sleek Branded Top Navigation Header Bar */
    .custom-header {
        background-color: #1a1a1e;
        color: #ffffff;
        padding: 15px 25px;
        font-weight: bold;
        font-size: 16px;
        letter-spacing: 0.5px;
        border-bottom: 1px solid #29292e;
        display: flex;
        align-items: center;
        gap: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }

    .header-icon {
        color: #8257e5; /* Lavender icon accent matching your style */
    }

    /* 3. Full-Screen Interactive Embed Frame Container */
    .chat-wrapper {
        flex: 1;
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: #121214;
    }

    /* Overriding Minnit's default parameters to make it expand 100% full-width */
    .minnit-chat-sembed, iframe {
        width: 100% !important;
        height: 100% !important;
        border: none !important;
    }

    /* Hidden credits styling block to keep the site design clean and premium */
    .powered-by-minnit {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }
  </style>
</head>
<body>

  <!-- Custom Header Bar making it feel like YOUR unique platform site -->
  <div class="custom-header">
    <span class="header-icon">🏫</span> 
    <span>School Workspace Lounge</span>
  </div>

  <!-- The Main Live Communication Viewer Wrapper -->
  <div class="chat-wrapper">
    
    <!-- 🔌 YOUR EXACT MINNIT CONNECTION CODES STITCHED INSIDE -->
    <script src="https://minnit.chat/js/embed.js?c=1772345192" defer></script>
    <span class="minnit-chat-sembed" data-chatname="https://organizations.minnit.chat/347179743601155/c/Main?embed" data-style="width:100%; height:100%;" data-version="1.55">Chat</span>

  </div>

</body>
</html>
