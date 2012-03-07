$(function(){
    //瀑布流
    var speed      = 1000;
    var $container = $('.container-fluid .content .items');

    $container.imagesLoaded(function(){
        $container.masonry({
            singleMode      : true,
            columnWidth     : 240,
            itemSelector    : '.item',
            animate         : true,
            animationOptions: {
                duration: speed,
                queue   : false
            }
        });
    });

    //无限滚动
    $('.container-fluid .content .items').infinitescroll({
        navSelector    : "#page_nav",
        nextSelector   : "#page_nav a",
        itemSelector   : ".container-fluid .content .items .item",
        debug          : false,
        loadingImg     : '/static/loader.gif',
        loadingText    : "<em>加载更多"+config.site_word+"...</em>",
        donetext       : "<em>没有更多的"+config.site_word+"了</em>",
        errorCallback  : function() {
            $('#infscr-loading').animate({opacity: .8},2000).fadeOut('normal');
        }},
        function( newElements ) {
            var $newElems = $( newElements ).css({ opacity: 0 });
            $newElems.imagesLoaded(function(){
                $newElems.animate({ opacity: 1 });
                $container.masonry( 'appended', $newElems, true ); 
            });
        });

    //返回到页首
    var $backToTopTxt = "返回顶部",
        $backToTopEle = $('<div class="backToTop"></div>')
            .appendTo($("body"))
            .text($backToTopTxt)
            .attr("title", $backToTopTxt)
            .click(function () {
                $("html, body").animate({ scrollTop: 0 }, 120);
            }), 
        $backToTopFun = function () {
            var st = $(document).scrollTop(), 
                winh = $(window).height();
            (st > 0) ? $backToTopEle.show() : $backToTopEle.hide();

            //IE6下的定位
            if (!window.XMLHttpRequest) {
                $backToTopEle.css("top", st + winh - 166);
            }
        };
    $(window).bind("scroll", $backToTopFun);
    $(function () { $backToTopFun(); });

    //分享到新浪
    var shareToWeibo = function(e){
        var item = $(e.target).closest('.item');
        
        var itemid       = item.find('a.image').attr('itemid'); 
        var ralateUid    = item.find('a.image').attr('userid');
        var shareUrl     = encodeURIComponent('http://shailiwu.sinaapp.com/show/' + itemid);
        var shareText    = encodeURIComponent('我好喜欢这个'+config.site_word+'呀。#晒'+config.site_word+'#');
        var shareImg     = encodeURIComponent(item.find('a.image img').attr('src'));
        var url          = 'http://v.t.sina.com.cn/share/share.php?appkey=3355748460' +
            '&url='      + shareUrl  +
            '&title='    + shareText +
            '&pic='      + shareImg  +
            '&ralateUid='+ ralateUid +
            '&source=&sourceUrl&content=utf-8';

        $.get('/api/hits',{itemid:itemid});

        var share = function(){
            var openParam = "toolbar=0,status=0,resizable=1,width=440,height=430,left=" +
                (screen.width-440)/2 + ',top=' + (screen.height-430)/2;
            if(!window.open(url,'mb', openParam)){
                u.href=[f,p].join('');
            }
        };


        if(/Firefox/.test(navigator.userAgent))
            setTimeout(share,0);
        else 
            share();
    };
    $(".container-fluid .content .item .bars a.share").live('click', shareToWeibo);

    //喜欢
    var likeLiwu = function(e){
        var item = $(e.target).closest('.item'),
            hits = parseInt(item.find('a.like span').text()),
            itemid = item.find('a.image').attr('itemid'); 
        $.get('/api/hits',{itemid:itemid});
        item.find('a.like span').text(++hits);
    };
    $(".container-fluid .content .item .bars a.like").live('click',likeLiwu);

    function SetCookie(name,value)
    {
        var Days = 30; 
        var exp  = new Date();
        exp.setTime(exp.getTime() + Days*24*60*60*1000);
        document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
    }
    function getCookie(name)
    {
        var arr = document.cookie.match(new RegExp("(^| )"+name+"=([^;]*)(;|$)"));
        if(arr != null) return unescape(arr[2]); return null;
    }

    //微博登录
    $(".topbar .weibo_login").click(function(){
        WB2.login(function(e){
            WB2.anyWhere(function(W){
                W.parseCMD("/account/verify_credentials.json", function(sResult, bStatus){
                    if(bStatus == true) {
                        $(".topbar .weibo_login").replaceWith('欢迎您'+sResult.screen_name);
                        SetCookie('sinauserid', sResult.id);
                        SetCookie('nickname', sResult.screen_name);
                    }
                });
            });
        });
    });

    //已经登录后的状态
    var nickname = getCookie('nickname');
    if(nickname){
        $(".topbar .weibo_login").replaceWith('<span>欢迎您'+nickname+'</span>');
    }
});

