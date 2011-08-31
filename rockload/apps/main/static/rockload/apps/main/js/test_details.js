var iframe = $('report-item');

$('available-tests').addEvent('change', function(ev) {
    var url = this.getSelected()[0].get('value');

    iframe.set('src', url);
});

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


iframe.addEvent('load', function(ev) {
    var document = this.contentDocument;
    var height = getDocHeight(document);

    var style = document.createElement('style');
    style.innerHTML = 'body { margin: 0 !important; padding: 0 !important } h1.title:first-child { margin-top: 0; }';
    document.head.appendChild(style);

    iframe.setStyle('height', height + 'px');
});
