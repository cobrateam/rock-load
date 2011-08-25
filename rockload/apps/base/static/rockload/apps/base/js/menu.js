$$('body').addEvent('click', function(e) {
    $$('a.menu').getParent("li").removeClass("open");
});

$$('a.menu').addEvent('click', function(e) {
    console.log(this.getParent('li'));
    this.getParent("li").toggleClass('open');
    e.preventDefault();
    e.stopPropagation();
});

