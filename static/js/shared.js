/* global angular */
var gamecoachShared = angular.module('gamecoachShared', []);
/* Source: https://github.com/webadvanced/ng-remote-validate */
/* global document, angular */
/*jshint evil:false */

var gamecoachShared = angular.module('gamecoachShared');
gamecoachShared.directive('gcRemoteValidate', function(usernameValidationService) {
    var directiveId = "gcRemoteValidate";
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function(scope, el, attrs, ngModel) {
            el.bind("keydown", function (event) {
                console.log("keydown");
                var validationPromise = usernameValidationService.validate(attrs['value']);
                validationPromise.success = function(data, status, headers, config) {
                    console.log("ALRIGHT!", data, status, headers, config);
                };
                validationPromise.error = function(data, status, headers, config) {
                    console.log("FAIL!", data, status, headers, config);
                };
            });
        }
    };
});

/*gamecoachShared.directive('ngRemoteValidate', function() {
    return {
        remoteValidate: function( $http, $timeout, $q ) {
            var directiveId = "ngRemoteValidate";
            return {
                restrict: 'A',
                require: 'ngModel',
                link: function( scope, el, attrs, ngModel ) {
                    var cache = {},
                        handleChange,
                        setValidation,
                        addToCache,
                        request,
                        shouldProcess,
                        options = {
                            ngRemoteThrottle: 400,
                            ngRemoteMethod: 'POST'
                        };

                    angular.extend( options, attrs );

                    options.urls = [ options.ngRemoteValidate ];

                    addToCache = function( response ) {
                        var value = response[ 0 ].data.value;
                        if (cache[value]) {
                            return cache[value];
                        }
                        cache[ value ] = response;
                    };

                    shouldProcess = function( value ) {
                        var otherRulesInValid = false;
                        for ( var p in ngModel.$error ) {
                            if ( ngModel.$error[ p ] && p !== directiveId ) {
                                otherRulesInValid = true;
                                break;
                            }
                        }
                        return !( ngModel.$pristine || otherRulesInValid );
                    };

                    setValidation = function( response, skipCache ) {
                        var i = 0,
                            l = response.length,
                            isValid = true;
                        for( ; i < l; i++ ) {
                            if( !response[ i ].data.isValid ) {
                                isValid = false;
                                break;
                            }
                        }
                        if( !skipCache ) {
                            addToCache( response );    
                        }
                        ngModel.$setValidity( directiveId, isValid );
                        el.removeClass( 'ng-processing' );
                        ngModel.$processing = false;
                    };

                    handleChange = function( value ) {
                        if(typeof value === 'undefined') {
                            return;
                        }

                        if ( !shouldProcess( value ) ) {
                            return setValidation( [ { data: { isValid: true, value: value } } ], true );
                        }

                        if ( cache[ value ] ) {
                            return setValidation( cache[ value ], true );
                        }

                        if ( request ) {
                            $timeout.cancel( request );
                        }

                        request = $timeout( function( ) {
                            el.addClass( 'ng-processing' );
                            ngModel.$processing = true;
                            var calls = [],
                                i = 0,
                                l = options.urls.length,
                                toValidate = { value: value },
                                httpOpts = { method: options.ngRemoteMethod };
                            
                            if ( scope[ el[0].name + 'SetArgs' ] ) {
                                toValidate = scope[el[0].name + 'SetArgs'](value, el, attrs, ngModel);
                            }

                            if(options.ngRemoteMethod === 'POST'){
                                httpOpts.data = toValidate;
                            } else {
                                httpOpts.params = toValidate;
                            }

                            for( ; i < l; i++ ) {
                                httpOpts.url =  options.urls[ i ];
                                calls.push( $http( httpOpts ) );
                            }

                            $q.all( calls ).then( setValidation );
                            
                        }, options.ngRemoteThrottle );
                        return true;
                    };

                    scope.$watch( function( ) {
                        return ngModel.$viewValue;
                    }, handleChange );
                }
            };
        }
    };
});*/
/* global document, angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.filter('capitalize', function() {
	return function(input, scope) {
		if (input != null) {
			return input.substring(0,1).toUpperCase() + input.substring(1);
		}
	};
});

gamecoachShared.filter('percentAsString', function() {
	return function(input, precision) {
		if(!input || input === '' || isNaN(input)) {
			return null;
		}

		if(!precision) {
			precision = 0;
		}
		return (parseFloat(input)*100).toFixed(precision) + "%";
	};
});

/* global document, angular, window */

function BaseProfileController($scope, $element, profileDataService, profileRegionService, profileAvailabilityService, profileRoleService, profileHeroService, profileStatisticsService, mentorId) {
    angular.element(document).ready(function () {
        profileDataService.getMentorProfile(mentorId, function(data) {
            $scope.profile = data;
            $scope.regions = profileRegionService.buildRegionList(data);
            $scope.availabilityProcessed = profileAvailabilityService.buildAvailabilityList(data);
            $scope.rolesProcessed = profileRoleService.buildRoleList(data);
            $scope.heroesProcessed = profileHeroService.buildHeroList(data);
            $scope.statistics = profileStatisticsService.buildStatisticsList(data);
        });
        $scope.profilePictureUri = '/data/mentor/' + mentorId + "/profilePicture";
    });
}

/* global angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('profileDataService', function($http) {
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

gamecoachShared.factory('profileRegionService', function(profileLabelService) {
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

gamecoachShared.factory('profileAvailabilityService', function(profileLabelService) {
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

gamecoachShared.factory('profileRoleService', function(profileLabelService) {
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

gamecoachShared.factory('profileHeroService', function() {
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

gamecoachShared.factory('profileStatisticsService', function($filter, profileLabelService) {
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

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('profileLabelService', function() {
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
/* global document, angular, $ */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('usernameValidationService', function($http) {
    return {
        validate: function(username) {
            return $http({method: 'GET', url: '/someUrl', params: {username: username}});
        }
    };
});

