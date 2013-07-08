'use strict'

angular.module('aniseasons', ['aniseasonsServices']).
  config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
  }
);
