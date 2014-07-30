/* global angular */
var mentorProfileApp = angular.module('mentorProfileApp', ['ngAnimate', 'gamecoachShared', 'gamecoachNavigation'])
	.config(['$locationProvider', function($locationProvider) {
        $locationProvider.html5Mode(true);
	}]);
/* global document, angular, window */

var mentorProfileApp = angular.module('mentorProfileApp'); 
mentorProfileApp.controller('ProfileController', function($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService) {
    angular.element(document).ready(function () {
        var mentorId = $scope.profile.mentorId;
        profileDataService.getMentorProfile($scope.profile.mentorId, function(data) {
            $scope.profile = data;
            $scope.regions = profileRegionService.buildRegionList(data);
            $scope.availabilityProcessed = profileAvailabilityService.buildAvailabilityList(data);
            $scope.rolesProcessed = profileRoleService.buildRoleList(data);
            $scope.heroesProcessed = profileHeroService.buildHeroList(data);
            $scope.statistics = profileStatisticsService.buildStatisticsList(data);
        });
        $scope.profilePictureUri = '/data/mentor/' + $scope.profile.mentorId + "/profilePicture";
        $scope.contact = function() {
            window.location = '/mentor/' + mentorId + "/contact";
        };
    });
});

/* global document, angular */

var mentorProfileApp = angular.module('mentorProfileApp');
mentorProfileApp.directive('valueAsPercent', function() {
    return {
        restrict: 'AE',
        replace: 'true',
        template: '<a>{{valueAsPercent}}</a>',
        link: function(scope, element, attrs, ngModel) {
            scope.$watch(attrs.valueAsPercent, function(newValue) {
                if(scope.profile && scope.profile.data && scope.profile.data.response_rate) {
                    var ofHundred = scope.profile.data.response_rate * 100;
                    scope.valueAsPercent = ofHundred.toFixed(1) + "%";
                }
            });
        }
    };
});

mentorProfileApp.directive('responseTimeAsText', function() {
    return {
        restrict: 'AE',
        replace: 'true',
        template: '<a>{{responseTimeAsText}}</a>',
        link: function(scope, element, attrs, ngModel) {
            scope.$watch(attrs.responseTimeAsText, function(newValue) {
                if(scope.profile && scope.profile.data && scope.profile.data.response_time) {
                    var value = scope.profile.data.response_time;
                    var text = "More than one day";
                    if(value < 7) {
                        text = value + " days";
                    }
                    if(value < 1) {
                        text = "Less than a day";
                    }
                    if(value === 7) {
                        text = "One week";
                    }
                    if(value > 7) {
                        text = "More than a week";
                    }
                    scope.responseTimeAsText = text;
                }
            });
        }
    };
});
/* global document, angular */

var mentorProfileApp = angular.module('mentorProfileApp'); 
mentorProfileApp.filter('percentAsString', function() {
	return function(input) {
		return Math.round(input * 100, 0) + "%";
	};
});

/* global angular */

var mentorProfileApp = angular.module('mentorProfileApp'); 
mentorProfileApp.factory('profileDataService', function($http) {
    return {
        getMentorProfile: function(mentorId, callable) {
            return $http({
                url: '/api/mentor/' + mentorId,
                method: 'GET',
                params: {}
            })
            .then(function(result) {
                callable(result.data);
            });
        }
    };
});

mentorProfileApp.factory('profileRegionService', function(profileLabelService) {
    return {
        buildRegionList: function(data) {
            var rawRegionList = this._buildRawRegionList(data);
            return this._orderRegionList(rawRegionList);
        },
        _buildRawRegionList: function(data) {
            if(!data.regions) {
                return [];
            }
            var regions = [];
            angular.forEach(data.regions, function(value, key) {
                if(value === true) {
                    regions.push({
                        label: profileLabelService.getNameForLabel('regions', key),
                        identifier: key
                    });
                }
            });
            return regions;
        },
        _orderRegionList: function(rawRegionList) {
            var labelOrder = profileLabelService.getLabelOrder('regions');
            var orderedRegionList = [];
            angular.forEach(labelOrder, function(label) {
                angular.forEach(rawRegionList, function(entry) {
                    if(entry.identifier === label) {
                        orderedRegionList.push(entry);
                    }
                });
            });
            return orderedRegionList;
        }
    };
});

