(function($){
  $(function() {
    var banner = $("#backgroundImg");
    var banner2 = $("#backgroundImg2");
    var useBanner2 = true;
    var i = 0;
    var loading = false;

    function updateBanner()
    {
      if (loading) return;
      if (useBanner2)
      {
        var img = new Image();
        loading = true;
        img.onload = function()
        {
          banner2.css("background-image", 'url("' + images[i] + '")');

          banner.css("z-index", "-5");
          banner2.css("z-index", "-6");

          banner.fadeOut(1000, callback=function()
          {
            i++; i %= images.length;
          });
          banner2.fadeIn(0);
          loading = false;
        };
        img.src = images[i];
      }
      else
      {
        var img = new Image();
        loading = true;
        img.onload = function()
        {
          banner.css("background-image", 'url("' + images[i] + '")');

          banner.css("z-index", "-6");
          banner2.css("z-index", "-5");

          banner2.fadeOut(1000, callback=function()
          {
            i++; i %= images.length;
          });
          banner.fadeIn(0);
          loading = false;
        };
        img.src = images[i];
      }
      useBanner2 = !useBanner2;
    }

    banner2.fadeOut(0);
    setInterval(updateBanner, 5000);
    updateBanner();
  });
})(jQuery);
