/* global angular */
var mentorResultsApp = angular.module('mentorResultsApp', ['ngAnimate', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global angular, document, window */

var mentorResultsApp = angular.module('mentorResultsApp'); 
mentorResultsApp.controller('RefineSearchController', function($scope, $element, mentorSearchService, mentorSettingsService, refineSettingsService, generateUrlService) {
    angular.element($element).ready(function() {
        $scope.refine = refineSettingsService.get();
        refineSettingsService.set($scope.refine);
    });
    $scope.change = function(evt) {
        mentorSearchService.getMatchingMentors($scope.refine, function() {});
        refineSettingsService.set($scope.refine);
        /*if(window.history !== undefined) {
            window.history.pushState({}, "Mentor search resuls", generateUrlService.buildFromSettings($scope.refine));
        }*/
    };
});

mentorResultsApp.controller('MentorListController', function($scope, mentorSearchService, refineSettingsService) {
    $scope.number = 0;
    $scope.$on('refineSettingsUpdated', function(event, data) {
        var refineSettings = refineSettingsService.get();
        mentorSearchService.getMatchingMentors(refineSettings, function(data) {
            $scope.mentors = data;
            $scope.number = data.length;
        });
    });
    $scope.goToProfile = function(profileId) {
        window.location = '/mentor/' + profileId;
    };
});
/* global angular */
var mentorResultsApp = angular.module('mentorResultsApp');

mentorResultsApp.factory('mentorSearchService', function($http, mentorPreviewService) {
  return {
    getMatchingMentors: function(data, callable) {
      return $http({
        url: '/api/mentor', 
        method: "GET",
        params: data
      })
        .then(function(result) {
          callable(mentorPreviewService.postProcess(result.data));
        }
      );
    }
  };
});

function tokenizeValues(values) {
  if(!values) {
    return [];
  }
  return String(values).split(',');
}

function processBinaryCategory(initialSettings, key, value) {
  if(initialSettings[key] !== undefined) {
    var values = tokenizeValues(value);
    angular.forEach(values, function(v, index) {
      if(initialSettings[key][v] !== undefined) {
        initialSettings[key][v] = true;
      }
    });
    return initialSettings[key];
  }
  return null;
}

function processChoiceCategory(initialSettings, key, value) {
  if(initialSettings[key] !== undefined) {
    console.log(key, value);
  }
}

function getInitialRefineSettings($location, initialSettings) {
  var urlParameters = $location.search();
  angular.forEach(urlParameters, function(value, key) {
    if(key === "roles") {
      initialSettings["roles"] = processBinaryCategory(initialSettings, key, value);
    }
    if(key === "regions") {
      initialSettings["regions"] = processBinaryCategory(initialSettings, key, value);
    }
    if(key === "day") {
      initialSettings["day"] = value;
    }
    if(key === "time") {
      initialSettings["time"] = value;
    }
  });
  return initialSettings;
}

mentorResultsApp.factory('refineSettingsService', function($rootScope, $location, mentorSettingsService) {
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

mentorResultsApp.factory('generateUrlService', function() {
  return {
    buildFromSettings: function(formContent) {
      var url = "/results";
      var urlParts = [];
      urlParts = urlParts.concat(this._buildUrlPart("roles", this._buildCategory("roles", formContent)));
      urlParts = urlParts.concat(this._buildUrlPart("regions", this._buildCategory("regions", formContent)));
      urlParts = urlParts.concat(this._buildUrlPart("day", this._buildChoiceCategory("day", formContent)));
      urlParts = urlParts.concat(this._buildUrlPart("time", this._buildChoiceCategory("time", formContent)));
      console.log(urlParts);
      if(urlParts.length === 0) {
        return url;
      } 
      return url + "?" + urlParts.join('&');
    },
    _buildUrlPart: function(category, value) {
      if(!value || value === "") {
        return [];
      }
      return [category + "=" + value];
    },
    _buildCategory: function(category, formContent) {
      var parts = [];
      angular.forEach(formContent[category], function(value, key) {
        if(value === true) {
          parts.push(key);
        }
      });
      return parts.join(',');
    },
    _buildChoiceCategory: function(category, formContent) {
      return formContent[category];
    }
  };
});

mentorResultsApp.factory('mentorPreviewService', function($filter) {
  var generateTopHeroText = function(entry) {
    if(!entry.data.top_heroes || entry.data.top_heroes === []) {
      return 'No top heroes listed';
    }
    return "Top heroes: " + entry.data.top_heroes.join(', ');
  };

  var generateStatisticsTextGamesPlayed = function(entry, statistics) {
    if(!statistics.games_played) {
      return;
    }
    return "Games played: " + $filter('number')(statistics.games_played, 0);
  };

  var generateStatisticsTextWinRate = function(entry, statistics) {
    if(!statistics.win_rate) {
      return;
    }
    return "Win rate: " + $filter('percentAsString')(statistics.win_rate);
  };

  var generateStatisticsTextSoloMmr = function(entry, statistics) {
    if(!statistics.solo_mmr) {
      return;
    }
    return "Solo MMR: " + $filter('number')(statistics.solo_mmr, 0);
  };

  var generateStatisticsText = function(entry) {
    if(!entry.data || !entry.data.statistics) {
      return;
    }
    var statistics = angular.fromJson(entry.data.statistics);

    var processors = [generateStatisticsTextGamesPlayed, generateStatisticsTextWinRate, generateStatisticsTextSoloMmr];
    var parts = [];
    angular.forEach(processors, function(processor, index) {
      var result = processor(entry, statistics);
      if(result) {
        parts.push(result);
      }
    });
    return parts.join(' | ');
  };

  return {
    postProcess: function(data) {
      angular.forEach(data, function(entry, index) {
        entry.data.topHeroText = generateTopHeroText(entry);
        entry.data.statisticsText = generateStatisticsText(entry);
      });
      return data;
    }
  };
});

mentorResultsApp.factory('mentorSettingsService', function() {
  return {
    initialSettings: {
      roles: {
          carry: false,
          disabler: false,
          ganker: false,
          initiator: false,
          jungler: false,
          offlaner: false,
          pusher: false,
          support: false
      },
      regions: {
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