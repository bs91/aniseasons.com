'use strict'

var app = angular.module('aniseasons', ['aniseasons.services', 'aniseasons.file', 'wu.masonry']).
  config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
  }
);