gamecoachShared.factory('gCStringService', function() {
    return {
        decodeHtml: function(stringInput) {
            return $('<div/>').html(stringInput).text(); 
        }
    };
});

gamecoachShared.factory('heroesService', function() {
  return {
    getHeroHash: function() {
      return {
        "abaddon": "Abaddon",
        "alchemist": "Alchemist",
        "ancient_apparition": "Ancient Apparition",
        "anti-mage": "Anti-Mage",
        "arc_warden": "Arc Warden",
        "axe": "Axe",
        "bane": "Bane",
        "batrider": "Batrider",
        "beastmaster": "Beastmaster",
        "bloodseeker": "Bloodseeker",
        "bounty_hunter": "Bounty Hunter",
        "brewmaster": "Brewmaster",
        "bristleback": "Bristleback",
        "broodmother": "Broodmother",
        "centaur_warrunner": "Centaur Warrunner",
        "chaos_knight": "Chaos Knight",
        "chen": "Chen",
        "clinkz": "Clinkz",
        "clockwerk": "Clockwerk",
        "crystal_maiden": "Crystal Maiden",
        "dark_seer": "Dark Seer",
        "dazzle": "Dazzle",
        "death_prophet": "Death Prophet",
        "disruptor": "Disruptor",
        "doom_bringer": "Doom Bringer",
        "dragon_knight": "Dragon Knight",
        "drow_ranger": "Drow Ranger",
        "earth_spirit": "Earth Spirit",
        "earthshaker": "Earthshaker",
        "elder_titan": "Elder Titan",
        "ember_spirit": "Ember Spirit",
        "enchantress": "Enchantress",
        "enigma": "Enigma",
        "faceless_void": "Faceless Void",
        "goblin_techies": "Goblin Techies",
        "gyrocopter": "Gyrocopter",
        "huskar": "Huskar",
        "invoker": "Invoker",
        "io": "Io",
        "jakiro": "Jakiro",
        "juggernaut": "Juggernaut",
        "keeper_of_the_light": "Keeper of the Light",
        "kunkka": "Kunkka",
        "legion_commander": "Legion Commander",
        "leshrac": "Leshrac",
        "lich": "Lich",
        "lifestealer": "Lifestealer",
        "lina": "Lina",
        "lion": "Lion",
        "lone_druid": "Lone Druid",
        "luna": "Luna",
        "lycanthrope": "Lycanthrope",
        "magnus": "Magnus",
        "medusa": "Medusa",
        "meepo": "Meepo",
        "mirana": "Mirana",
        "morphling": "Morphling",
        "naga_siren": "Naga Siren",
        "nature's_prophet": "Nature's Prophet",
        "necrophos": "Necrophos",
        "night_stalker": "Night Stalker",
        "nyx_assassin": "Nyx Assassin",
        "ogre_magi": "Ogre Magi",
        "omniknight": "Omniknight",
        "oracle": "Oracle",
        "outworld_devourer": "Outworld Devourer",
        "phantom_assassin": "Phantom Assassin",
        "phantom_lancer": "Phantom Lancer",
        "phoenix": "Phoenix",
        "pit_lord": "Pit Lord",
        "puck": "Puck",
        "pudge": "Pudge",
        "pugna": "Pugna",
        "queen_of_pain": "Queen of Pain",
        "razor": "Razor",
        "riki": "Riki",
        "rubick": "Rubick",
        "sand_king": "Sand King",
        "shadow_demon": "Shadow Demon",
        "shadow_fiend": "Shadow Fiend",
        "shadow_shaman": "Shadow Shaman",
        "silencer": "Silencer",
        "skywrath_mage": "Skywrath Mage",
        "slardar": "Slardar",
        "slark": "Slark",
        "sniper": "Sniper",
        "soul_keeper": "Soul Keeper",
        "spectre": "Spectre",
        "spirit_breaker": "Spirit Breaker",
        "storm_spirit": "Storm Spirit",
        "sven": "Sven",
        "templar_assassin": "Templar Assassin",
        "terrorblade": "Terrorblade",
        "tidehunter": "Tidehunter",
        "timbersaw": "Timbersaw",
        "tinker": "Tinker",
        "tiny": "Tiny",
        "treant_protector": "Treant Protector",
        "troll_warlord": "Troll Warlord",
        "tusk": "Tusk",
        "undying": "Undying",
        "ursa": "Ursa",
        "vengeful_spirit": "Vengeful Spirit",
        "venomancer": "Venomancer",
        "viper": "Viper",
        "visage": "Visage",
        "warlock": "Warlock",
        "weaver": "Weaver",
        "windranger": "Windranger",
        "winter_wyvern": "Winter Wyvern",
        "witch_doctor": "Witch Doctor",
        "wraith_king": "Wraith King",
        "zeus": "Zeus"
      };
    }
  };
});
/* global angular */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('timeService', function($filter) {
	return {
		getCurrentDate: function() {
			return new Date();
		},
		isToday: function(d) {
			var now = this.getCurrentDate();
			if(d.getYear() === now.getYear() && d.getMonth() === now.getMonth() && d.getDate() === now.getDate()) {
				return true;
			}
			return false;
		},
		formatMessageDate: function(message) {
			var date = this.convertJsonToDate(message.sent_at);
			var format = 'shortDate';
			if(this.isToday(date)) {
				format = 'shortTime';
			}
			message.sent_at = $filter('date')(date, format);
			return message;
		},
		convertJsonToDate: function(d) {
			return new Date(d.year, d.month - 1, d.day, d.hour, d.minute, d.second, 0);
		}
	};
});