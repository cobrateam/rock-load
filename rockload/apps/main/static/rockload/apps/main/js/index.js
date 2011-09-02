$$('a.delete-button').addEvent('click', function(ev) {
    var deleteButton = this;
    var result = confirm('Are you sure you want to delete this result? It will delete all its gathered data.');
    if (!result) {
        ev.preventDefault();
        ev.stopPropagation();
    }
});

$$('.test-result-row').addEvent('click', function(ev) {
    var url = this.get('data-url');
    window.location = url;
});
