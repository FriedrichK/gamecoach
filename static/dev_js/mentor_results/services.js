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

app.factory('generateUrlService', function() {
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

app.factory('mentorSettingsService', function() {
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