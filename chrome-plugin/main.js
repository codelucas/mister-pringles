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
        var $img_tag = $(this);
        console.log('[page url] ' + $(this).attr('src') );
        $.post('http://localhost:8000', $(this).attr('src'), function(url) {
            console.log("DA DA DA");
            console.log(url);
            console.log('[post success] ' + url); 
	        $img_tag.replaceWith("<img src='http://" + url +"'>");
        });   
    });

    console.log('LENGTH of images: ' + imgs.length.toString());
    prev_length = imgs.length;
}

swap_imgs();
