//FUNCTION DECLARATIONS



// A function that updates the charts
function update_Charts(figs, data) {
	figs.pathyFig.update_cutoff_line(d3.select("#cutoff_user").text());

	//iterate over all figures in figs and update them
	for (let [key, value] of Object.entries(figs)) { 
		try {
			value.update_bars(data);
		}
		catch {

			console.log("Failed to update: " + key)
		}
	}
}

// Update the output when parameters are changed
function do_update(figs, data) {
	let my_seq = {{ my_seq | safe }};
	// If the box is checked, I mutate the amino acid
	if(d3.select("#mutatebox").property("checked")){
		const snp_id = document.getElementById("snp_id").value;
		const amino_acid = document.getElementById("residue_type").value;
		my_seq = my_seq.slice(0, snp_id-1) + amino_acid + my_seq.substr(snp_id, my_seq.length);
	} 

	const d_value = d3.select("#domain_threshold_user").text();
	const selectedValue = d3.select("#cutoff_user").text();
	const m_str = {my_seq: my_seq, domain_threshold: d_value, cutoff: selectedValue, my_disorder: {{ my_disorder | tojson | safe }}};

	$.post( "/postmethod", m_str , "json")
		.then(function(data) {
			var data_tmp = data.chart_data;
			var tt = JSON.stringify(eval("(" + data_tmp + ")"));
			var data_obj = JSON.parse(tt);
			update_Charts(figs, data_obj);
		});
}

function draw(data) {
	const my_snp = {{ my_snp | safe }};
	const my_seq = {{ my_seq | safe }};
	const my_disorder = {{ my_disorder | tojson | safe }};
	const domain_threshold_max = {{ domain_threshold_max | safe }};
	if (my_disorder == "0") {
		var snps = false
	} else {
		var snps = true
	}
	let figs = [];
	figs.pathyFig = new Figure("pathyPlot", data)
		.add_title("Smoothed hydropathy per residue")
		.add_tooltip(hydropathy_tool_text)
		.add_pathy_ylabel()
		.add_cutoff_line({{ my_cut | safe }})
		.build_barChart(domain_threshold_max, snps)
		.add_yAxis()
		.add_snps(my_snp, my_seq, Tooltip_snps);

	figs.blobFig = new Figure("blobPlot", data)
		.add_title("Blobs colored according to blob type")
		.build_barChart(domain_threshold_max, snps)
		.add_BlobLegend()
		.add_snps(my_snp, my_seq, Tooltip_snps)
		.add_psh_ylabel()
		.add_skyline();
	
	figs.globFig = new Figure("globPlot", data)
		.add_title("Blobs colored according to globular tendency (Das-Pappu Phase)")
		.add_tooltip(Das_Pappu_text)
		.add_GlobularLegend()
		.build_barChart(domain_threshold_max, snps)
		.add_snps(my_snp, my_seq, Tooltip_snps)
		.add_psh_ylabel()
		.add_skyline();

	figs.ncprFig = new Figure("ncprPlot", data)
		.add_title("Blobs colored according to net charge per residue")
		.add_tooltip(ncpr_tool_text)
		.add_ContinuousLegend("RWB", {min: "-0.5", med: "0.0", max: "+0.5"})
		.build_barChart(domain_threshold_max, snps)
		.add_snps(my_snp, my_seq, Tooltip_snps)
		.add_psh_ylabel()
		.add_skyline();

	figs.richFig = new Figure("richPlot", data)
		.add_title("Blobs colored according to estimated mutation sensitivity")
		.add_tooltip(enrichment_tool_text)
		.add_ContinuousLegend("RWB", {min: "0.5", med: "1.0", max: "2.0"})
		.build_barChart(domain_threshold_max, snps)
		.add_snps(my_snp, my_seq, Tooltip_snps)
		.add_psh_ylabel()
		.add_skyline()

	figs.uverskyFig = new Figure("uverskyPlot", data)
		.add_title("Blobs colored according to distance from Uversky-Gillespie-Fink boundary")
		.add_tooltip(uversky_tool_text)
		.add_ContinuousLegend("PuOr", {min: "-0.65", med: "0.05", max: "0.73"})
		.build_barChart(domain_threshold_max, snps)
		.add_snps(my_snp, my_seq, Tooltip_snps)
		.add_psh_ylabel()
		.add_skyline();

	if (my_disorder == "0") {
		figs.disorderFig = new Figure("disorderPlot", data)
			.add_title("DISORDER UNAVAILABLE")
			.add_tooltip("Disorder information is acquired from Uniprot. To see the disorder plot, please provide the Uniprot ID on the previous page.");
	} else {
		figs.disorderFig = new Figure("disorderPlot", data)
			.add_title("Blobs colored according to disordered fraction")
			.add_tooltip(disorder_tool_text)
			.add_ContinuousLegend("PuOr", {min: "0.0", med: "0.5", max: "1.0"})
			.build_barChart(domain_threshold_max, snps)
			.add_snps(my_snp, my_seq, Tooltip_snps)
			.add_psh_ylabel()
			.add_skyline();
	}

	var str_i = "Download plots!";
	var str_j = "Download data!";

	// Set up UI element change handler
	d3.selectAll("#mutatebox,#snp_id,#residue_type,#domain_threshold_user_box,#domain_threshold_user_slider,#cutoff_user_box,#cutoff_user_slider,.checkbox").on("change", function(){do_update(figs, data)});
	

	//download_data
	d3.select('#download_data_link').on('click', function() {
		// If the box is check, I mutate the amino acid
		// TODO: This code should not be duplicated
		var my_seq = {{ my_seq | safe }};
		if(d3.select("#mutatebox").property("checked")) {
			var snp_id = document.getElementById("snp_id").value;
			var amino_acid = document.getElementById("residue_type").value;
			my_seq = my_seq.slice(0, snp_id-1) + amino_acid + my_seq.substr(snp_id, my_seq.length);
		}

		$.ajax({
			url: "/json",
			type: "post",
			data: {my_seq: my_seq, domain_threshold: d3.select("#domain_threshold_user").text(), cutoff: d3.select("#cutoff_user").text(), my_disorder:my_disorder},
			xhrFields: {responseType: 'blob'},
			success: function(data) {
				var a = document.createElement('a');
				var url = window.URL.createObjectURL(data);
				let name = {{ my_uni_id | safe }};
				a.href = url;
				a.download = name + '_blobulated.csv';
				document.body.append(a);
				a.click();
				a.remove();
				window.URL.revokeObjectURL(url);
			}
		});
	});  
}