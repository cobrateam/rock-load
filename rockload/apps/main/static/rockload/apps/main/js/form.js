$('cancel').addEvent('click', function(ev) {
    window.history.back();
    ev.preventDefault();
});
