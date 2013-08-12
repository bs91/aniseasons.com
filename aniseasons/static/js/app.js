'use strict'

angular.module('aniseasons', ['aniseasonsServices', 'wu.masonry']).
  config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
  }
);
