'use strict';

angular.module('aniseasons.services', ['ngResource']).
    factory('Anime', function($resource){
  return $resource('api/anime/', {}, {
    query: {method:'GET', isArray:true}
  });
});
