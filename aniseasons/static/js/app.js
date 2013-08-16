'use strict'

var app = angular.module('aniseasons', ['aniseasons.services', 'aniseasons.file', 'wu.masonry', 'ui.bootstrap', 'ui.select2']).
config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
  }
);
