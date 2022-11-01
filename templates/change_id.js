var entry_box = document.getElementById("uniprot_id");
var chosen_input = document.getElementByID("input_type");

entry_box.addEventListener('change', function() {
	if (chosen_input.value == "uniprot_id") {
		entry_box.innerHTML = "P37840";
	} else if (chosen_input.value == "ensembl_id") {
		entry_box.innerHTML = "ENSG00000145335";
	}
})