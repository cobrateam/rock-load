window.addEvent('click', function(e) {
    $$('a.menu').getParent("li").removeClass("open");
});

$$('a.menu').addEvent('click', function(e) {
    var li = this.getParent('li');
    var isOpen = li.hasClass('open');
    $$('a.menu').getParent('li').removeClass('open');
    if (isOpen) {
        li.removeClass('open');
    } else {
        li.addClass('open');
    }
    e.preventDefault();
    e.stopPropagation();
});

