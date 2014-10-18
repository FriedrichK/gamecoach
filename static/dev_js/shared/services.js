/* global document, angular, $ */

var gamecoachShared = angular.module('gamecoachShared'); 
gamecoachShared.factory('usernameValidationService', function($http) {
    return {
        validate: function(url, params) {
            return $http({method: 'GET', url: url, params: params});
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

gamecoachShared.factory('notificationService', function() {
    var getErrorNotificationElement = function() {
        return angular.element('.errornotification');
    };
    var getErrorTextElement = function() {
        return getErrorNotificationElement().find('.errortext');
    };
    var changeMessage = function(message) {
        getErrorTextElement().html(message);
    };
    var showNotification = function() {
        getErrorNotificationElement().removeClass('ng-hide');
    };
    return {
        notifyError: function(message) {
            changeMessage(message);
            showNotification();
        },
        hide: function() {
            getErrorNotificationElement().addClass('ng-hide');
        }
    };
});

gamecoachShared.factory('fileTypeService', function() {
    return {
        isFileTypeFromOptions: function(fileType, fileTypes) {
            var valid = false;
            angular.forEach(fileTypes, function(mimeArray, label) {
                if(mimeArray.indexOf(fileType) > -1) {
                    valid = true;
                }
            });
            return valid;
        },
        getAcceptedFileTypeString: function(fileTypes) {
            var labels = [];
            angular.forEach(fileTypes, function(mimeArray, label) {
                labels.push(label);
            });
            return labels.join(', ');
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