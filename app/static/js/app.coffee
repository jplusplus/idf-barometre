angular
    .module('barometre', ['barometreFilters', 'barometreServices', 'ngSanitize', 'ui.bootstrap'])
    .config(
        [
            '$interpolateProvider', 
            '$routeProvider',              
            ($interpolateProvider, $routeProvider)->    
                # Avoid a conflict with Django Template's tags
                $interpolateProvider.startSymbol '[['
                $interpolateProvider.endSymbol   ']]'

                # Bind routes to the controllers
                $routeProvider
                    .when('/', {controller: QuestionListCtrl, templateUrl: "/partial/questionList.html?#{Date()}"})
                    .when('/answers/', {
                        controller: AnswerGraphCtrl,  
                        templateUrl: "/partial/answerGraph.html",
                        reloadOnSearch: false
                    })
                    .otherwise redirectTo: '/'


        ]
    #you can inject stuff!
    ).animation("explode-enter", ()->
        setup: (element) ->        
            # Random number between -1000 and 1000
            distX = ~~(500+Math.random()*1000)-1000 + "px"  
            distY = ~~(500+Math.random()*1000)-1000 + "px"
            # this is called before the animation
            element.css 
                "opacity": 0
                "transform": "translate(#{distX}, #{distY})"
        start: (element, done) ->        
            #this is where the animation is expected to be run
            element.animate
                "opacity": 1
                "transform": 'translate(0, 0)'
            , 800
            #call done to close when the animation is complete
            , -> done()                          
        # This is called when another animation is started
        # whilst the previous animation is still chugging away                
        cancel: (element, done) ->
    )
