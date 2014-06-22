/* global angular */
var app = angular.module('app');

app.factory('mentorSearchService', function($http) {
  return {
    getMatchingMentors: function(data, callable) {
      return $http({
        url: '/api/mentor', 
        method: "GET",
        params: data
      })
        .then(function(result) {
          callable(result.data);
        }
      );
    }
  };
});

function tokenizeValues(values) {
  return values.split(',');
}

function getInitialRefineSettings($location, initialSettings) {
  var urlParameters = $location.search();
  angular.forEach(urlParameters, function(value, key) {
    if(initialSettings[key] !== undefined) {
      var values = tokenizeValues(value);
      angular.forEach(values, function(v, index) {
        if(initialSettings[key][v] !== undefined) {
          initialSettings[key][v] = true;
        }
      });
    } 
  });
  return initialSettings;
}

app.factory('refineSettingsService', function($rootScope, $location, mentorSettingsService) {
  var initialSettings = mentorSettingsService.initialSettings;
  var refineSettings = getInitialRefineSettings($location, initialSettings);
  return {
    set: function(settings) {
      refineSettings = settings;
      $rootScope.$broadcast('refineSettingsUpdated', settings);
    },
    get: function() {
      return refineSettings;
    }
  };
});

app.factory('mentorSettingsService', function() {
  return {
    initialSettings: {
      role: {
          carry: false,
          disabler: false,
          ganker: false,
          initiator: false,
          jungler: false,
          offlaner: false,
          pusher: false,
          support: false
      },
      region: {
          uswest: false,
          useast: false,
          euwest: false,
          eueast: false,
          russia: false,
          southamerica: false,
          seasia: false,
          australia: false
      },
      availability: {
          day: undefined,
          time: undefined
      }
    }
  };
});