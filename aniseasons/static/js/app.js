'use strict'

Array.prototype.prettify = function() {
  for(var i = 0; i < this.length; i++) {
    this[i] = this[i].charAt(0).toUpperCase() + this[i].slice(1);
  }

  return this.join(', ');
}

var app = angular.module('aniseasons', ['aniseasons.services', 'aniseasons.file', 'wu.masonry', 'ui.bootstrap', 'ui.select2']);

app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

app.filter('genreFilter', function() {
  return function(anime, genres) {
    var items = {
      genres: genres,
      out: []
    };

    if (genres.length !== 0) {
      angular.forEach(anime, function (value, key) {
        for (var i = 0; i < this.genres.length; i++) {
          if (value.genre.indexOf(this.genres[i]) !== -1) {
            this.out.push(value);
            break;
          }
        }
      }, items);
    } else {
      items.out = anime;
    }

    return items.out
  };
});

angular.bootstrap(document, ['aniseasons']);
