
# Services
angular
    .module('barometreServices', ['ngResource'])
    .factory 'Answer', ($resource)->   
        $resource './reponses.json', {}, {
        	query: {
        		method:'GET', 
        		isArray:false
        	}
       	}
    .factory 'Introduction', ($resource)->   
        $resource './introductions.json', {}, {
        	query: {
        		method:'GET',
        		isArray:true
        	}
       	}
    .factory 'ArrowColor', ->
        question: 'economique'
        active  : false


    
