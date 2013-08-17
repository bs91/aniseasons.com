'use strict';

function AnimeListCtrl($scope, Anime) {
  $scope.anime = Anime.query();
  $scope.genre = [];
  $scope.query = {};

  $scope.open = function(anime) {
    $scope.selectedAnime = anime;
    $scope.shouldBeOpen = true;
  };

  $scope.close = function() {
    $scope.shouldBeOpen = false;
    $scope.selectedAnime = null;
  };

  $scope.opts = {};
}

function AdminCtrl($scope, Anime, $http) {
  $scope.anime = Anime.query();

  $scope.add = function() {
    var self = this;
    var fd = new FormData();

    angular.forEach(self.entry, function(value, key) {
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
