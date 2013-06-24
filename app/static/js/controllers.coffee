
QuestionListCtrl = ($scope, Introduction, $rootElement )->    
    $scope.introductions = Introduction.query()

QuestionListCtrl.$inject = ['$scope', 'Introduction', '$rootElement'];


AnswerGraphCtrl = ($scope, Answer, $rootElement, $routeParams, $location, $filter)->


    # Models attributes
    $scope.question = $routeParams.question or "economique"
    $scope.sample   = $routeParams.sample   or "all"
    # List of active point
    $scope.activePoints = {}

    # Graph attributes
    chartSvg   = {}
    yAxisSvg   = {}    
    parse      = d3.time.format("%m/%Y").parse
    dateFormat = d3.time.format("%b %y")    
    # Empty shortcuts
    wrapper = chart = axis = $(null)        
    # Saves wrap
    wrapperWidth  = 549
    wrapperHeight = 330
    tickSize      = 5    
    padding       = [10, 10, 60, 10]
    minGap        = 40

    # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
    x = d3.time.scale()
    y = d3.scale.linear()
    
    update = -> 
        params = profil: $scope.sample, question: $scope.question
        $scope.answers = Answer.query params, render

    loadShortcuts = ->
        wrapper = $rootElement.find(".wrapper")
        chart   = $rootElement.find(".chart")
        axis    = $rootElement.find(".yaxis")

    closestActivePoints = (ref)->
        ref = parseInt(ref)
        # By default the closest key is a very big number
        closestDist = Math.pow(99,99)
        # Get all keys
        keys = _.keys($scope.activePoints)
        # Take the first key by default
        closest = keys[0] 
        # Look every key
        _.each keys, (k)->
            # Distance to the reference index
            dist = Math.abs(parseInt(k)-ref)
            # If the new distance is smaller
            if dist > 0 and dist < closestDist
                closestDist = dist
                # Take the key as closest key
                closest = k
            
        # Return the closest key
        return parseInt(closest)

    point =      
        offset: (d)-> 
            wrapper = $rootElement.find(".wrapper")
            return {
                top  :  wrapper.offset().top  + y(d.ratio)
                left :  wrapper.offset().left + x(d.date)
            }
        setTrend: (d)->
            # Wait for D3 instance
            if chartSvg.select?
                # find the trend group
                trend = chartSvg.select("g.trend")
                # Keys list sortted by key
                keys = _.sortBy _.keys($scope.activePoints), (d, key)->key
                # Only if there is enougth data
                unless keys.length < 2
                    fst = $scope.activePoints[ keys[0] ]
                    snd = $scope.activePoints[ keys[1] ]
                    # First and second values substracted to know the trend
                    val  = snd.ratio
                    val -= fst.ratio
                    # Set the value
                    trend.select("text").text( $filter("supPercent")(val+"%", false) )
                    # Set the color of the circle
                    trend.select("circle").transition()
                        .attr("fill", if val < 0 then "#cc0e00" else "#69cc00")
                    # Show the trend                                                                            
                    trend.style("display", null)
                    # Find the new position
                    dist = x(snd.date) - x(fst.date)
                    tx   = x(fst.date) + (dist)/2
                    # Put the rend beside the dots when there a close
                    if dist < 50
                        ty = Math.min( y(fst.ratio), y(snd.ratio) ) + 40
                    else
                        ty = Math.min( y(fst.ratio), y(snd.ratio) )
                    # Set the position
                    trend.transition()
                        .attr("transform", "translate(#{tx}, #{ty})")
                else
                    # Hide the trend                                                                            
                    trend.style("display", "none")
        tips:
            update: ()->                
                # Update the existing activePoint
                _.each $scope.activePoints, (d, key)->
                    # Update the data within activePoints
                    $scope.activePoints[key] = $scope.answers[key]
                # Render the tips
                point.tips.clean()
            clean:->
                # For each point's tips
                # look for the useless ones
                $(".point-tips").each (key, tip)-> 
                    index = $(tip).data("point")
                    # Remove the inative point
                    $(tip).remove() unless $scope.activePoints[index]
                # For each activepoint,
                # look for the missing tips                
                _.each $scope.activePoints, point.tips.add

            add: (d, index)->
                $tips = $(".point-tips[data-point=" + index + "]")
                $point = $(chartSvg.selectAll(".data-point")[0][index])  
                # tips doenst exist yet
                if $tips.length is 0
                    # Create the tips
                    $tips = $("<div class='point-tips' data-point='" + index + "' />") 
                    # offset of the point according its data
                    offset = point.offset(d);      
                    # Positionate the tips to under the mouse
                    $tips.css
                        left: offset.left
                        top:  offset.top
                    # Appends the tips to the bodu
                    $tips.appendTo "body"   
                # tips exists
                else        
                    # offset of the point according its data
                    offset = point.offset(d);      
                    # Positionate the tips to under the mouse
                    $tips.css
                        left: offset.left
                        top:  offset.top
                # In any case, change the content of the tip
                $tips.html "<div class='content'>" + ~~d.ratio + "%</div>"

        toggle: (d, index)->             
            p = d3.select this
            if not d.selected? or d.selected isnt true
                d.selected = true
                p.attr "fill", "#323c45"                
                $scope.activePoints[index] = d
                # if there is more than 2 points
                if _.keys($scope.activePoints).length > 2
                    # Get closest point
                    closestIdx = closestActivePoints(index)
                    closestElt = d3.selectAll(".data-point")[0][closestIdx]
                    # If element exists
                    if closestElt
                        # Unselect it
                        d3.select(closestElt).attr "fill", $filter("colors")($scope.question)
                        delete $scope.activePoints[closestIdx].selected = false
                        delete $scope.activePoints[closestIdx]

                $scope.$apply()
            else
                d.selected = false
                p.attr "fill", $filter("colors")($scope.question)
                delete $scope.activePoints[index].selected = false
                delete $scope.activePoints[index]             
                $scope.$apply()

    insertLinebreaks = (d) ->
        el = d3.select(this)
        words = dateFormat(d).split(" ")
        el.text ""
        i = 0

        while i < words.length
            tspan = el.append("tspan").text(words[i])
            tspan.attr("x", 0).attr "dy", "12"  if i > 0
            i++

    render = ()->    
        loadShortcuts()    
        # Empty container
        chart.empty()
        axis.empty()
        # Update tips
        point.tips.update()        
        # Do we stop
        return false if $scope.answers.length is 0                    
        # Parse dates and numbers. We assume $scope.answers is sorted by date.
        _.each $scope.answers, (d) ->
            try 
                return d.date = parse(d.date)  
            # Some parsings fail          
            catch error
                return null

        dotGap    = Math.max(minGap, wrapperWidth / ($scope.answers.length - 1))
        w         = (dotGap * ($scope.answers.length - 1)) - padding[1] - padding[3]
        h         = wrapperHeight - padding[0] - padding[2]        
        gradientW = (w / ($scope.answers.length - 1)) * 2    


        # Scales and axes. Note the inverted domain for the y-scale: bigger is up!
        x.range [0, w]
        y.range [h, 0]
        xAxis = d3.svg.axis().scale(x).tickSize(tickSize).tickPadding(10).tickFormat(dateFormat).ticks(d3.time.months, 2)
        yAxis = d3.svg.axis().scale(y).tickSize(tickSize).tickPadding(5).tickFormat((d)->d+"%").orient("left")

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

        chart.css("width",  w + padding[1] + padding[3])

        # Add an SVG element with the desired dimensions and margin.
        chartSvg = d3.select( chart[0] )
                .append("svg:svg")
                    .attr("width",  w + padding[1] + padding[3])
                    .attr("height", h + padding[0] + padding[2])
                    .append("g")
                        .attr("transform", "translate(" + padding[3] + "," + padding[0] + ")")

        # Add an another svg presenting the y axis
        yAxisSvg = d3.select( axis[0] )
                        .append("svg:svg")                        
                            .attr("width",  axis.width())
                            .attr("height", h + padding[0] + padding[2])

        unless Modernizr.svg         
            # Add the area path.
            chartSvg.append("svg:path")
                    .attr("class", "area bg")
                    .attr("fill", $filter("colors")($scope.question))
                    .attr("d", area($scope.answers))
        # Add stripes
        else            
            chartSvg.append("linearGradient")
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
            chartSvg.append("svg:path")
                .attr("class", "area bg")
                .attr("fill", "url(#sequence-gradient)")
                .attr("d", area($scope.answers))

        # Add line dots
        chartSvg.selectAll(".data-point")
            .data($scope.answers)
            .enter()
            .append("svg:circle")
                .attr("class", "data-point")
                .attr("cx", (d)-> x d.date)
                .attr("cy", (d)-> y d.ratio)
                .attr("fill", $filter("colors")($scope.question))
                .attr("r", 5)
                .attr("stroke-width", 3)
                .attr("stroke", "#ffffff")
                .on("mousemove",  point.tips.add)
                .on("mouseleave", point.tips.clean)
                .on("click",      point.toggle)

        trendDisplay = if _.keys($scope.activePoints).length < 2 then "none" else null
        # Create a group to contain the trend circle
        trend = chartSvg.append("g")
                            .style("display", trendDisplay)
                            .attr("class", "trend")
                            .attr("transform", "translate(#{w/2}, -50)")

        # Appends a circle
        trend.append("svg:circle")
            .attr("r", 25)
            .attr("fill", "#cc0e00")

        # Appends a text
        trend.append("svg:text")
            .attr("y", 5)
            .attr("text-anchor", "middle")
            .attr("fill", "#fff")
            .style("font-size", 16)
            .style("font-weight", "bold")
            .text $filter("supPercent")("10%", false)


        # Add the x-axis.
        chartSvg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, #{h + 25-tickSize})")            
            .call xAxis

        # Add the y-axis to an other svg
        yAxisSvg.append("g")
            .attr("class", "y axis")
            .attr("transform", "translate(#{30+tickSize}, #{padding[0]})")
            .call yAxis    

        # Add axis break line
        chartSvg.selectAll(".axis g text").each insertLinebreaks
        # Removes horizontal lines
        chartSvg.selectAll(".axis path").remove()
        yAxisSvg.selectAll(".axis path").remove()
        # Adjust text size
        chartSvg.selectAll(".axis g text").attr "font-size", 10
        yAxisSvg.selectAll(".axis g text").attr "font-size", 10 
        # Draw ticks
        chartSvg.selectAll(".axis g line").attr "stroke", "#aaa"
        chartSvg.selectAll(".axis g line").attr "stroke-width", 1
        yAxisSvg.selectAll(".axis g line").attr "stroke", "#aaa"
        yAxisSvg.selectAll(".axis g line").attr "stroke-width", 1 
        
        # jscrollpane already exists
        if wrapper.data("jsp")?
            # Reinitialize jscrollpane
            wrapper.data("jsp").reinitialise() 
        else        
            # Add customise scrollbar
            wrapper.jScrollPane hideFocus: true

        # This is the end
        return true

    # Watch for model change to update the graph
    $scope.$watch 'sample',       update
    $scope.$watch 'question',     update    
    $scope.$watch 'activePoints', point.tips.clean, true
    $scope.$watch 'activePoints', point.setTrend, true
    # Watch the controller destruction
    $scope.$on '$destroy', ->
        $scope.activePoints = []
        # Force active point removing     
        point.tips.clean()

            

AnswerGraphCtrl.$inject = ['$scope', 'Answer', '$rootElement', '$routeParams', '$location', '$filter'];
