'use strict'

var app = angular.module('aniseasons', ['aniseasons.services', 'aniseasons.file', 'wu.masonry', 'ui.bootstrap']).
  config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
  }
);
