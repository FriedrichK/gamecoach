/* global angular */
var app = angular.module('app', [])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document */

var app = angular.module('app'); 
app.controller('RefineSearchController', function($scope, mentorSearchService, mentorSettingsService, refineSettingsService) {
    $scope.refine = mentorSettingsService.initialSettings;
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine);
        refineSettingsService.set($scope.refine);
    };
    $scope.test = function(evt) {
    };
});

app.controller('DocumentReadyController', function(refineSettingsService) {
    angular.element(document).ready(function() {
        var state = refineSettingsService.get();
    });
});

app.controller('MentorListController', function($scope, mentorSearchService) {
    mentorSearchService.getMatchingMentors({}, function(data) {
        $scope.mentors = data;
    });
});
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

app.factory('refineSettingsService', function($location, mentorSettingsService) {
  var initialSettings = mentorSettingsService.initialSettings;
  var refineSettings = getInitialRefineSettings($location, initialSettings);
  return {
    set: function(settings) {
      refineSettings = settings;
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