'use strict';

function AnimeListCtrl($scope, $routeParams, $route, $location, Anime) {
  var lastRoute = $route.current;
  $scope.$on('$locationChangeSuccess', function(event) {
    $route.current = lastRoute;
  });

  $scope.anime = Anime.query();
  $scope.genre = [];

  $scope.open = function(anime) {
    $scope.selectedAnime = anime;
    $scope.shouldBeOpen = true;

    if ($routeParams.slug === undefined) {
      $location.url('anime/' + $scope.selectedAnime.slug);
    }

    $('body').addClass('noscroll');
  };

  $scope.close = function() {
    $scope.shouldBeOpen = false;
    $scope.selectedAnime = null;
    $location.url($scope.query.season + '/' + $scope.query.year);
    $('body').removeClass('noscroll');
  };

  $scope.query = {
    season: $routeParams.season || 'fall',
    year: $routeParams.year || new Date().getFullYear()
  };

  $scope.opts = {
    backdropFade: true,
    dialogFade: true
  };

  $scope.$watch('query.year + query.season', function() {
    if($routeParams.slug === undefined) {
      $location.url($scope.query.season + '/' + $scope.query.year);
    } else {
      $scope.open(Anime.get({slug:$routeParams.slug}));
      delete $routeParams.slug;
    }
  });
}

function AdminCtrl($scope, Anime, $http) {
  $scope.anime;

  $scope.login = function() {
    var fd = new FormData();
    fd.append('username', $scope.user.name);
    fd.append('password', $scope.user.password);

    return $http({
      method: 'POST',
      url: '/api/user/login',
      headers: {
        'Content-Type': undefined
      },
      data: fd,
      transformRequest: function(data) { return data; }
    }).success(function() {
      $scope.user.logged_in = true;
      $scope.anime = Anime.query();
      console.log('logged in');
    }).error(function() {
      console.log('error');
    });
  }

  $scope.logout = function() {

  }

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
    var fd = new FormData();

    angular.forEach(anime, function(value, key) {
      if (key !== '_id' && key !== '$$hashKey') {
        fd.append(key, value);
      }
    });

    return $http({
      method: 'PUT',
      url: '/api/anime/' + anime.slug,
      headers: {
        'Content-Type': undefined
      },
      data: fd,
      transformRequest: function(data) { return data; }
    }).success(function(data) {
      anime = new Anime(data);
    });
  };

  $scope.remove = function(anime) {
    return anime.$remove(function() {
      $scope.anime.splice($scope.anime.indexOf(anime), 1);
    });
  };
}
