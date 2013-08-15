'use strict';

function AnimeListCtrl($scope, Anime) {
  $scope.anime = Anime.query();

  $scope.details = function(anime) {
    console.log(anime)
  }
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
