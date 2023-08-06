function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
      results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function toggleCollapsedSimulatedInlines(evt) {
  var elem = $(this);
  if (this.tagName == 'H2'){
    elem = $(this).find('a.simulated-inline-collapse-toggle');
  }

  var childs = $(elem.parent('h2').nextAll());

  childs.each(function(i, c) {
    var child = $(c);
    if (child.is(":hidden")) {
      child.show();
      elem.html(gettext('Hide'));
    } else {
      child.hide();
      clearQueryString(child);
      elem.html(gettext('Show'));
    }
  });

  return false;
}

// Clear the query string when the inline is closed
function clearQueryString(elem) {
  var inlineName = elem.attr('id').replace('-table', '');
  if (inlineName) {
    var pageParam = getParameterByName(inlineName + '-page');
    if (pageParam) {
      // TODO: check if works with more than one qs
      var search = window.location.search.replace(inlineName + '-page=' + pageParam, '');

      var lastChar = search[search.length - 1];
      if (lastChar === '?' || lastChar === '&') {
        search = search.slice(0, -1);
      }

      var newUrl = window.location.origin + window.location.pathname + search;

      window.history.replaceState({}, document.title, newUrl);
    }
  }
}

// Keep inline opened after reload on change page
function hideIfOnFirstPage(inlineRoot) {
  var inlineName = $(inlineRoot).attr('id').replace('-list', '');
  var pageParam = getParameterByName(inlineName + '-page');

  return function(i, elem) {
    if (pageParam){$(elem).show();} else {$(elem).hide();}
  };
}

(function($) {
  $(document).ready(function() {
    $('div.collapse-simulated-inline').each(function() {

      var h2 = $(this).find('h2:first');
      var childs = $(h2.nextAll(':visible'));
      var text = 'Show';

      childs.each(hideIfOnFirstPage(this));

      h2.append('(<a class="simulated-inline-collapse-toggle" href="#">' + gettext(text) + '</a>)');

      h2.find('a.simulated-inline-collapse-toggle')
        .bind("click", toggleCollapsedSimulatedInlines)
        .removeAttr('href')
        .css('cursor', 'pointer');

      h2.bind("click", toggleCollapsedSimulatedInlines)
        .css('cursor', 'pointer');

    });
  });
})($ || jQuery || django.jQuery);
