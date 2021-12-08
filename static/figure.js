class Figure {
	constructor(figID, data) {
		// These constants set fixed values for height and width to be used in making all four visualizations
		this.MARGIN = { top: 30, right: 230, bottom: 30, left: 50 };
		this.GLOBAL_WIDTH = 1200 - this.MARGIN.left - this.MARGIN.right;
		this.GLOBAL_HEIGHT = 200 - this.MARGIN.top - this.MARGIN.bottom;

		//Sets the dimensions and location of the svg container
		this.figID = figID;

		let node = document.createElement("div");
		node.style.position = "relative";
		this.container = document.getElementById("my_dataviz").appendChild(node);

		this.svg = d3.select(this.container)
			.append("svg")
			.attr("width", this.GLOBAL_WIDTH + this.MARGIN.left + this.MARGIN.right)
			.attr("height", this.GLOBAL_HEIGHT + this.MARGIN.top + this.MARGIN.bottom + 45)
			.append("g")
			.attr("transform", "translate(" + this.MARGIN.left + "," + this.MARGIN.top + ")");
			
		this.y = d3.scaleLinear()
			.domain([0, 1])
			.range([this.GLOBAL_HEIGHT, 0]);

		// add the x Axis
		this.x = d3.scaleBand()
			.range([0, this.GLOBAL_WIDTH])
			.domain(data.map(function(d) { return d.resid; }))
			.padding(0.2);
			
		this.data = data;

		return this;
	}

	add_title(title){
	    // Creates the title
		this.svg.append("text")
			.attr("x", this.GLOBAL_WIDTH / 2)
			.attr("y", this.MARGIN.top - 25)
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
		linearGradient.append("stop").attr("offset", "0%").attr("stop-color", ctop);
		//Set the color for the end (25%)
		if (cq1) {
			linearGradient.append("stop").attr("offset", "25%").attr("stop-color", cq1);
		}
		//Set the color for the end (50%)
		if (cmid) {
			linearGradient.append("stop").attr("offset", "50%").attr("stop-color", cmid);
		}
		//Set the color for the end (75%)
		if (cq3) {
			linearGradient.append("stop").attr("offset", "75%").attr("stop-color", cq3);
		}
		//Set the color for the end (100%)
		linearGradient.append("stop").attr("offset", "100%").attr("stop-color", cend);

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
	add_tooltip(content="Place Holder", xpos=this.GLOBAL_WIDTH, ypos=this.MARGIN.top-20) {
		this.infoIcon = document.createElement("div");
		this.infoIcon.style.position = "absolute";
		this.infoIcon.style.top = ypos + "px";
		this.infoIcon.style.left = xpos + 30 + "px";
		this.infoIcon.style.font = "arial";
		this.infoIcon.style.cursor = "pointer";
		this.infoIcon.style.fontSize = "larger";
		this.infoIcon.style.fill = "blue";
		this.infoIcon.innerText = '\u{24D8}';
		this.infoIcon.type = "button";
		this.infoIcon.title = '<a onclick="$(this).closest(\'div.popover\').popover(\'hide\');" type="button" class="close" aria-hidden="true">&times;</a><br>';
		this.infoIcon.style.zIndex = "10"; // Put this element on top of the SVG
		
		$(this.infoIcon).popover({
			content: content, 
			placement: "top", 
			html: true,
			sanitize: false,
			container: 'body'
		});

		this.container.appendChild(this.infoIcon);

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
			.attr("x", 0 - (this.GLOBAL_HEIGHT / 2) - 50)
			.attr("y", this.MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("p");

		var ylabel = this.svg.append("g").attr("id", "ylabel")
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (this.GLOBAL_HEIGHT / 2) - 20)
			.attr("y", this.MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("s");


		//"h" blob y-axis label for globular tendency plot
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (this.GLOBAL_HEIGHT / 2) + 10)
			.attr("y", this.MARGIN.left - 80)
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
			.attr("x", 0 - (this.GLOBAL_HEIGHT / 2))
			.attr("y", this.MARGIN.left - 80)
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
	add_BlobLegend(keysize=20, offset=20) {
		//This section contains the key that appears next to the Globular tendency colored plot
		//squares for the key
		var legend = this.svg.append("g").attr("id", "legend")

		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 5)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#0071BC")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 35)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#F7931E")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 65)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#2DB11A")
				
		//Text that appears to the right of the key    
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 15).text("h blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 45).text("p blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 75).text("s blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
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
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top - 25)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#0f0")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 5)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#FEE882")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 35)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#BF72D2")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 65)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#f00")
		legend.append("rect")
			.attr("x", this.GLOBAL_WIDTH + offset)
			.attr("y", this.MARGIN.top + 95)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#00f")
				
		//Text that appears to the right of the key    
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top - 15).text("Globular").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 15).text("Janus/Boundary").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 45).text("Strong Polyelectrolyte").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 75).text("Strong Polyanion (-)").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.GLOBAL_WIDTH + 50)
			.attr("y", this.MARGIN.top + 105).text("Strong Polycation (+)").style("font-size", "15px")
			.attr("alignment-baseline", "middle")

		return this;
	}
	
	add_ContinuousLegend(cmap, {min='-1', med='0', max='+1', width=20, height=80}={min: '-1', med: '0', max: '+1', width: 20, height: 80}) {
		switch(cmap) {
			case "PuOr":
				this.add_colorbar("PuOr", width, height, min, max, this.GLOBAL_WIDTH, this.GLOBAL_HEIGHT,
					{ med: med, cend: '#7f3b08', cq3: '#ee9d3c', cmid: '#f6f6f7', ctop: '#2d004b' });
				break;
			case "RWB":
				//Color bar key to the right of the enrichment plot.
				this.add_colorbar("RWB", width, height, min, max, this.GLOBAL_WIDTH, this.GLOBAL_HEIGHT,
					{ med: med, cend: '#ff0000', cmid: '#f4f4ff', ctop: '#0000ff' });
				break;
			default:
				try {
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
				this.add_colorbar("PuOr", width, height, min, max, this.GLOBAL_WIDTH, this.GLOBAL_HEIGHT,
					{ med: med, cend: '#7f3b08', cq3: '#ee9d3c', cmid: '#f6f6f7', ctop: '#2d004b'});
				break;
			case "RWB":
				//Color bar key to the right of the enrichment plot.
				this.add_colorbar("RWB", width, height, min, max, this.GLOBAL_WIDTH, this.GLOBAL_HEIGHT,
					{ med: med, cend: '#ff0000', cmid: '#f4f4ff', ctop: '#0000ff' });
				break;
			default:
				try {
					throw cmap
				} catch(e) {
					      ("Figure.add_ContinuousLegend doesn't know colormap: "+e)
				}
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
		
		if (med){this.svg.append("text").attr("x", xpos+2*width+6).attr("y", (2*ypos-height+12)/2).text(med)}
		
		this.svg.append("text").attr("x", xpos+2*width+6).attr("y", ypos+6).text(min)

		return this
	}
	
	/* add_snps
	*/
	add_snps(my_snp, tooltip_snps, x=this.x, y=this.y) {
		var arc = d3.symbol().type(d3.symbolTriangle)
		this.svg.append('g')
			.selectAll("rect")
			//.data(my_disorder.map(function(d) { return +d; }))
			.data(my_snp)
			.enter()
			.append("path")
			.attr('d', arc)
			.attr("transform", (d) => "translate(" + (x(d.resid) + x.bandwidth()/2) + ", 145)")
			.attr("fill", 'black')
			.on("click", function(d) {
				//window.location.href = d.xrefs[0].url+'_blank'
				window.open(d.xrefs.url, '_blank')
			})
			.on("mouseover", function(d) {
				d3.select(this)
					.attr("fill", "red");
				tooltip_snps.transition()
					.on("start", () => tooltip_snps.style("display", "block"))
					.duration(100)
					.style("opacity", .9);
				tooltip_snps.html('<a href="' + d.xrefs.url + '"target="_blank">' + d.xrefs.id + "</a>")
					.style("left", (d3.event.pageX) + "px")
					.style("top", (d3.event.pageY - 28) + "px");
			})
			.on("mouseout", function(d, i) {
				d3.select(this).attr("fill", "black");
				tooltip_snps.transition()
					.duration(500)
					.style("opacity", 0)
					.on("end", () => tooltip_snps.style("display", "none"));
			});

		return this;
	}
	
	add_yAxis() {
		this.svg.append("g") //the y axis is drawn only for plot 1
				.call(d3.axisLeft(this.y));
		return this
	}
	
	add_cutoff_line(my_cut, x=this.x, y=this.y) {
		this.cut_line = this.svg.append('g')
			.append("path")
			.attr("class", "mypath")
			.datum(this.data)
			.attr("fill", "none")
			.attr("stroke", "steelblue")
			.attr("stroke-width", 1.5)
			.attr("d", d3.line()
				.x((d) => x(d.resid))
				.y((d) => y(my_cut)));

		return this;
	}
	
	update_cutoff_line(my_cut, x=this.x, y=this.y) {
		this.cut_line
			.transition()
			.duration(1000)
			.attr("d", d3.line()
				.x((d) => x(d.resid))
				.y((d) => y(my_cut)));

		return this;
	}

	/* add_hydropathy_bars
	*/
	add_hydropathy_bars(x=this.x, y=this.y) {
		this.hydropathy_bars = this.svg.selectAll("mybar")
		this.hydropathy_bars.data(this.data)
			.enter()
			.append("rect")
			.attr("x", (d) => x(d.resid))
			.attr("y", (d) => y(d.hydropathy_3_window_mean))
			.attr("width", x.bandwidth())
			.attr("height", (d) => this.GLOBAL_HEIGHT - y(d.hydropathy_3_window_mean))
			.attr("fill", 'grey')

		return this
	}

	add_xAxis(domain_threshold_max, x=this.x, y=this.y){
		this.xAxis = this.svg.append("g")
						.call(d3.axisBottom(x).tickValues(x.domain().filter(function(d, i) { return !((i+1) % 
						   (Math.round((Math.round(domain_threshold_max/10))/10)*10) )})))
						.attr("transform", "translate(0," + this.GLOBAL_HEIGHT + ")");
		// Bars
		//Creates the "Residue" x-axis label
		this.svg.append("text")
			.attr("x", this.GLOBAL_WIDTH / 2)
			.attr("y", this.GLOBAL_HEIGHT + this.MARGIN.bottom)
			.style("text-anchor", "middle")
			.text("Residue")

		return this
	}


	add_snp_xAxis(domain_threshold_max, x=this.x, y=this.y){
		this.xAxis = this.svg.append("g")
						.call(d3.axisBottom(x).tickValues(x.domain().filter(function(d, i) { return !((i+1) % 
						   (Math.round((Math.round(domain_threshold_max/10))/10)*10) )})))
						.attr("transform", "translate(0," + this.GLOBAL_HEIGHT + ")")
						.attr("transform", "translate(0, 155)");
		// Bars
		//Creates the "Residue" x-axis label
		this.svg.append("text")
			.attr("x", this.GLOBAL_WIDTH / 2)
			.attr("y", this.GLOBAL_HEIGHT + this.MARGIN.bottom + 40)
			.style("text-anchor", "middle")
			.text("Residue")

		return this
	}


	build_barChart(timing=0, x=this.x, y=this.y) {
		this.plot_variable = this.svg.append("g")
								.attr("id", "barChart"+this.figID)
								.selectAll("rect")
								.data(this.data);

		this.bars = this.plot_variable.enter().append("rect");
		this.bars.attr("width", x.bandwidth())
			.attr("x", (d) => x(d.resid))
			.attr("y", this.GLOBAL_HEIGHT)
		this.update_bars(this.data, timing);

		return this;
	}
	
	update_bars(data, timing=1000, x=this.x, y=this.y) {
		this.data = data;
		this.plot_variable.enter().selectAll("rect").data(data);
		
		// The hydropathy plot requires special colors
		if (this.figID == "pathyPlot") {
			this.bars.transition()
				.duration(timing)
				.attr("y", (d) => y(d.hydropathy_3_window_mean))
				.attr("height", (d) => this.GLOBAL_HEIGHT - y(d.hydropathy_3_window_mean));
			this.bars.attr("fill", 'grey');
		} else {
			// Lookup table for color attribute of our data as a function of the plot name.
			// E.g. The "globPlot" plot data stores colors in the "P_diagram" attribute of the data.
			const figID_to_var = {'blobPlot': 'blob_color', 'globPlot': 'P_diagram', 'ncprPlot': 'NCPR_color', 'richPlot': 'h_blob_enrichment',
				'uverskyPlot': 'uversky_color', 'disorderPlot': 'disorder_color'};

			this.bars.transition()
				.duration(timing)
				.attr("y", (d) => y(d.domain_to_numbers))
				.attr("height", (d) => this.GLOBAL_HEIGHT - y(d.domain_to_numbers))
				.attr("fill", (d) => d[figID_to_var[this.figID]]);
			
			// Update/add the corresponding skyline, in a potentially ugly way
			this.add_skyline();
		}
		return this;
	}


	add_skyline(data=this.data, x=this.x, y=this.y) {
		// We should have at least two data points to draw a line
		if(data.length < 2) {
			return;
		}
		
		// Do we already have a skyline? Remove it
		if(this.skyline !== undefined) {
			this.skyline.remove();
		}

		// Start the line in the correct spot
		let points = [{resid: data[0].resid, height: data[0].domain_to_numbers}];

		// Find the edges of each "skyscraper"
		for(let i = 1; i < data.length; i++){
			let last_res = data[i-1].domain_to_numbers;
			let this_res = data[i].domain_to_numbers;
			let resid = data[i].resid;
			if (last_res != this_res) {
				points.push({resid: resid, height: last_res});
				points.push({resid: resid, height: this_res});
			} 
		}

		// Last line segment
		const last_resid = data[data.length-1].resid;
		points.push({resid: last_resid,
			height: data[data.length-1].domain_to_numbers});

		this.skyline = this.svg.append('g');
		this.skyline.append("path")
			.attr("class", "mypath")
			.datum(points)
			.attr("fill", "none")
			.attr("stroke", "grey")
			.attr("stroke-width", 1.0)
			.attr("d", d3.line()
				.x(function (d) {
					// Extend the final line segment all the way to the right
					if(d.resid == last_resid) {
						return x(d.resid) + x.bandwidth();
					} else {
						return x(d.resid);
					}
				})
				.y((d) => y(d.height)));

		return this;
	}
}