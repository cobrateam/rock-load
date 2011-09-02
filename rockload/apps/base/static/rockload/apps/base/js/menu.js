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

$$('a.close').addEvent('click', function(e) {
    var div = this.getParent('div.alert-message');
    div.setStyle('display', 'none');
    e.preventDefault();
    e.stopPropagation();
});

$$('.delete-project').addEvent('click', function(ev) {
    var deleteButton = this;
    var result = confirm('Are you sure you want to delete this project? It will delete all its tests and gathered data.');
    if (!result) {
        ev.preventDefault();
        ev.stopPropagation();
    }
});
