// Globals
var freq = 7500;  // every 7.5 seconds
var interval = 0;

console.log('------------loaded plugin------------')


function swap_imgs() {
    var imgs = $('img').filter(function() {
        return (parseInt($(this).attr('width')) > 36 &&
                parseInt($(this).attr('height')) > 36 &&
                !$(this).hasClass('pringle-used'))
    });

    console.log('----------replacing imgs-----------');

    imgs.each(function(index) {
        var $img_tag = $(this);
        console.log('[page url] ' + $img_tag.attr('src') );
        // 'pringle-used' means we won't replace this imagine in subsequence
        // runs
        $.post('http://localhost:8000', $img_tag.attr('src'), function(url) {
            console.log('[post recieve] ' + url); 
	        $img_tag.replaceWith(
                "<img class='pringle-used' src='http://" + url +"'>");
        });
    });

    console.log('length of imgs: ' + imgs.length.toString());
}


function start_loop() {
    if (interval > 0) {
        clearInterval(myInterval);
    }
    // run first iteration immediately
    swap_imgs();
    interval = setInterval("swap_imgs()", freq);
}


start_loop();
