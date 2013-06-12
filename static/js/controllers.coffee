
QuestionListCtrl = ($scope, $http, $rootElement )->
    $http.get('/static/questions.json').success (data)-> 
        $scope.questions = data

QuestionListCtrl.$inject = ['$scope', '$http', '$rootElement'];


AnswerGraphCtrl = ($scope, $http, $rootElement)->
    $http.get('/static/answers.json').success (data)-> 
        $scope.answers = data

AnswerGraphCtrl.$inject = ['$scope', '$http', '$rootElement'];
