'use strict';

function AnimeListCtrl($scope, $routeParams, $route, $location, Anime) {
  var lastRoute = $route.current;
  $scope.$on('$locationChangeSuccess', function(event) {
    $route.current = lastRoute;
  });

  $scope.anime = Anime.query();
  $scope.genre = [];
  $scope.mediaToggle = true;

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
    $scope.mediaToggle = true;
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

  $scope.alert = {
    type: 'info',
    msg: 'Admin alerts will be displayed here'
  };

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
      var new_anime = new Anime(data);
      $scope.alert.type = 'success';
      $scope.alert.msg = new_anime.title + ' has successfully been added';
      $scope.anime.unshift(new_anime);
    }).error(function(data) {
      $scope.alert.type = 'error';
      $scope.alert.msg = data.message;
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
      var edited_anime = new Anime(data);
      $scope.alert.type = 'success';
      $scope.alert.msg = edited_anime.title + ' has successfully been updated';
    }).error(function(data) {
      $scope.alert.type = 'error';
      $scope.alert.msg = data.message;
    });
  };

  $scope.remove = function(anime) {
    return anime.$remove(function() {
      $scope.alert.type = 'success';
      $scope.alert.msg = anime.message;
      $scope.anime.splice($scope.anime.indexOf(anime), 1);
    });
  };
}
