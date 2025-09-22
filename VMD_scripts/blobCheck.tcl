source blobulation.tcl 
source normalized_hydropathyscales.tcl

#Filename needs to be csv

proc blobTest {filename molID lMin H select {dictInput "Kyte-Doolittle"} } {
	set blobulated [::blobulator::blobulateSelection $molID 4 .4 "all" $dictInput]

	puts "TCL:$blobulated"
	set file [open $filename w]
	set count 0
	puts $file "Count, BlobNum"
	foreach residue $blobulated {
		puts $file "$count, $residue"
		incr count
	}
	close $file
}

blobTest "blobTest.csv" top 4 .4 "all" 