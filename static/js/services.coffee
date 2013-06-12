
# Services
angular
    .module('barometreServices', ['ngResource'])
    .factory 'Question', ($resource)->
        $resource '/static/questions.json', {}, {query:{method:'GET'}, isArray:true}
    
