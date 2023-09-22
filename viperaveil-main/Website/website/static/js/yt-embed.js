var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    width: '100%',
    height: '100%',
    videoId: '4aWOKVM4m1I', //Vipera - 4aWOKVM4m1I //Test Vid - RGoPU-OLQHE //Pax klwUt29HSn0
    playerVars: { 'autoplay': 1, 'playsinline': 1},
    events: {
      'onReady': onPlayerReady,
      onStateChange:
    function(e) {
        if (e.data === YT.PlayerState.ENDED){
            player.playVideo();
        }
    }
    }
  });
}
function onPlayerReady(event) {
  event.target.mute();
  event.target.playVideo();
}