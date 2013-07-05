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
                "environnement" : "de <strong>la qualité de l'environnement</strong>"
                "75"            : "les <strong>habitants du 75</strong>"
                "77"            : "les <strong>habitants du 77</strong>"
                "78"            : "les <strong>habitants du 78</strong>"
                "91"            : "les <strong>habitants du 91</strong>"
                "92"            : "les <strong>habitants du 92</strong>"
                "93"            : "les <strong>habitants du 93</strong>"
                "94"            : "les <strong>habitants du 94</strong>"
                "95"            : "les <strong>habitants du 95</strong>"
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
                    "default" : "#07C5D8"
                    "0"       : "#08c5d8"
                    "50"      : "#4dd5e3"
                    "51"      : "#07C5D8"
                    "100"     : "#1096a2"
                "environnement":
                    "default" : "#bad808"
                    "0"       : "#bbd80a"
                    "50"      : "#cfe252"
                    "51"      : "#bad808"
                    "100"     : "#8fa310"
            return colors[key][level]         
    )
    .filter("supPercent", ->
        return (val='', html=true, format=null)-> 
            # Remove ,0% end
            val = val.replace /,0(%|pt)/, "$1"
            # Add <sup></sup> arround %
            val = val.replace /(%|pt)/, "<sup>$1</sup>" if html           

            if format == "trend"
                if html
                    # Add a plus prefix for percentage and non-negative values
                    val = "<sub>+</sub>" + val if val.indexOf("-") == -1                 
                    # Relplace the classic minus by a special chart
                    val = val.replace("-", "<sub>-</sub>")
                else
                    val = "+" + val if val.indexOf("-") == -1
            # Return the new value explcitily
            return val
    )
    .filter("nl2br", ->
        return (str='')-> (str + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1<br />$2')
    )