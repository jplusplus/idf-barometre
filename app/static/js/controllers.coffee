
QuestionListCtrl = ($scope, Introduction, $rootElement )->    
    $scope.introductions = Introduction.query()

QuestionListCtrl.$inject = ['$scope', 'Introduction', '$rootElement'];


AnswerGraphCtrl = ($scope, Answer, $rootElement, $routeParams, $location, $filter)->
    # Models attributes
    $scope.question = $routeParams.question or "economique"
    $scope.sample   = $routeParams.sample   or "all"
    # Watch for model change to update the graph
    $scope.$watch 'sample',   ->update()
    $scope.$watch 'question', ->update()

    # Graph attributes
    svg        = {}    
    parse      = d3.time.format("%m/%Y").parse
    dateFormat = d3.time.format("%b %y")
    # Wrapper that container the graph and a scrollbar
    wrapper = $rootElement.find(".wrapper")
    chart   = $rootElement.find(".chart")
    # Saves wrap
    wrapperWidth  = wrapper.innerWidth()
    wrapperHeight = wrapper.innerHeight() - 20
    # Add customise scrollbar
    wrapper.jScrollPane hideFocus: true

    # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
    x = d3.time.scale()
    y = d3.scale.linear()

    # Methods
    update = -> 
        params = profil: $scope.sample, question: $scope.question
        $scope.answers = Answer.query params, render

    mouse = (ev) ->
        ev = ev or event
        x: event.clientX + (document.documentElement.scrollLeft or document.body.scrollLeft)
        y: event.clientY + (document.documentElement.scrollTop or document.body.scrollTop)

    createPointTips = (d, index) ->
        $tips = $(".point-tips[data-point=" + index + "]")
        $point = $(svg.selectAll(".data-point")[0][index])      
        # tips doenst exist yet
        if $tips.length is 0        
            # Create the tips
            $tips = $("<div class='point-tips hidden' data-point='" + index + "' />")        
            # Positionate the tips to under the mouse
            $tips.css
                left: (if $point.offset() then $point.offset().left else mouse().x)
                top: (if $point.offset() then $point.offset().top else mouse().y)
            # Appends the tips to the bodu
            $tips.appendTo "body"      
        # tips exists
        else        
            # Positionate the tips to under the mouse
            $tips.css(
                left: (if $point.offset() then $point.offset().left else mouse().x)
                top: (if $point.offset() then $point.offset().top else mouse().y)
            ).removeClass "hidden"
      
        # In any case, change the content of the tip
        $tips.html "<div class='content'>" + ~~d.ratio + "%</div>"

    closePointTips = (d, index) ->
        $point = $(svg.selectAll(".data-point")[0][index])    
        # Do not close active point      
        # Just add a class hidden to the right tips
        $(".point-tips[data-point=" + index + "]").addClass "hidden"  unless $point.hasClass("active")

    insertLinebreaks = (d) ->
        el = d3.select(this)
        words = dateFormat(d).split(" ")
        el.text ""
        i = 0

        while i < words.length
            tspan = el.append("tspan").text(words[i])
            tspan.attr("x", 0).attr "dy", "18"  if i > 0
            i++

    render = ()-> 
        chart.empty()   
        # Do we stop
        return if $scope.answers.length == 0
        # Parse dates and numbers. We assume $scope.answers is sorted by date.
        _.each $scope.answers, (d) ->
            try 
                return d.date = parse(d.date)  
            # Some parsings fail          
            catch error
                return null

        p         = [0, 15, 60, 15]
        minGap    = if $("html").hasClass("lt-ie9") then 80 else 40
        dotGap    = Math.max(minGap, wrapperWidth / ($scope.answers.length - 1))
        w         = (dotGap * ($scope.answers.length - 1)) - p[1] - p[3]
        h         = wrapperHeight - p[0] - p[2]        
        gradientW = (w / ($scope.answers.length - 1)) * 2    


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
        minDate  = d3.min $scope.answers, (d)-> d.date
        maxDate  = d3.max $scope.answers, (d)-> d.date        
        minValue = d3.min $scope.answers, (d)-> d.ratio
        maxValue = d3.max $scope.answers, (d)-> d.ratio        
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
                    .attr("d", area($scope.answers))
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
                .attr("d", area($scope.answers))

        # Add line dots
        svg.selectAll(".data-point")
            .data($scope.answers)
            .enter()
            .append("svg:circle")
                .attr("class", "data-point")
                .attr("cx", (d)-> x d.date)
                .attr("cy", (d)-> y d.ratio)
                .attr("fill", $filter("colors")($scope.question))
                .attr("stroke-width", 3)
                .attr("stroke", "#ffffff")
                .attr("r", 5)
                .on("mousemove", createPointTips)
                .on("mouseleave", closePointTips)
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
            

AnswerGraphCtrl.$inject = ['$scope', 'Answer', '$rootElement', '$routeParams', '$location', '$filter'];
