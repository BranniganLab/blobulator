class barChart extends Figure {
	constructor(figID, data, snps, seq, snp_tooltips) {
		super(figID, data);
		build_barChart(snps.length())
		if (snps) {
			add_snps(snps, seq, snp_tooltips)
		}
	}

	
	/* add_snps
	*/
	add_snps(my_snp, my_seq, tooltip_snps, x=this.x, y=this.y) {
		var arc = d3.symbol().type(d3.symbolTriangle);
		this.svg.append('g')
			.selectAll("rect")
			.data(my_snp)
			.enter()
			.append("path")
			.attr('d', arc)
			.attr("transform", (d) => "translate(" + (x(d.resid) + x.bandwidth()/2) + ", 145)")
			.attr("fill", 'black')
			.on("click", function(event, d) {
				//window.location.href = d.xrefs[0].url+'_blank'
				window.open(d.xrefs.url, '_blank')
			})
			.on("mouseover", function(event, d) {
				d3.select(this)
					.attr("fill", "red");
				tooltip_snps.transition()
					.on("start", () => tooltip_snps.style("display", "block"))
					.duration(100)
					.style("opacity", 0.9);
				tooltip_snps.html(`<a href="${d.xrefs.url}" target="_blank">${d.xrefs.id}</a>, ${my_seq[d.resid-1]}${d.resid}${d.alternativeSequence}`)
					.style("left", (event.pageX) + 10 + "px")
					.style("top", (event.pageY - 28) + "px");
			})
			.on("mouseout", function(event, d) {
				d3.select(this).attr("fill", "black");
				tooltip_snps.transition()
					.duration(2000)
					.style("opacity", 0)
					.on("end", () => tooltip_snps.style("display", "none"));
			});

		return this;
	}
	
	build_barChart(snps=0, timing=0, x=this.x, y=this.y) {
		// Add a clipPath: everything out of this area won't be drawn.
		this.clip = this.svg.append("defs").append("svg:clipPath")
			.attr("id", "clip")
			.append("svg:rect")
			.attr("width", this.GLOBAL_WIDTH )
			.attr("height", this.GLOBAL_HEIGHT )
			.attr("x", 0)
			.attr("y", 0);
		
		this.bars = this.svg.selectAll("bars")
			.data(this.data)
			.join("rect")
			.attr("id", "barChart"+this.figID)
			.attr("clip-path", "url(#clip)")
			.attr("width", x.bandwidth())
			.attr("x", (d) => x(d.resid))
			.attr("y", this.GLOBAL_HEIGHT);
			
		this.update_bars(this.data, timing);
		this.add_xAxis(snps)
		
		return this;
	}
	
	add_xAxis(snps=0, x=this.x, y=this.y){
		if (snps) {
			var xaxisMargin = this.GLOBAL_HEIGHT + 15
		} else {
			var xaxisMargin = this.GLOBAL_HEIGHT
		}
		num_residues = this.data.length()
		this.xAxis = this.svg.append("g")
						.call(d3.axisBottom(x).tickValues(x.domain().filter(function(d, i) { return !((i+1) % 
						   (Math.round((Math.round(num_residues/10))/10)*10) )})))
						.attr("transform", "translate(0," + xaxisMargin + ")");
		
		// Bars
		//Creates the "Residue" x-axis label
		if (snps) {
			var bottomMargin = this.MARGIN.bottom + 25
		} else {
			var bottomMargin = this.MARGIN.bottom
		}
		this.svg.append("text")
			.attr("x", this.GLOBAL_WIDTH / 2)
			.attr("y", this.GLOBAL_HEIGHT + bottomMargin)
			.style("text-anchor", "middle")
			.text("Residue")

		return this
	}

}

class blobChart extends barChart {
	constructor(figID, data, snps, seq, snp_tooltips, num_residues) {
		super(figID, data, snps, seq, snp_tooltips, num_residues);
		add_psh_ylabel();
		update_bars();
		add_skyline();
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
			.attr("y", this.GLOBAL_HEIGHT-5)
			.attr("x", this.MARGIN.left-80)
			.attr("transform", "rotate(0)")
			.text("p");

		var ylabel = this.svg.append("g").attr("id", "ylabel")
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("y", this.GLOBAL_HEIGHT - 37.5)
			.attr("x", this.MARGIN.left - 80)
			.attr("transform", "rotate(0)")
			.text("s");


		//"h" blob y-axis label for globular tendency plot
		ylabel.append("text")
			.attr("class", "y label")
			.attr("text-anchor", "middle")
			.attr("y", this.GLOBAL_HEIGHT - 70)
			.attr("x", this.MARGIN.left - 80)
			.attr("transform", "rotate(0)")
			.text("h");

		//"SNPs" y-axis label for globular tendency plot

		return this;
	}
	
	update_bars(data=this.data, timing=1000, x=this.x, y=this.y) {
		this.data = data;
		this.bars.data(data);
		
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

class hydropathyPlot extends barChart {
	constructor(figID, data, snps, seq, snp_tooltips, cutoff_init=0.4) {
		super(figID, data, snps, seq, snp_tooltips);
		add_cutoff_line(cutoff_init);
		add_hydropathy_bars();
		add_yAxis();
		add_pathy_ylabel();
		update_bars();
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

	add_yAxis() {
		this.svg.append("g") //the y axis is drawn only for plot 1
				.call(d3.axisLeft(this.y));
		return this
	}
	
	add_cutoff_line(my_cut=0.4, x=this.x, y=this.y) {
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
	
	update_bars(data=this.data, timing=1000, x=this.x, y=this.y) {
		this.data = data;
		this.bars.data(data);
		
		// The hydropathy plot requires special colors
		this.bars.transition()
			.duration(timing)
			.attr("y", (d) => y(d.hydropathy_3_window_mean))
			.attr("height", (d) => this.GLOBAL_HEIGHT - y(d.hydropathy_3_window_mean));
		this.bars.attr("fill", 'grey');

		return this;
	}
}
