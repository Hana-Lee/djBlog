if (!window.djBlog) {
    window.djBlog = {};
}

jQuery(document).ready(function () {
    var $win_height = jQuery(window).height();
    var $frame_height = jQuery(window).width() <= 767 ? $win_height : $win_height - 59;

    jQuery('#iframe').height($frame_height);
    sideBarResize($frame_height);
    jQuery('.wp-pagenavi').hide();
});

jQuery(window).resize(function () {
    var $win_height = jQuery(window).height();
    var $frame_height = jQuery(window).width() <= 767 ? $win_height : $win_height - 59;

    jQuery('#iframe').height($frame_height);
    sideBarResize($frame_height);
});

function sideBarResize(frameHeight) {
    $et_sidebar = jQuery('#sidebar');
    var headerHeight = jQuery("#left-area header").height();
    var sidePadding = $et_sidebar.outerHeight() - $et_sidebar.height();
    var sideHeight = frameHeight - headerHeight - sidePadding - 5;
    $et_sidebar.height(sideHeight);
}

(function ($) {
    var $et_content_area = $('#content-area'),
        $et_sidebar = $('#sidebar'),
        $et_footer = $('#main_footer');

    $(document).ready(function () {
        var $et_image_entry = $('.entry.image'),
            image_entry_element = 'span.zoom',
            main_speed = 700;

        $et_image_entry.find('.photo').hover(function () {
            $(this).find(image_entry_element).css({ opacity: 0, 'display': 'block' }).stop(true, true).animate({ opacity: 1 }, main_speed);
        }, function () {
            $(this).find(image_entry_element).stop(true, true).animate({ opacity: 0 }, main_speed);
        });
    });

    $(window).load(function () {
        $postsContainer = $('#et_posts');
        $postsContainer.masonry({
            itemSelector: '.entry',
            isAnimated: true
        }).imagesLoaded(function(){
            if (!djBlog.originSideBarHeight) {
                    djBlog.originSideBarHeight = $et_sidebar.height();
            }
            var iframeHeight = jQuery("#iframe").height();
            var headerHeight = jQuery("#left-area header").height();
            var contentHeight = jQuery("#content_right").outerHeight();
            var mainHeight = iframeHeight;
            if (iframeHeight < contentHeight) {
                mainHeight = contentHeight;
            }
            var sidePadding = $et_sidebar.outerHeight() - $et_sidebar.height();
            var sideHeight = mainHeight - headerHeight - sidePadding - 5;
            $et_sidebar.height(sideHeight);

            jQuery('.wp-pagenavi').show();
        });

        et_calculate_blocks();
    });

    function et_calculate_blocks() {
        var $et_content_area_right = $('#content_right'),
            $et_left_area = $('#left-area'),
            et_sidebar_top = parseInt($et_sidebar.css('padding-top')),
            et_content_height = $et_content_area_right.innerHeight(),
            et_left_area_height = $et_left_area.innerHeight();

        if (et_left_area_height > et_content_height) $et_footer.css('height', $et_footer.height() + et_left_area_height - et_content_height);
        else $et_sidebar.css('height', $et_content_area.height() - $et_left_area.find('> header').height() - et_sidebar_top);
    }

    $(window).bind( 'smartresize.masonry', function() {
		setTimeout(function() {
            var iframeHeight = jQuery("#iframe").height();
            var headerHeight = jQuery("#left-area header").height();
            var contentHeight = jQuery("#content_right").outerHeight();
            var mainHeight = iframeHeight;
            if (iframeHeight < contentHeight) {
                mainHeight = contentHeight;
            }
            var sidePadding = $et_sidebar.outerHeight() - $et_sidebar.height();
            var sideHeight = mainHeight - headerHeight - sidePadding - 5;
            $et_sidebar.height(sideHeight);
			et_calculate_blocks();
		}, 500);
	});
})(jQuery);