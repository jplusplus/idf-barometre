
# Services
angular
    .module('barometreServices', ['ngResource'])
    .factory 'Answer', ($resource)->   
        $resource './answers.json', {}, {query:{method:'GET', isArray:true}}
    .factory 'Introduction', ($resource)->   
        $resource './introductions.json', {}, {query:{method:'GET', isArray:true}}
    .factory 'ArrowColor', ->
        question: 'economique'
        active  : false


    
