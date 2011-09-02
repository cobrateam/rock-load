var iframe = $('report-item');

var select = $('available-tests');
if (select) {
    select.addEvent('change', function(ev) {
        var url = this.getSelected()[0].get('value');
        iframe.set('src', url);
    });
}

function getDocHeight(doc) {
  var docHt = 0, sh, oh;
  if (doc.height) docHt = doc.height;
  else if (doc.body) {
    if (doc.body.scrollHeight) docHt = sh = doc.body.scrollHeight;
    if (doc.body.offsetHeight) docHt = oh = doc.body.offsetHeight;
    if (sh && oh) docHt = Math.max(sh, oh);
  }
  return docHt;
}


if (iframe) {
    iframe.addEvent('load', function(ev) {
        var document = this.contentDocument;
        var height = getDocHeight(document);

        var style = document.createElement('style');
        style.innerHTML = 'body { margin: 0 !important; padding: 0 !important } h1.title:first-child { margin-top: 0; }';
        document.head.appendChild(style);

        iframe.setStyle('height', (height - 150) + 'px');
    });
}

var views_req = $('view-reqs-sec');
var views_duration = $('view-avg-req-time');
var chart_req = $('chart_div');
var chart_duration = $('chart_div_2');

if (views_req) {
    views_req.addEvent('click', function(ev) {
        chart_req.fade('in');
        chart_duration.fade('out');

        views_req.getParent('li').addClass('active');
        views_duration.getParent('li').removeClass('active');

        ev.preventDefault();
        ev.stopPropagation();
    });
}

if (views_duration) {
    views_duration.addEvent('click', function(ev) {
        chart_req.fade('out');
        chart_duration.fade('in');

        views_req.getParent('li').removeClass('active');
        views_duration.getParent('li').addClass('active');

        ev.preventDefault();
        ev.stopPropagation();
    });
}

$$('a.delete-button').addEvent('click', function(ev) {
    var deleteButton = this;
    var result = confirm('Are you sure you want to delete this test? It will delete all gathered data.');
    if (!result) {
        ev.preventDefault();
        ev.stopPropagation();
    }
});
