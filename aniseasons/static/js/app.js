'use strict'

Array.prototype.prettify = function() {
  var genre_display = [];
  for(var i = 0; i < this.length; i++) {
    genre_display[i] = this[i].charAt(0).toUpperCase() + this[i].slice(1);
  }

  return genre_display.join(', ');
}

// Weird scoping issue with 'this'. Why can I sometimes do:
// 
//   this = this.substring();
//
// but get an "Invalid Assignment Left-Hand Side" at other times?
//
 
String.prototype.truncate = function(length) {
  length = typeof length !== 'undefined' ? length : 100;
  if (this.length > length) {
    var str = this.substring(0, length);
    
    str = str.substring(0, Math.min(str.length, str.lastIndexOf(" ")));
    str = str + " ...";
    return str;
  } else {
    return this;
  }
}

var app = angular.module('aniseasons', ['aniseasons.services', 'aniseasons.file', 'wu.masonry', 'ui.bootstrap', 'ui.select2']);

app.config(function($interpolateProvider){
  $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
});

app.config(function($locationProvider, $routeProvider) {
  $locationProvider.html5Mode(true);
  $routeProvider.when('/', { templateUrl: '/templates/index', controller: AnimeListCtrl });
  $routeProvider.when('/anime/:slug', { templateUrl: '/templates/index', controller: AnimeListCtrl });
  $routeProvider.when('/:season/:year', { templateUrl: '/templates/index', controller: AnimeListCtrl });
  $routeProvider.when('/admin', { templateUrl: '/templates/admin', controller: AdminCtrl });
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