mentorProfileApp.factory('profileAvailabilityService', function(profileLabelService) {
    return {
        buildAvailabilityList: function(data) {
            var availabilityList = [];
            availabilityList = availabilityList.concat(this._buildDayList(data));
            availabilityList = availabilityList.concat(this._buildTimeList(data));
            return availabilityList;
        },
        _buildDayList: function(data) {
            if(!data.availability) {
                return [];
            }
            var day = [];
            if(data.availability["Any day"] === true) {
                day = [{label: 'Any day', identifier: 'anyday'}];
            }
             if(data.availability["Weekends only"] === true) {
                day = [{label: 'Weekends only', identifier: 'weekends'}];
            }
            return day;
        },
        _buildTimeList: function(data) {
            if(!data.availability) {
                return [];
            }
            var time = [];
            if(data.availability["Any time"] === true) {
                time = [{label: 'Any time', identifier: 'anytime'}];
            }
             if(data.availability["Evenings only"] === true) {
                time = [{label: 'Evenings only', identifier: 'evenings'}];
            }
            return time;
        }
    };
});

mentorProfileApp.factory('profileRoleService', function(profileLabelService) {
    var numberOfColumns = 2;
    return {
        buildRoleList: function(data) {
            if(!data.roles) {
                return [];
            }
            var rawList = this._buildRawList(data);
            var roles = this._divideRawListIntoColumns(rawList, numberOfColumns);
            return roles;
        },
        _buildRawList: function(data) {
            var me = this;
            var roles = [];
            angular.forEach(data.roles, function(value, key) {
                if(value === true) {
                    roles.push({
                        label: me._getLabel(key),
                        identifier: key
                    });
                }
            });
            return roles;
        },
        _divideRawListIntoColumns: function(rawList, numberOfColumns) {
            var itemsByColumn = Math.ceil(rawList.length/numberOfColumns);
            var columns = [];
            for(var i = 0, total = numberOfColumns; i < total; i++) {
                var start = i * itemsByColumn;
                var end = (i + 1) * itemsByColumn;
                columns.push(rawList.slice(start, end));
            }
            return columns;
        },
        _getLabel: function(key) {
            var label = profileLabelService.getNameForLabel('roles', key);
            return label.charAt(0).toUpperCase() + label.slice(1);
        }
    };
});

mentorProfileApp.factory('profileHeroService', function() {
    return {
        buildHeroList: function(data) {
            if(!data || !data.data || !data.data.top_heroes) {
                return [];
            }
            var me = this;
            var heroList = [];
            angular.forEach(data.data.top_heroes, function(hero) {
                heroList.push({
                    identifier: hero,
                    label: me._buildLabel(hero)
                });
            });
            return heroList;
        },
        _buildLabel: function(hero) {
            return hero;
        }
    };
});

mentorProfileApp.factory('profileStatisticsService', function($filter, profileLabelService) {
    return {
        buildStatisticsList: function(data) {
            if(!data || !data.data || !data.data.statistics) {
                return [];
            }
            var me = this;
            var statistics = [];
            var parsedStatistics = this._parseStatistics(data.data.statistics);
            angular.forEach(parsedStatistics, function(value, key) {
                statistics.push({
                    identifier: key,
                    label: profileLabelService.getNameForLabel('statistics', key),
                    value: me._processValue(key, value)
                });
            });
            return statistics;
        },
        _processValue: function(key, value) {
            if(key === "win_rate") {
                return $filter('percentAsString')(value);
            }
            return $filter('number')(value, 0);
        },
        _parseStatistics: function(statisticsString) {
            return angular.fromJson(statisticsString);
        }
    };
});
/* global angular */

var mentorProfileApp = angular.module('mentorProfileApp'); 
mentorProfileApp.factory('profileLabelService', function() {
  return {
    labels: {
      regions: {
        'useast': 'US East',
        'uswest': 'US West',
        'eueast': 'EU East',
        'euwest': 'EU West',
        'seasia': 'SE Asia',
        'russia': 'Russia',
        'southamerica': 'South America',
        'australia': 'Australia'
      },
      roles: {
        'carry': 'carry',
        'disabler': 'disabler',
        'ganker': 'ganker',
        'initiator': 'initiator',
        'jungler': 'jungler',
        'offlaner': 'offlaner',
        'pusher': 'pusher',
        'support': 'support'
      },
      statistics: {
        'games_played': 'games played',
        'win_rate': 'win rate',
        'solo_mmr': 'solo MMR'
      }
    },
    labelOrder: {
      regions: ['useast', 'uswest', 'eueast', 'euwest', 'seasia', 'russia', 'southamerica', 'australia'],
      statistics: ['games_played', 'win_rate', 'solo_mmr']
    },
    getLabelForName: function(category, name) {
      var label;
      angular.forEach(this.labels[category], function(value, key) {
        if(value === name) {
          label = key;
        }
      });
      return label;
    },
    getNameForLabel: function(category, label) {
      return this.labels[category][label];
    },
    getLabelOrder: function(category) {
      return this.labelOrder[category];
    }
  };
});