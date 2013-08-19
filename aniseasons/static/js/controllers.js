'use strict';

function AnimeListCtrl($scope, Anime) {
  $scope.anime = Anime.query();
  $scope.genre = [];

  $scope.query = {
    season: "winter",
    year: new Date().getFullYear()
  };

  $scope.opts = {
    backdropFade: true,
    dialogFade: true
  };

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
    }).success(function(data) {
      $scope.entry = null;
      $scope.anime.unshift(new Anime(data));
    });
  };

  $scope.edit = function(anime) {
    console.log(anime);
  };

  $scope.remove = function(anime) {
    return anime.$remove(function() {
      $scope.anime.splice($scope.anime.indexOf(anime), 1);
    });
  };
}
