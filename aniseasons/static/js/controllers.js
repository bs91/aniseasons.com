'use strict';

function AnimeListCtrl($scope, Anime) {
  $scope.anime = Anime.query();
}
