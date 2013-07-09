if (!window.djBlog) {
    window.djBlog = {};
}

jQuery(document).ready(function() {
    var $win_height = jQuery(window).height();
    var $frame_height = jQuery(window).width() <= 767 ? $win_height : $win_height - 59;
    jQuery('#iframe').height($frame_height);
});

jQuery(window).resize(function() {
    var $wheight = jQuery(window).height();
    var $fheight = jQuery(window).width() <= 767 ? $wheight : $wheight - 59;
    jQuery('#iframe').height($fheight);
});
