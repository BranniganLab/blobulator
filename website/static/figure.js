class ZFigure {
	constructor(figID, data){
		// These constants set fixed values for height and width to be used in making all visualizations
		this.MARGIN = { top: 30, right: 230, bottom: 30, left: 50 };
		this.WIDTH = 1200 - this.MARGIN.left - this.MARGIN.right;
		this.HEIGHT = 200 - this.MARGIN.top - this.MARGIN.bottom;
		
		this.figID = figID
		this.data = data
		
		let node = document.createElement("div");
		node.style.position = "relative";
		this.container = document.getElementById("my_dataviz").appendChild(node);		
		
		// append the svg object to the body of the page
		this.svg = d3.select(this.container)
		  .append("svg")
			.attr("width", this.WIDTH + this.MARGIN.left + this.MARGIN.right)
			.attr("height", this.HEIGHT + this.MARGIN.top + this.MARGIN.bottom + 45)
			.attr("figID", figID)
		  .append("g")
			.attr("transform",
				  "translate(" + this.MARGIN.left + "," + this.MARGIN.top + ")");
		

		return this
	}

	// Code for the reset zoom button, appended to the hydropathy plot

	add_zoomout_button(figID, data) {

		this.figID = figID
		this.data = data

		var btn = document.createElement("button");
		btn.innerHTML = "Reset Zoom";
		btn.id = "reset_zoom"
		btn.type = "button";
		btn.space 
		btn.onclick = function () {
			let fig = ZChart.allInstances[figID];
			let domainArray_zoom = fig.data.map(d => d.resid);
		  	let domainBounds_zoom = [Math.min(...domainArray_zoom), Math.max(...domainArray_zoom)];
		  	Object.values(ZChart.allInstances).forEach(fig => fig.do_zoom(fig.data, null, domainBounds_zoom, domainArray_zoom, fig.xAxis, fig.WIDTH, 1000));
		 };
		var top_container = document.getElementById("result_main_container");
		top_container.appendChild(btn);

		return this;
	}

	// add_mutation_button() {

	// var btn = document.createElement("button");
	// btn.innerHTML = "Add Mutation";
	// btn.id = "add_mut"
	// btn.type = "button";
	// btn.style.margin = "4px";
	// btn.onclick = function () {
	// 	var $table = $("#results_table");
	// 	var $trLast = $table.find("tr:last");
	// 	var $trNew = $trLast.clone();
	// 	$trLast.after($trNew)
	// }
	// var top_container = document.getElementById("result_main_container");
	// top_container.appendChild(btn);

	// return this;
	// }

	add_resetmutation_button() {

	var btn = document.createElement("button");
	btn.innerHTML = "Clear Mutation";
	btn.id = "reset_mut"
	btn.type = "button";
	btn.style.margin = "4px";
	btn.onclick = function () {
		if (document.getElementById("mutatebox").checked == true){
			document.getElementById("mutatebox").click();	
		};
		document.getElementById("snp_id").value = 1;
		document.getElementById("residue_type").value = "R";
	}
	var top_container = document.getElementById("result_main_container");
	top_container.appendChild(btn);

	return this;
	}
	
	add_title(title){
	    // Creates the title
		this.svg.append("text")
			.attr("x", this.WIDTH / 2)
			.attr("y", this.MARGIN.top - 5)
			.style("text-anchor", "middle")
			.text(title)
			.attr("font-size", "20px")

		return this;
	}

		add_smoothed_hydro_title(title){
	    // Creates the title
		this.svg.append("text")
			.attr("x", this.WIDTH / 2)
			.attr("y", this.MARGIN.top - 35)
			.style("text-anchor", "middle")
			.text(title)
			.attr("font-size", "20px")

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
	add_tooltip(content="Place Holder", xpos=this.WIDTH, ypos=this.MARGIN.top-20) {
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

	/* add_zoomtip
		FUNCTION: add_zoomtip
		SHORT DESCRIPTION: add a small magnifying glass that provides zoom information to the user in a tooltip
		INPUTS:
			svg - a container for a graph (modified by the function directly)
		RETURNS:
			none
	*/
	add_zoomtip(content="Place Holder", xpos=this.WIDTH, ypos=this.MARGIN.top-30) {
		this.zoomIcon = document.createElement("div");
		this.zoomIcon.style.position = "absolute";
		this.zoomIcon.style.top = ypos + "px";
		this.zoomIcon.style.left = xpos + 0 + "px";
		this.zoomIcon.style.font = "arial";
		this.zoomIcon.style.cursor = "pointer";
		this.zoomIcon.style.fontSize = 'xx-large';
		this.zoomIcon.style.fill = "blue";
		this.zoomIcon.innerText = '\u{2315}';
		this.zoomIcon.type = "button";
		this.zoomIcon.title = '<a onclick="$(this).closest(\'div.popover\').popover(\'hide\');" type="button" class="close" aria-hidden="true">&times;</a><br>';
		this.zoomIcon.style.zIndex = "10"; // Put this element on top of the SVG
		
		$(this.zoomIcon).popover({
			content: content, 
			placement: "top", 
			html: true,
			sanitize: false,
			container: 'body'
		});

		this.container.appendChild(this.zoomIcon);

		return this;
	}
	
}

// Based on this tutorial: https://www.d3-graph-gallery.com/graph/interactivity_zoom.html
class ZChart extends ZFigure{
	static allInstances = {};
	constructor(figID, data, my_snps, seq, snp_tooltips) {

		super(figID, data);

		this.y = d3.scaleLinear()
			.domain([0, 1])
			.range([this.HEIGHT, 0]);
			
		// Add X axis
		this.x = d3.scaleBand()
			.range([0, this.WIDTH])
			.domain(data.map(d => d.resid ))
			.padding(0.2);
		var x = this.x;
		
		if(my_snps == 0){
			var snps = false
		}else{
			var snps = true
		}
		this.add_xAxis(snps, x)

		// Add a clipPath: everything out of this area won't be drawn.
		var clip = this.svg.append("defs").append("svg:clipPath")
			.attr("id", "clip")
			.append("svg:rect")
			.attr("width", this.WIDTH )
			.attr("height", this.HEIGHT+45 )
			.attr("x", 0)
			.attr("y", 0);

		// Create the plot
		this.plot = this.svg.append('g')
			.attr("clip-path", "url(#clip)");

		this.data = data

		this.bars = this.plot.selectAll("bars")
			.data(this.data)
			.join("rect")
			.attr("id", "barChart"+this.figID)
			.attr("width", x.bandwidth())
			.attr("x", (d) => x(d.resid))
			.attr("y", d => this.HEIGHT);
			
		if (snps) {
			this.add_snps(my_snps, seq, snp_tooltips, x)
			this.update_snps(x)
		}

		
		// Add brush for zoom selection
		this.brush = d3.brushX()                 // Add the brush feature using the d3.brush function
			.extent( [ [0,0], [this.WIDTH, this.HEIGHT] ] ) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
			.on("end", this.updateChart) // Each time the brush selection changes, trigger the 'updateChart' function
		this.plot
			.append("g")
			  .attr("class", "brush")
			  .call(this.brush);
		
		// Save this instance of ZChart so an event handler can get to it later
		ZChart.allInstances[this.figID] = this;
		return this
	}
 
  
	// NB: This is called as a static method, NOT as the method of a particular object instance.
	//     So we don't know which ZFigure (or child class) instance is the correct one.
	//     So we have to recover it using the "figID" attribute of the SVG element which we set earlier.
	updateChart(event) {
		function scaleBandInvert(scale) {
			let domain = scale.domain();
			let paddingOuter = scale(domain[0]);
			let eachBand = scale.step();
			return function (value) {
			  let index = Math.floor(((value - paddingOuter) / eachBand));
			  return domain[Math.max(0, Math.min(index, domain.length-1))];
			}
		}
	
		// A quick and dirty function to generate a sequence of integers, because of course JavaScript doesn't have that
		const range = ([min, max]) => Array.from({ length: max - min + 1 }, (_, i) => min + i);

		// Recover the figID of the plot object related to this brush event
		// (we saved it as an attribute to its svg element)
		const figID = this.closest('svg').getAttribute('figID');
		let fig = ZChart.allInstances[figID];

		const extent = event.selection;
		let domainArray, domainBounds;
		
		// If no selection, back to initial coordinate. Otherwise, update X axis domain
		if(extent == null) {
		  // if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
		  	domainArray = fig.data.map(d => d.resid);
		  	domainBounds = [Math.min(...domainArray), Math.max(...domainArray)];
		} else {
		  	domainBounds = [scaleBandInvert(fig.x)(extent[0]), scaleBandInvert(fig.x)(extent[1])];
		  	domainArray = range(domainBounds);
			// Remove the grey brush area as soon as the selection has been done
		  	fig.plot.select(".brush").call(fig.brush.move, null);
		}

		// Synchronize all the zooming in all the plots
		Object.values(ZChart.allInstances).forEach(fig => fig.do_zoom(fig.data, extent, domainBounds, domainArray, fig.xAxis, fig.WIDTH, 1000));			

	}
	

	do_zoom(data, extent, domain, arrDomain, xAxis, width, timing){
		let x = this.x, y = this.y;
		x.domain(arrDomain);
		// Update axis and bar position
		this.update_bars(data, x, y);
		this.zoom_bars(data, x, y, extent, domain);

		this.update_xAxis(x);
		if(this.snps) {
			this.update_snps(x, extent, domain, width, timing);
		}

		return this;
	}
	
	add_xAxis(snps, x){
		if (snps) {
			var xaxisMargin = this.HEIGHT + 15
		} else {
			var xaxisMargin = this.HEIGHT
		}

		var num_residues = this.data.length
		
		this.xAxis = this.svg.append("g")
						.attr("transform", "translate(0," + xaxisMargin + ")")
						.style("font-size", "15px");
						
		this.update_xAxis(x)
		
		// Bars
		//Creates the "Residue" x-axis label
		if (snps) {
			var bottomMargin = this.MARGIN.bottom + 25
		} else {
			var bottomMargin = this.MARGIN.bottom
		}
		this.svg.append("text")
			.attr("x", this.WIDTH / 2)
			.attr("y", this.HEIGHT + bottomMargin)
			.style("text-anchor", "middle")
			.style("font-size", "17px")
			.text("Residue")
		
		return this
	}
	
	update_xAxis(x) {
		// Decide how many ticks to show based on how wide the domain is.
		// Actually, we are choosing the interval between ticks.
		const tickPeriod = Math.round((Math.round(x.domain().length/10))/10)*10;
		let xAxisGenerator = d3.axisBottom(x);
		let tickValues = x.domain().filter(function(d, i) {
			return !((i+1) % tickPeriod);
		});
		xAxisGenerator.tickValues(tickValues);
		// Generate tick labels from the tick values
		let seq_name_by_resid = new Array();
		// We have to create a map of resid to sequence because resid might not start at 1
		for(let i = 0; i < this.data.length; i++) {
			seq_name_by_resid[this.data[i].resid] = this.data[i].seq_name;
		}
		let tickLabels = tickValues.map((d, i) => {
			return seq_name_by_resid[d] + d; // returns e.g. "A123"
		});
		xAxisGenerator.tickFormat((d, i) => tickLabels[i]);
		// Actually call the axis generator to emit SVG elements
		this.xAxis.call(xAxisGenerator);
		return this;
	}
	
	/* add_snps
	*/
	add_snps(my_snp, my_seq, tooltip_snps, x) {
		var triangle_symbol = d3.symbol().type(d3.symbolTriangle);
		this.snps = this.plot.append('g')
			.selectAll("rect")
			.data(my_snp)
			.enter()
			.append("path")
			.attr('d', triangle_symbol)
			.attr("fill", 'black')
			.attr("transform", (d) => "translate(" + (x(d.resid) + x.bandwidth()/2) + ", 145)")
			.attr("id", "snp_triangles")
			.on("click", function(event, d){
				document.getElementById("snp_id").value = d.resid;
				document.getElementById("residue_type").value = d.alternativeSequence;
				document.getElementById("mutatebox").click();
				if (document.getElementById("mutatebox").checked == true){
					d3.select(this).attr("fill", "red");
				}
			})
			.on("mouseover", function(event, d) {
				if (document.getElementById("mutatebox").checked == false) {
					d3.select(this).attr("fill", "red")
					var mutatecheckbox = document.getElementById("mutatebox")
					mutatecheckbox.addEventListener('change', function(){
						if (mutatecheckbox.checked == false) {
							d3.selectAll("#snp_triangles").attr("fill", "black")
						}
					});
				}
				tooltip_snps.transition()
					.on("start", () => tooltip_snps.style("display", "block"))
					.duration(100)
					.style("opacity", 0.9);
				tooltip_snps.html(`<a href="${d.xrefs.url}" target="_blank">${d.xrefs.id}</a>, ${my_seq[d.resid-1]}${d.resid}${d.alternativeSequence}`)
					.style("left", (event.pageX) + 10 + "px")
					.style("top", (event.pageY - 28) + "px");
			})
			.on("mouseout", function(event, d) {
				if (document.getElementById("mutatebox").checked == false) {
					d3.select(this).attr("fill", "black")
				};
				tooltip_snps.transition()
					.duration(2000)
					.style("opacity", 0)
					.on("end", () => tooltip_snps.style("display", "none"));
			});

		return this;
	}
	
	update_snps(x, extent, domain, width, timing=1000){
		this.snps.transition()
			.duration(timing)
			.attr("transform", function(d){
				if(extent && d.resid>domain[1]){
					var translation = ("translate("+ 2*width+", 145)")
				}else if(extent && d.resid<domain[0]){
					var translation = ("translate(" + -width + ", 145)");
				}else{
					var translation = ("translate(" + (x(d.resid) + x.bandwidth()/2) + ", 145)");
				}
				return translation
			});
		
		return this
	}
}

class ZHydropathy extends ZChart{
	constructor(figID, data, snps, seq, snp_tooltips, cutoff_init=0.4) {
		super(figID, data, snps, seq, snp_tooltips)
		
		// Add Y axis			
		this.svg.append("g")
			.call(d3.axisLeft(this.y));
			
		//Creates the "Mean Hydropathy" y-axis label for Smoothed hydropathy per residue
		this.svg.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("x", 0 - (this.HEIGHT / 2))
			.attr("y", this.MARGIN.left - 80)
			.attr("transform", "rotate(-90)")
			.text("Mean Hydropathy");
			
		this.add_cutoff_line(cutoff_init)
		this.update_bars(data, this.x, this.y);
		
		return this
	}
	
	update_bars(data, x=this.x, y=this.y, timing=1000) {
		this.data = data;
		this.bars.data(data);
		//console.log(this.bars.data())
		this.update_xAxis(x); // because there might have been a mutation
		this.bars.transition()
			.duration(timing)
			.attr("y", d => y(d.hydropathy_3_window_mean))
			.attr("fill", "grey")
			.attr("height", d => this.HEIGHT - y(d.hydropathy_3_window_mean));

		return this;
	}
	
	add_cutoff_line(my_cut=0.4, x=this.x, y=this.y) {
		this.cut_line = this.plot.append('g')
			.append("line")
			.attr("fill", "none")
			.attr("stroke", "steelblue")
			.attr("stroke-width", 1.5)
			.attr("x1", 0)
			.attr("x2", this.WIDTH)
			.attr("y1", y(my_cut))
			.attr("y2", y(my_cut))

		return this;
	}
	
	update_cutoff_line(my_cut, x=this.x, y=this.y) {
		this.cut_line
			.transition()
			.duration(1000)
			.attr("y2", y(my_cut))
			.attr("y1", y(my_cut));

		return this;
	}
	
	zoom_bars(data, x, y, extent, domain, timing=1000){
		var width = this.WIDTH
		this.bars
		  .transition().duration(timing)
		  .attr("x", function (d) { 
			if(extent && d.resid>domain[1]){
				return 2*width
			}else if(extent && d.resid<domain[0]){
				return -width;
			}else{
				return x(d.resid); 
			}
		  })
		  .attr("y", function (d) { return y(d.hydropathy_3_window_mean); } )
		  .attr("width", x.bandwidth());
	}
	
}

class ZblobChart extends ZChart {
	constructor(figID, data, snps, seq, snp_tooltips, num_residues) {
		super(figID, data, snps, seq, snp_tooltips, num_residues);
		this.add_psh_ylabel();
		this.update_bars(data);
		this.add_skyline(data, this.x, this.y);
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
			.attr("y", this.HEIGHT-22)
			.attr("x", this.MARGIN.left-65)
			.attr("transform", "rotate(0)")
			.style("font-size", "17px")
			.text("p");

		var ylabel = this.svg.append("g").attr("id", "ylabel")
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("y", this.HEIGHT - 50.25)
			.attr("x", this.MARGIN.left - 65)
			.attr("transform", "rotate(0)")
			.style("font-size", "17px")
			.text("s");


		//"h" blob y-axis label for globular tendency plot
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("y", this.HEIGHT - 78.5)
			.attr("x", this.MARGIN.left - 65)
			.attr("transform", "rotate(0)")
			.style("font-size", "17px")
			.text("h");

		//"SNPs" y-axis label for globular tendency plot

		return this;
	}
	
	update_bars(data, timing=1000, x=this.x, y=this.y) {
		this.data = data;
		this.bars.data(data);

		// Lookup table for color attribute of our data as a function of the plot name.
		// E.g. The "globPlot" plot data stores colors in the "P_diagram" attribute of the data.
		const figID_to_var = {'ZblobPlot': 'blob_color', 'blobPlot': 'blob_color', 'globPlot': 'P_diagram', 'ncprPlot': 'NCPR_color', 'richPlot': 'h_blob_enrichment',
			'uverskyPlot': 'uversky_color', 'disorderPlot': 'disorder_color'};

		this.update_xAxis(x); // because there migh have been a mutation
		this.bars.transition()
			.duration(timing)
			.attr("y", (d) => y(d.domain_to_numbers))
			.attr("height", (d) => this.HEIGHT - y(d.domain_to_numbers))
			.attr("fill", (d) => d[figID_to_var[this.figID]]);
		
		// Update/add the corresponding skyline, in a potentially ugly way
		this.add_skyline(data);
		
		return this;
	}
	
	add_skyline(data) {
		var x = this.x;
		var y = this.y;
		var domain = [x.domain()[0], x.domain()[x.domain().length-1]];
		data = data.slice(domain[0]-1,domain[1]);

		// Do we already have a skyline? Remove it, since it might not be correct
		this.svg.selectAll('.skyline').remove();
		if(this.skyline !== undefined) {
			this.skyline = undefined;
		}

		// We should have at least two data points to draw a line
		if(data.length < 2) {
			return;
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

		// Last line segment - add an extraneous data point to signify this
		const last_resid = data[data.length-1].resid;
		points.push({resid: last_resid,
			height: data[data.length-1].domain_to_numbers});

		this.skyline = this.svg.append('g').classed('skyline', true);
		this.skyline.append("path")
			.attr("class", "mypath")
			.datum(points)
			.attr("fill", "none")
			.attr("stroke", "grey")
			.attr("stroke-width", 1.0)
			.attr("d", d3.line()
				.x(function (d, index) {
					// Extend the final line segment all the way to the right,
					// if we are on that last extraneous data point
					if(index == (points.length-1)) {
						return x(d.resid) + x.bandwidth();
					} else {
						return x(d.resid);
					}
				})
				.y((d) => y(d.height)));

		return this;
	}
	
	/* add_BlobLegend
	FUNCTION: add_BlobLegend
	SHORT DESCRIPTION: add the discrete legend for the globular tendencies graph
	INPUTS:
		svg - a container containing an graph modified by the function itself
	RETURNS:
		none
	*/
	add_BlobLegend(keysize=20, offset=20) {
		//This section contains the key that appears next to the Blob types colored plot
		//squares for the key
		var legend = this.svg.append("g").attr("id", "legend")

		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 5)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#0071BC")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 35)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#F7931E")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 65)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#2DB11A")
				
		//Text that appears to the right of the key    
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 15).text("Hydrophobic blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 45).text("Hydrophilic blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 75).text("Short blob").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		return this;
	}
	
	zoom_bars(data, x, y, extent, domain, timing=1000){
		var width = this.WIDTH
		this.bars
		  .transition().duration(timing)
		  .attr("x", function (d) { 
			if(extent && d.resid>domain[1]){
				return 2*width
			}else if(extent && d.resid<domain[0]){
				return -width;
			}else{
				return x(d.resid); 
			}
		  })
		  .attr("width", x.bandwidth());
		this.add_skyline(data, x, y)
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
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top - 25)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#0f0")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 5)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#FEE882")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 35)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#BF72D2")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 65)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#f00")
		legend.append("rect")
			.attr("x", this.WIDTH + offset)
			.attr("y", this.MARGIN.top + 95)
			.attr('width', keysize)
			.attr('height', keysize)
			.style("fill", "#00f")
				
		//Text that appears to the right of the key    
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top - 15).text("Globular").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 15).text("Janus/Boundary").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 45).text("Strong Polyelectrolyte").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 75).text("Strong Polyanion (-)").style("font-size", "15px")
			.attr("alignment-baseline", "middle")
		legend.append("text")
			.attr("x", this.WIDTH + 50)
			.attr("y", this.MARGIN.top + 105).text("Strong Polycation (+)").style("font-size", "15px")
			.attr("alignment-baseline", "middle")

		return this;
	}

	add_ContinuousLegend(cmap, {min='-1', med='0', max='+1', width=20, height=80}={min: '-1', med: '0', max: '+1', width: 20, height: 80}) {
		switch(cmap) {
			case "PuOr":
				this.add_colorbar("PuOr", width, height, min, max, this.WIDTH, this.HEIGHT,
					{ med: med, cend: '#7f3b08', cq3: '#ee9d3c', cmid: '#f6f6f7', ctop: '#2d004b' });
				break;
			case "OrPu":
				this.add_colorbar("OrPU", width, height, min, max, this.WIDTH, this.HEIGHT,
					{ med: med, cend: '#2d004b', cmid: '#f6f6f7', cq1: '#ee9d3c', ctop: '#7f3b08' });
				break;
			case "RWB":
				//Color bar key to the right of the enrichment plot.
				this.add_colorbar("RWB", width, height, min, max, this.WIDTH, this.HEIGHT,
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

}



