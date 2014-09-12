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
      },
      mentoring: {
        'individual': 'individual mentoring',
        'team': 'team mentoring',
        'spectating': 'mentoring while spectating',
        'together': 'mentoring while playing together',
        'analysing': 'analysing replies',
        'questions': 'general questions & answers',
        'voicechat': 'voice chat',
        'textchat': 'text chat'
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