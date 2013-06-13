angular
    .module('barometreFilters', [])
    .filter('alias', -> 
        return (key)->            
            aliases =
                "all"           : "les <strong>franciliens</strong>"
                "femme"         : "les <strong>femmes</strong>"
                "homme"         : "les <strong>hommes</strong>"
                "18_24"         : "les <strong>18-24 ans</strong>"
                "25_34"         : "les <strong>25-34 ans</strong>"
                "35_49"         : "les <strong>35-49 ans</strong>"
                "50_64"         : "les <strong>50-64 ans</strong>"
                "65_plus"       : "les <strong>65 ans et plus</strong>"
                "cadre"         : "les <strong>cadres</strong>"
                "employe"       : "les <strong>employés</strong>"
                "ouvrier"       : "les <strong>ouvriers</strong>"
                "technicien"    : "les <strong>techniciens</strong>"
                "retraite"      : "les <strong>retraités</strong>"
                "economique"    : "de la <strong>situation économique</strong>"
                "transport"     : "des <strong>transports en commun</strong>"
                "environnement" : "de la <strong>situation économique</strong>"
            return aliases[key]
    )
    .filter('colors', ->
        return (key, level='default')->
            colors =
                "economique":
                    "default" : "#EA9806"
                    "0"       : "#ED9B0B"
                    "50"      : "#F2B84D"
                    "51"      : "#EA9806"
                    "100"     : "#B3750E"
                "transport":
                    "default" : "#06c3d6"
                    "0"       : "#08c5d8"
                    "50"      : "#4dd5e3"
                    "51"      : "#06c3d6"
                    "100"     : "#1096a2"
                "environnement":
                    "default" : "#bad808"
                    "0"       : "#bbd80a"
                    "50"      : "#cfe252"
                    "51"      : "#bad808"
                    "100"     : "#8fa310"
            return colors[key][level]         
    )