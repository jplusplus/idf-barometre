// Generated by CoffeeScript 1.6.2
angular.module('barometreFilters', []).filter('alias', function() {
  return function(key) {
    var aliases;

    aliases = {
      "all": "les <strong>franciliens</strong>",
      "femme": "les <strong>femmes</strong>",
      "homme": "les <strong>hommes</strong>",
      "18_24": "les <strong>18-24 ans</strong>",
      "25_34": "les <strong>25-34 ans</strong>",
      "35_49": "les <strong>35-49 ans</strong>",
      "50_64": "les <strong>50-64 ans</strong>",
      "65_plus": "les <strong>65 ans et plus</strong>",
      "cadre": "les <strong>cadres</strong>",
      "employe": "les <strong>employés</strong>",
      "ouvrier": "les <strong>ouvriers</strong>",
      "technicien": "les <strong>techniciens</strong>",
      "retraite": "les <strong>retraités</strong>",
      "economique": "de la <strong>situation économique</strong>",
      "transport": "des <strong>transports en commun</strong>",
      "environnement": "de la <strong>situation économique</strong>"
    };
    return aliases[key];
  };
});
