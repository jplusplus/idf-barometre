
# Services
angular
    .module('barometreServices', ['ngResource'])
    .factory 'Answer', ($resource)->   
        $resource '/answers.json', {}, {query:{method:'GET', isArray:true}}
    
