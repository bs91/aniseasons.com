'use strict';

function AnimeListCtrl($scope, Anime) {
  $scope.anime = Anime.query();
  $scope.genre = [];
  $scope.query = {};

  $scope.open = function(anime) {
    $scope.selectedAnime = anime;
    $scope.shouldBeOpen = true;
    $('body').addClass('noscroll');
  };

  $scope.close = function() {
    $scope.shouldBeOpen = false;
    $scope.selectedAnime = null;
    $('body').removeClass('noscroll');
  };

  $scope.opts = {};
}

function AdminCtrl($scope, Anime, $http) {
  $scope.anime = Anime.query();

  $scope.add = function() {
    var fd = new FormData();

    angular.forEach($scope.entry, function(value, key) {
      fd.append(key, value);
    });

    return $http({
      method: 'POST',
      url: '/api/anime/',
      headers: {
        'Content-Type': undefined
      },
      data: fd,
      transformRequest: function(data) { return data; }
    });
  }
}
