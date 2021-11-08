class Figure {
	/*
	container
	figID;
	width;
	height;
	tooltip;
	yaxis;
	svg;
	title="";
	snps;
	legend;
	bars;
	barchart;
	data;
	cut_line;
	Tooltip;
	infoIcon;
	plot_variable;
	x;
	y;
	xAxis;
	*/
	
	constructor(figID, data) {
		//Sets the dimensions and location of the svg container
		this.figID = figID

		var node = document.createElement("div")
		node.style.position = "relative"
		this.container = document.getElementById("my_dataviz").appendChild(node)

		this.svg = d3.select(this.container)
			.append("svg")
			.attr("width", GLOBAL_WIDTH + MARGIN.left + MARGIN.right)
			.attr("height", GLOBAL_HEIGHT + MARGIN.top + MARGIN.bottom + 45)
			.append("g")
			.attr("transform", "translate(" + MARGIN.left + "," + MARGIN.top + ")")
			
		this.y = d3.scaleLinear()
			.domain([0, 1])
			.range([GLOBAL_HEIGHT, 0]);

		// add the x Axis
		this.x = d3.scaleBand()
			.range([0, GLOBAL_WIDTH])
			.domain(data.map(function(d) { return d.resid; }))
			.padding(0.2);
			
		this.data = data;

		return this;
	}

	set_data(data) {this.data=data; return this;}
	
	add_title(title){
	    //Creates the title
		this.svg.append("text")
			.attr("x", GLOBAL_WIDTH / 2)
			.attr("y", MARGIN.top - 25)
			.style("text-anchor", "middle")
			.text(title)
			.attr("font-size", "20px")

		return this;
	}
	
	/* add_linearGradient:
        Function to create linear color bars for graphs. Adapted from: https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient/
		Inputs: 
			svg container, 
			ctop and cend for the first and last colors of the gradient
			an id string
			optional arguments: cq1, cmid, cq3 which define the colors at 25%, 50%, and 75% respectively.d
		Returns:
			The svg with a linear gradient with the given id
	*/
	add_linearGradient(id, ctop, cend, {cq1, cmid, cq3}={}) {
		var defs = this.svg.append("defs");

		//Append a linearGradient element to the defs and give it a unique id
		var linearGradient = defs.append("linearGradient").attr("id", id).attr("x1", "0%").attr("y1", "0%").attr("x2", "0%").attr("y2", "100%");

		//Define the gradient
		//Set the color for the start (0%)
		linearGradient.append("stop").attr("offset", "0%").attr("stop-color", ctop)
		//Set the color for the end (25%)
		if (cq1){linearGradient.append("stop").attr("offset", "25%").attr("stop-color", cq1)}
		//Set the color for the end (50%)
		if (cmid){linearGradient.append("stop").attr("offset", "50%").attr("stop-color", cmid)}
		//Set the color for the end (75%)
		if (cq3){linearGradient.append("stop").attr("offset", "75%").attr("stop-color", cq3)}
		//Set the color for the end (100%)
		linearGradient.append("stop").attr("offset", "100%").attr("stop-color", cend)

		return this;
	}
	

/* add_tooltip
	FUNCTION: add_tooltip
	SHORT DESCRIPTION: add a small i that provides information to the user in a tooltip
	INPUTS:
		svg - a container for a graph (modified by the function directly)
	RETURNS:
		none
	*/
	add_tooltip(content="Place Holder", {xpos, ypos, xoffset}={xpos: GLOBAL_WIDTH, ypos: MARGIN.top, xoffset: 500}) {
		var ii = document.createElement("info")

		ii.style.position = "absolute"
		ii.style.top = ypos
		ii.style.left = xpos+30
		ii.style.font = "arial"
		ii.style.cursor = "pointer"
		ii.style.fontSize = "larger"
		ii.style.fill = "blue"
		ii.innerText = '🛈'
		ii.type = "button"


		var genericCloseBtnHtml = '<a onclick="$(this).closest(\'div.popover\').popover(\'hide\');" type="button" class="close" aria-hidden="true">&times;</a>';
		
		var p = $(ii).popover({
			title: genericCloseBtnHtml+'<p></p>',
			content: content, 
			placement:"top", 
			html: true,
			sanitize: false,
			container: 'body'
		}) 

		this.infoIcon = ii
		this.container.appendChild(this.infoIcon)

		return this;
	}

	/* add_psh_ylabel
	FUNCTION: add_psh_ylabel
	SHORT DESCRIPTION: add an p s h text y label to the svg object
	INPUTS:
		svg - a container containing an graph modified by the function itself
	RETURNS:
		none
	*/
	add_psh_ylabel() {
		//"p" blob y-axis label for globular tendency plot
		var ylabel = this.svg.append("g").attr("id", "ylabel")
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (GLOBAL_HEIGHT / 2) - 50)
			.attr("y", MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("p");

		var ylabel = this.svg.append("g").attr("id", "ylabel")
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (GLOBAL_HEIGHT / 2) - 20)
			.attr("y", MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("s");


		//"h" blob y-axis label for globular tendency plot
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (GLOBAL_HEIGHT / 2) + 10)
			.attr("y", MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("h");

		//"SNPs" y-axis label for globular tendency plot

		return this;
	}

	add_pathy_ylabel() {
		//Creates the "Mean Hydropathy" y-axis label for Smoothed hydropathy per residue
		this.svg.append("text") 
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (GLOBAL_HEIGHT / 2))
			.attr("y", MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("Mean Hydropathy");

		return this;
	}

	/* add_GlobularLegend
	FUNCTION: add_GlobularLegend
	SHORT DESCRIPTION: add the discrete legend for the globular tendencies graph
	INPUTS:
		svg - a container containing an graph modified by the function itself
	RETURNS:
		none
	*/
	add_GlobularLegend(keysize=20, offset=20) {
		//This section contains the key that appears next to the Globular tendency colored plot
		//squares for the key
		var legend = this.svg.append("g").attr("id", "legend")

		legend.append("rect")
			.attr("x", GLOBAL_WIDTH + offset)
			.attr("y", MARGIN.top - 25)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#0f0");
		legend.append("rect")
			.attr("x", GLOBAL_WIDTH + offset)
			.attr("y", MARGIN.top + 5)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#FEE882");
		legend.append("rect")
			.attr("x", GLOBAL_WIDTH + offset)
			.attr("y", MARGIN.top + 35)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#BF72D2");
		legend.append("rect")
			.attr("x", GLOBAL_WIDTH + offset)
			.attr("y", MARGIN.top + 65)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#f00");
		legend.append("rect")
			.attr("x", GLOBAL_WIDTH + offset)
			.attr("y", MARGIN.top + 95)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#00f");
				
		//Text that appears to the right of the key    
		legend.append("text")
			.attr("x", GLOBAL_WIDTH + 50)
			.attr("y", MARGIN.top - 15).text("Globular").style("font-size", "15px")
			.attr("alignment-baseline", "middle");
		legend.append("text")
			.attr("x", GLOBAL_WIDTH + 50)
			.attr("y", MARGIN.top + 15).text("Janus/Boundary").style("font-size", "15px")
			.attr("alignment-baseline", "middle");
		legend.append("text")
			.attr("x", GLOBAL_WIDTH + 50)
			.attr("y", MARGIN.top + 45).text("Strong Polyelectrolyte").style("font-size", "15px")
			.attr("alignment-baseline", "middle");
		legend.append("text")
			.attr("x", GLOBAL_WIDTH + 50)
			.attr("y", MARGIN.top + 75).text("Strong Polyanion (-)").style("font-size", "15px")
			.attr("alignment-baseline", "middle");
		legend.append("text")
			.attr("x", GLOBAL_WIDTH + 50)
			.attr("y", MARGIN.top + 105).text("Strong Polycation (+)").style("font-size", "15px")
			.attr("alignment-baseline", "middle");

		return this;
	}
	
	add_ContinuousLegend(cmap, {min='-1', med='0', max='+1', width=20, height=80}={min: '-1', med: '0', max: '+1', width: 20, height: 80}) {
		switch(cmap) {
			case "PuOr":
				this.add_colorbar("PuOr", width, height, min, max, GLOBAL_WIDTH, GLOBAL_HEIGHT,
					{med: med, 
					cend: '#7f3b08',
					cq3: '#ee9d3c', 
					cmid: '#f6f6f7',
					ctop: '#2d004b'
					});
				break;
			case "RWB":
				//Color bar key to the right of the enrichment plot.
				this.add_colorbar("RWB", width, height, min, max, GLOBAL_WIDTH, GLOBAL_HEIGHT,
					{med: med, 
					cend: '#ff0000',
					cmid: '#f4f4ff',
					ctop: '#0000ff'
					});
				break;
			default:
				// XXX: ???	
				try{
					throw cmap
				} catch(e) {
					console.log("Figure.add_ContinuousLegend doesn't know colormap: "+e)
				}
		}

		return this;
	}

	add_ncprContinuousLegend(cmap, {min='-1', med='0', max='+1', width=20, height=80}={min: '-0.5', med: '0', max: '+0.5', width: 20, height: 80}) {
		switch(cmap) {
			case "PuOr":
				this.add_colorbar("PuOr", width, height, min, max, GLOBAL_WIDTH, GLOBAL_HEIGHT,
					{ med: med, 
					cend: '#7f3b08',
					cq3: '#ee9d3c', 
					cmid: '#f6f6f7',
					ctop: '#2d004b'
					})
				break;
			case "RWB":
				//Color bar key to the right of the enrichment plot.
				this.add_colorbar("RWB", width, height, min, max, GLOBAL_WIDTH, GLOBAL_HEIGHT,
					{med: med, 
					cend: '#ff0000',
					cmid: '#f4f4ff',
					ctop: '#0000ff'
					})
				break;
			default:
				try{throw cmap} catch(e) {console.log("Figure.add_ContinuousLegend doesn't know colormap: "+e)}
		}

		return this;
	}
	
	/* add_colorbar
    Function to create linear color bars for graphs. Adapted from: https://www.visualcinnamon.com/2016/05/smooth-color-legend-d3-svg-gradient/
    Inputs: 
      svg container,
      width and height of the colorbar in px
      min and max values
      x and y position of the upper left corner
      ctop and cend for the first and last colors of the gradient
      Unique id string
      optional arguments: cq1, cmid, cq3 which define the colors at 25%, 50%, and 75% respectively.d
    Returns: 
        none - svg is passed "by reference"
	*/
	add_colorbar(id, width, height, min, max, xpos, ypos, {ctop, cend, med, cq1, cmid, cq3}={}) {
		this.add_linearGradient(id, ctop, cend, {cq1, cmid, cq3})

		//Draw the rectangle and fill with the gradient
		this.svg.append("rect").attr("width", width).attr("height", height).attr("y", ypos-height).attr("x", xpos+width).style("fill", "url(#"+id+")");

		//Add labels
		this.svg.append("text").attr("x", xpos+2*width+6).attr("y", ypos-height+6).text(max)
		
		if (med) {
			this.svg.append("text").attr("x", xpos+2*width+6).attr("y", (2*ypos-height+12)/2).text(med);
		}
		
		this.svg.append("text").attr("x", xpos+2*width+6).attr("y", ypos+6).text(min)

		return this
	}
	
	/* add_snps
	*/
	add_snps(x=this.x, y=this.y) {
		//console.log("not pathyplot")
		this.svg.append('g')
			.selectAll("rect")
			//.data(my_disorder.map(function(d) { return +d; }))
			.data(my_snp)
			.enter()
			.append("rect")
			.attr("x", function(d) { return x((d.resid)); })
			.attr("y", function(d) { return y(0); })
			.attr("width", x.bandwidth())
			.attr("height", function(d) { return y(0.84); })
			.attr("fill", 'black')
			.on("click", function(d) {
				//window.location.href = d.xrefs[0].url+'_blank'
				window.open(d.xrefs.url, '_blank')
			})
			.on("mouseover", function(d) {
				d3.select(this)
					.attr("fill", "red");
				Tooltip_snps.transition()
					.duration(100)
					.style("opacity", .9);
				Tooltip_snps.html(
						'<a href="' + d.xrefs.url + '"target="_blank">' + d.xrefs.id +
						"</a>")
					.style("left", (d3.event.pageX) + "px")
					.style("top", (d3.event.pageY - 28) + "px");
			})
			.on("mouseout", function(d, i) {
				d3.select(this).attr("fill", function() {
					return "" + 'black' + "";
				});
				
				Tooltip_snps.transition()
					.duration(500)
					.style("opacity", 0);
			})

		return this
	}
	
	add_yAxis() {
		this.svg.append("g") //the y axis is drawn only for plot 1
				.call(d3.axisLeft(this.y));
		return this;
	}


//	add_cut_line(x=this.x, y=this.y) {
//		this.add_cutoff(this.x, this.y)
//		this.add_hydropathy_bar(this.x, this.y)
//	}
	
	/* add_cutoff
	*/
	add_cutoff_line(x=this.x, y=this.y) {
		this.cut_line = this.svg.append('g')
			.append("path")
			.attr("class", "mypath")
			.datum(this.data)
			.attr("fill", "none")
			.attr("stroke", "steelblue")
			.attr("stroke-width", 1.5)
			.attr("d", d3.line()
				.x(function(d) { return x(d.resid) })
				.y(function(d) { return y(my_cut) })
			);

		return this;
	}
	
	update_cutoff_line(x=this.x, y=this.y) {
		let given_cutoff=d3.select("#cutoff_user").text()
		this.cut_line
			.transition()
			.duration(1000)
			.attr("d", d3.line()
				.x(function(d) { return x(d.resid); })
				.y(function(d) { return y(given_cutoff); })
			);

		return this;
	}

	/* add_hydropathy_bars
	*/
	add_hydropathy_bars(x=this.x, y=this.y) {
		this.hydropathy_bars = this.svg.selectAll("mybar")
		this.hydropathy_bars.data(this.data)
			.enter()
			.append("rect")
			.attr("x", function(d) { return x(d.resid); })
			.attr("y", function(d) { return y(d.hydropathy_3_window_mean); })
			.attr("width", x.bandwidth())
			.attr("height", function(d) { return GLOBAL_HEIGHT - y(d.hydropathy_3_window_mean); })
			.attr("fill", 'grey');

		return this;
	}

	add_xAxis(x=this.x, y=this.y){
		this.xAxis = this.svg.append("g")
						.call(d3.axisBottom(x).tickValues(x.domain().filter(function(d, i) {
							return !((i+1) % (Math.round((Math.round(domain_threshold_max/10))/10)*10));
						})))
						.attr("transform", "translate(0," + GLOBAL_HEIGHT + ")");
		// Bars
		//Creates the "Residue" x-axis label
		this.svg.append("text")
			.attr("x", GLOBAL_WIDTH / 2)
			.attr("y", GLOBAL_HEIGHT + MARGIN.bottom)
			.style("text-anchor", "middle")
			.text("Residue");

		return this
	}


	add_snp_xAxis(x=this.x, y=this.y){
		this.xAxis = this.svg.append("g")
						.call(d3.axisBottom(x).tickValues(x.domain().filter(function(d, i) { return !((i+1) % 
						   (Math.round((Math.round(domain_threshold_max/10))/10)*10) )})))
						.attr("transform", "translate(0," + GLOBAL_HEIGHT + ")")
						.attr("transform", "translate(0, 165)");
		// Bars
		//Creates the "Residue" x-axis label
		this.svg.append("text")
			.attr("x", GLOBAL_WIDTH / 2)
			.attr("y", GLOBAL_HEIGHT + MARGIN.bottom + 40)
			.style("text-anchor", "middle")
			.text("Residue");

		return this;
	}

	// Run-length-encodes data identified by a key in this array of dicts
	// Conceptually:
	// t, t, t, t, o, o, m, m, m, m, m => t*4, o*2, m*5
	//   t: offset: 0, length: 4
	//   o: offset: 4, length: 2
	//   m: offset: 6, length: 5
	run_length_encode_data(data, key) {
		let offsets = [], widths = [0], values = [];
		let d, val, offset_counter = 0, last_val = null, iter = data.values();
		while(d = iter.next(), !d.done) {
		    val = d.value[key];
		    if(val != last_val && last_val != null) {
		    	// End and save this run so we can move on to the next
				offsets.push(offset_counter)
				offset_counter += widths[widths.length - 1];
				widths.push(0);
				values.push(val);
		    }
			// Increment the width of the current run
			widths[widths.length - 1]++;
			last_val = val;
		}
		offsets.push(offset_counter)
		values.push(val);
		widths.forEach((x) => { })
		// Make this into a d3-compatible data structure
		let out = [];
		for(let i = 0; i < offsets.length; i++) {
			out.push({offset: offsets[i], width: widths[i], value: values[i]});
		}
		return out;
	}


	build_barChart(timing=0, x=this.x, y=this.y) {
		this.plot_variable = this.svg.append("g")
								.attr("id", "barChart" + this.figID)
								.selectAll("rect")
								.data(this.data);
		this.update_bars(this.data, timing);

		return this;
	}

	
	update_bars(data, timing=1000, x=this.x, y=this.y) {
		this.plot_variable.exit().remove();
		this.bars = this.plot_variable.enter().append("rect");

		// Set bar heights and colors and stuff
		let relevant_attr = this.figID; // this.figID won't make it inside closures
		// Special case for hydropathy plot
		if(this.figID == "hydropathy_3_window_mean") {
			this.plot_variable.enter().selectAll("rect").data(data);
			this.bars.attr("height", (d) => GLOBAL_HEIGHT - y(d[relevant_attr]))
				.attr("width", x.bandwidth())
				.attr("x", (d) => x(d.resid) )
				.attr("y", (d) => y(d[relevant_attr]) )
				.attr("fill", "grey");
		} else {
			const step = x.step();
			const padding = step - x.bandwidth();
			let coalesced_data = this.run_length_encode_data(data, this.figID);
			this.plot_variable.enter().selectAll("rect").data(coalesced_data);
			this.bars.attr("height", (d) => GLOBAL_HEIGHT) // should subtract y(d.domain_to_numbers);
				.attr("width", (d) => d.width * step - padding)
				.attr("x", (d) => x(d.offset + 1))
				.attr("y", (d) => 0)
				.attr("fill", (d) => d.value);

			console.log(coalesced_data);
		}

		return this;
	}


	add_skyline(x=this.x, y=this.y) {
		this.skyline = this.svg.append('g')
			.append("path")
			.attr("class", "mypath")
			.datum(this.data)
			.attr("fill", "none")
			.attr("stroke", "black")
			.attr("stroke-width", 1.5)
			.attr("d", d3.line()
				.x(function(d) { return x(d.resid) })
				.y(function(d) { return y(d.domain_for_skyline) })
			);

		return this
	}


}