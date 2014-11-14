// Globals
var prev_length;

console.log('------------loaded plugin------------')

function swap_imgs() {
    var imgs = $('img').filter(function() {
        return (parseInt($(this).attr("width")) > 36 &&
                parseInt($(this).attr("height")) > 36)
    });

    console.log('----------replacing imgs-----------');

    imgs.each(function(index) {
        console.log('[page url] ' + $(this).attr('src') );
        $.post('http://localhost:8000', $(this).attr('src'), function(data) {
            console.log('[post success] ' + data.url); 
        }, 'json');
        $(this).replaceWith(
            "<img src='http://www.clker.com/cliparts/X/C/L/8/R/Z/red-box-hi.png'>");
    });

    console.log('LENGTH of images: ' + imgs.length.toString());
    prev_length = imgs.length;
}

swap_imgs();
