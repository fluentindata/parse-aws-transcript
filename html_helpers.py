def inject_video_player(youtube_id):
    return '''
    <div id="panel">
    <div id="player"></div>
    </div>

    <script>
      // 2. This code loads the IFrame Player API code asynchronously.
      var tag = document.createElement('script');

      tag.src = "https://www.youtube.com/iframe_api";
      var firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

      // 3. This function creates an <iframe> (and YouTube player)
      //    after the API code downloads.
      var player;
      function onYouTubeIframeAPIReady() {{
        player = new YT.Player('player', {{
          height: '50%',
          width: '100%',
          videoId: '{}',
          playerVars: {{
            'playsinline': 1
          }},
          events: {{
            'onReady': onPlayerReady
          }}
        }});
      }}

      // 4. The API will call this function when the video player is ready.
      function onPlayerReady(event) {{
        // event.target.playVideo();
      }}

      function stopVideo() {{
        player.stopVideo();
      }}
      
      function svt(time) {{
        player.seekTo(time);
        player.playVideo();
      }}
    </script>'''.format(youtube_id)


def inject_header():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <link href="/reset.css" rel="stylesheet">
    <link href="/styles.css" rel="stylesheet">
    
    <link href="/parse-aws-transcript/reset.css" rel="stylesheet">
    <link href="/parse-aws-transcript/styles.css" rel="stylesheet">
    """


def inject_footer():
    return """
    </html>
    """