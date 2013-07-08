'use strict';

angular.module('aniseasonsServices', ['ngResource']).
    factory('Anime', function($resource){
  return $resource('api/anime/', {}, {
    query: {method:'GET', isArray:true}
  });
});
