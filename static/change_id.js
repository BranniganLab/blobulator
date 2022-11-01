var entry_box = document.getElementById("uniprot_id");
const chosen_input = document.getElementById("input_type");

chosen_input.addEventListener('change', function() {
	if (chosen_input.value == "uniprot_id") {
		entry_box.innerHTML = "P37840";
	} else if (chosen_input.value == "ensembl_id") {
		entry_box.innerHTML = "ENSG00000145335";
	}
})