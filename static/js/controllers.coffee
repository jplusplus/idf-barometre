
QuestionListCtrl = ($scope, $http, $rootElement )->
    $http.get('/static/questions.json').success (data)-> 
        $scope.questions = data

QuestionListCtrl.$inject = ['$scope', '$http', '$rootElement'];


AnswerGraphCtrl = ($scope, $http, $rootElement, $routeParams, $location, $filter)->
    # Models attributes
    $scope.question = $routeParams.question or "economique"
    $scope.sample   = $routeParams.sample   or "all"
    # Watch for model change to update the graph
    $scope.$watch 'sample',   ->update()
    $scope.$watch 'question', ->update()

    # Graph attributes
    svg        = {}    
    parse      = d3.time.format("%d/%m/%Y").parse
    dateFormat = d3.time.format("%b %y")
    # Wrapper that container the graph and a scrollbar
    wrapper = $rootElement.find(".wrapper")
    chart   = $rootElement.find(".chart")
    wrapperWidth = wrapper.innerWidth()
    wrapperHeight = wrapper.innerHeight() - 20
    # Add customise scrollbar
    wrapper.jScrollPane hideFocus: true

    # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
    x = d3.time.scale()
    y = d3.scale.linear()
    insertLinebreaks = (d) ->
      el = d3.select(this)
      words = dateFormat(d).split(" ")
      el.text ""
      i = 0

      while i < words.length
        tspan = el.append("tspan").text(words[i])
        tspan.attr("x", 0).attr "dy", "18"  if i > 0
        i++

    # Methods
    update = -> $http.get('/static/answers.json').success render
    render = (values)-> 
        chart.empty()
        # Filter to one symbol; the S&P 500.
        values = _.filter(values, (d)-> 
            d.question.toLowerCase() == $scope.question && d.profil.toLowerCase() == $scope.sample
        )       
        # Do we stop
        return if values.length == 0
        # Parse dates and numbers. We assume values are sorted by date.
        _.each values, (d) ->
            d.date  = parse(d.date)                      
            d.ratio = parseFloat(d.ratio)
        # Sort by date
        values = _.sortBy(values, (d)-> d.date) 

        p         = [0, 0, 60, 0]
        minGap    = if $("html").hasClass("lt-ie9") then 80 else 40
        dotGap    = Math.max(minGap, wrapperWidth / (values.length - 1))
        w         = (dotGap * (values.length - 1)) - p[1] - p[3]
        h         = wrapperHeight - p[0] - p[2]        
        gradientW = (w / (values.length - 1)) * 2    


        # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
        x.range [0, w]
        y.range [h, 0]
        xAxis = d3.svg.axis().scale(x).tickSize(1).tickPadding(10).tickFormat(dateFormat).ticks(d3.time.months, 2)
        yAxis = d3.svg.axis().scale(y).tickSize(1).orient("right")

        # An area generator, for the light fill.
        area = d3.svg.area()
            .interpolate("linear")
            .x((d) -> x(d.date))
            .y0(h)
            .y1((d)-> y(d.ratio))

        # A line generator, for the dark stroke.
        line = d3.svg.line()
            .interpolate("linear")
            .x( (d) -> x(d.date))
            .y( (d) -> y(d.ratio))


        # Compute the minimum and maximum date, and the maximum price.
        minDate  = d3.min values, (d)-> d.date
        maxDate  = d3.max values, (d)-> d.date        
        minValue = d3.min values, (d)-> d.ratio
        maxValue = d3.max values, (d)-> d.ratio        
        offset   = (maxValue - minValue) * 0.3
        x.domain([minDate, maxDate])
        y.domain([minValue - offset, maxValue + offset]).nice()

        chart.css("width",  w + p[1] + p[3])
        # Add an SVG element with the desired dimensions and margin.
        svg = d3.select( chart[0] )
                .append("svg:svg")
                    .attr("width",  w + p[1] + p[3])
                    .attr("height", h + p[0] + p[2])
                    .append("g")
                        .attr("transform", "translate(" + p[3] + "," + p[0] + ")")
        
        unless Modernizr.svg         
            # Add the area path.
            svg
                .append("svg:path")
                    .attr("class", "area bg")
                    .attr("fill", "#ee9807")
                    .attr("d", area(values))
        # Add stripes
        else            
            svg
                .append("linearGradient")
                    .attr("id", "sequence-gradient")
                    .attr("gradientUnits", "userSpaceOnUse")
                    .attr("spreadMethod", "repeat")
                    .attr("y1", 0)
                    .attr("x1", 0)
                    .attr("y2", 0)
                    .attr("x2", gradientW)
                    .selectAll("stop")
                        .data([                            
                            { offset: "0%",   color: $filter("colors")($scope.question, "0") }
                            { offset: "50%",  color: $filter("colors")($scope.question, "50") }
                            { offset: "51%",  color: $filter("colors")($scope.question, "51") }
                            { offset: "100%", color: $filter("colors")($scope.question, "100") }
                        ])
                        .enter()
                        .append("stop")
                            .attr("offset",     (d)-> d.offset)
                            .attr("stop-color", (d)-> d.color)
            # Add the area path.
            svg.append("svg:path")
                .attr("class", "area bg")
                .attr("fill", "url(#sequence-gradient)")
                .attr("d", area(values))

        # Add line dots
        svg.selectAll(".data-point")
            .data(values)
            .enter()
            .append("svg:circle")
                .attr("class", "data-point")
                .attr("cx", (d)-> x d.date)
                .attr("cy", (d)-> y d.ratio)
                .attr("fill", $filter("colors")($scope.question))
                .attr("stroke-width", 3)
                .attr("stroke", "#ffffff")
                .attr("r", 5)
                # .on("mousemove", createPointTips)
                # .on("mouseleave", closePointTips)
                # .on "click", togglePoint

        # Add the x-axis.
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + (h + 15) + ")")
            .call xAxis
        # Add axis break line
        svg.selectAll(".x.axis g text").each insertLinebreaks
        svg.selectAll(".x.axis g text").attr "font-size", 16

        # Reinitialize jscrollpane
        wrapper.data("jsp").reinitialise()

    update()
            

AnswerGraphCtrl.$inject = ['$scope', '$http', '$rootElement', '$routeParams', '$location', '$filter'];
