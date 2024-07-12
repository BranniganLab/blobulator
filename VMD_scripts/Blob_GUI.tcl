source blobulation.tcl
if [winfo exists .blob] {
	wm deiconify $::blobulator::blobs
	return
}

namespace eval ::blobulator {
	variable buttonWidth 54
	variable defaultButtonWidth 7
	variable dropDownMenuWidth 14 
	variable isFirst 0
	variable blobColorType1 "Blob Type"
	variable blobColorType2 "Blob ID"
	variable hydropathyScale1 "Kyte-Doolittle"
	variable hydropathyScale2 "Eisenberg-Weiss"
	variable hydropathyScale3 "Moon-Fleming"
	variable graphRepOptions "Blob ID"
	variable Lmin 4
	variable H .4
	variable MolID 
	variable checkForUpdate
	variable hydropathyScaleDictionaryList "Kyte-Doolittle"

	} 

proc ::blobulator::Window {} {
variable blobs [toplevel ".blob"]
	wm title $::blobulator::blobs "Blobulator"
	wm resizable $::blobulator::blobs 0 0
	wm attributes $::blobulator::blobs -alpha 1;
	wm attributes $::blobulator::blobs -fullscreen 0
}
proc ::blobulator::GUI {} {
	::blobulator::Window
	grid [label $::blobulator::blobs.1_MolID -text MolID ]
	grid [entry $::blobulator::blobs.tv_MolID -width 10 -textvariable ::blobulator::MolID ] -row 0 -column 1
	if {$::blobulator::MolID == ""} {
		set ::blobulator::MolID "top"
	}
	set paraList [list Lmin ::blobulator::Lmin 1 50 1 H ::blobulator::H .1 1 .01]
	foreach { entry variableName min max interval} $paraList {
		set w1 [label $::blobulator::blobs.l_$entry -text $entry]
		set w2 [entry $::blobulator::blobs.e_$entry -width 10 -textvariable $variableName]
		set w3 [scale $::blobulator::blobs.s_$entry -orient horizontal -from $min -to $max -length 175 -resolution $interval -tickinterval 0 -variable $variableName -showvalue 0]
		
		
		grid $w1 $w2 $w3 	
	}
	grid [label $::blobulator::blobs.t -text "Blobulate by: " -height 2] -row 4 -column 0 -columnspan 2 -sticky e
	grid [ttk::combobox $::blobulator::blobs.dmnu -textvariable ::blobulator::graphRepOptions -width $::blobulator::dropDownMenuWidth -values [list $::blobulator::blobColorType1 $::blobulator::blobColorType2] -state readonly ] -pady 6 -row 4 -column 2 -sticky w
	grid [label $::blobulator::blobs.t2 -text "hydropathy Scale : " -height 2] -row 5 -column 0 -columnspan 2 -sticky e
	grid [checkbutton $::blobulator::blobs.check -text "Auto Update" -variable ::blobulator::checkForUpdate -command {::blobulator::blobulationSlider }] -row 5 -column 2 -sticky e
	grid [ttk::combobox $::blobulator::blobs.dmnu2  -textvariable ::blobulator::hydropathyScaleDictionaryList -width $::blobulator::dropDownMenuWidth -values [list $::blobulator::hydropathyScale1 $::blobulator::hydropathyScale2 $::blobulator::hydropathyScale3] -state readonly] -pady 6 -row 5 -column 2 -sticky w
	grid [button $::blobulator::blobs.blobulate -text "Blobulate!" -font [list arial 9 bold] -width $::blobulator::buttonWidth -command {blobulation } ] -columnspan 5
	grid [button $::blobulator::blobs.ldefault -text "Default" -width $::blobulator::defaultButtonWidth -command {::blobulator::lminDefault }] -padx 0 -row 1 -columnspan 1 -column 4
	grid [button $::blobulator::blobs.hdefault -text "Default" -width $::blobulator::defaultButtonWidth -command {::blobulator::hDefault }] -padx 0 -row 2 -columnspan 1 -column 4
	grid [button $::blobulator::blobs.clear -text "Clear representations" -width $::blobulator::buttonWidth -command {::blobulator::blobClear $::blobulator::MolID}] -column 0 -columnspan 5
}
# 
#	Checks radiobutton value so blobulate properly displays representations
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#
#	Global Arguments:
#	::blobulator::graphRepOptions (List): A list of graph representation options, decided which graphuser proc called depending on what the variable is set to
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
#	::blobulator::blobColorType1 (String): A parameter used for ::blobulator::graphRepOptions checks, if it is set to this variable, will call ::blobulator::graphRepUser proc
#	::blobulator::blobColorType2 (String): A parameter used for ::blobulator::graphRepOptions checks, if it is set to this variable, will call ::blobulator::graphRepUser2 proc
#	blobs (Object): Overarching window frame
proc blobulation {} {
	
	set ::blobulator::isFirst 1
	
	bind $::blobulator::blobs.s_Lmin <ButtonRelease> {::blobulator::blobulationSlider } 
	bind $::blobulator::blobs.s_H <ButtonRelease> {::blobulator::blobulationSlider } 
	bind $::blobulator::blobs.dmnu <<ComboboxSelected>> {::blobulator::blobulationSlider }
	bind $::blobulator::blobs.dmnu2 <<ComboboxSelected>> {hydropathyScaleDropDownMenu }
	if {$::blobulator::graphRepOptions == $::blobulator::blobColorType1} {
		blobulate $::blobulator::MolID $::blobulator::Lmin $::blobulator::H $::blobulator::hydropathyScaleDictionaryList
		::blobulator::graphRepUser 
	} elseif { $::blobulator::graphRepOptions == $::blobulator::blobColorType2} {
		blobulate $::blobulator::MolID $::blobulator::Lmin $::blobulator::H $::blobulator::hydropathyScaleDictionaryList
		::blobulator::graphRepUser2 
	} else {
		puts "no value"
	}
return
}


#
#	Runs blobulation when any slider is moved
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#	
#	Global Arguments:
#	::blobulator::graphRepOptions (List): A list of graph representation options, decided which graphuser proc called depending on what the variable is set to
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
#	::blobulator::blobColorType1 (String): A parameter used for ::blobulator::graphRepOptions checks, if it is set to this variable, will call ::blobulator::graphRepUser proc
#	::blobulator::blobColorType2 (String): A parameter used for ::blobulator::graphRepOptions checks, if it is set to this variable, will call ::blobulator::graphRepUser2 proc
proc ::blobulator::blobulationSlider {} {
	if {$::blobulator::isFirst == 1} {

		if {$::blobulator::graphRepOptions == $::blobulator::blobColorType1} {
			blobulate $::blobulator::MolID $::blobulator::Lmin $::blobulator::H $::blobulator::hydropathyScaleDictionaryList 
			::blobulator::graphRepUser 
		} elseif {$::blobulator::graphRepOptions == $::blobulator::blobColorType2} {
			blobulate $::blobulator::MolID $::blobulator::Lmin $::blobulator::H $::blobulator::hydropathyScaleDictionaryList
			::blobulator::graphRepUser2 

		} else {
			puts "no value"
		}
	} else {
		return 
	} 
return
}

#
#	Creates parameters for when the second drop down menu is changed  
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#
#	Global Arguments:
#	checkForUpdate (Integer): A number that switches to 1 if the checkbox is active and 0 when the checkbox is inactive
proc hydropathyScaleDropDownMenu {} {
	
	if {$::blobulator::checkForUpdate == 1} {
		::blobulator::hDefault
	} else {
		::blobulator::blobulationSlider
	}
return
}

#
#	Set Lmin variable to default value, currently 4
#
#	Global Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
proc ::blobulator::lminDefault {} {
	
	set ::blobulator::Lmin 4
	::blobulator::blobulationSlider 
return
}

#
#	Sets H variable to default value based on dictionary 
#
#	Global Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
#	hydropathyScaleDictionaryList (List): List of names that the drop down menu contains, each name calls a dictionary for normalized hydropathy scale values
#	checkForUpdate (Integer): A number that switches to 1 if the checkbox is active and 0 when the checkbox is inactive
#	blobs (Object): Overarching window frame
proc ::blobulator::hDefault {} {
	
	
	if {$::blobulator::hydropathyScaleDictionaryList == "Kyte-Doolittle"} {
		set ::blobulator::H .4
	}

	if {$::blobulator::hydropathyScaleDictionaryList == "Eisenberg-Weiss"} {
		set ::blobulator::H .28
	}
	if {$::blobulator::hydropathyScaleDictionaryList == "Moon-Fleming"} {
		set ::blobulator::H .35
	}

	::blobulator::blobulationSlider 

	return
}

#
#	Runs graphical representations showing hblobs in QuickSurf, p and s blobs in NewCartoon
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
proc ::blobulator::graphRepUser {} { 
	
	set range [molinfo $::blobulator::MolID get numreps]
	for {set i 0} { $i < $range } {incr i} {
		mol delrep 0 $::blobulator::MolID
	}  
	set count 0

	set sel [atomselect $::blobulator::MolID protein]
	set user2length [lsort -unique [$sel get user2]]
	$sel delete
	foreach u2 $user2length {

		mol representation QuickSurf 1.21 1 .5 2
		mol material AOChalky
		mol color ColorID 23
		
		

		mol addrep $::blobulator::MolID 
		mol modselect $count $::blobulator::MolID "user 1 and user2 $u2"
		
		incr count 
	}
	

	mol representation NewCartoon .3 20
	mol color ColorID 7
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 2"
	incr count

	mol representation NewCartoon .3 20 
	mol color ColorID 3
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 3"
	incr count

	mol representation NewCartoon .3 20 
	mol color ColorID 23
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 1"
	incr count
return 
}

#
#	Runs graphical representations showing hblobs in QuickSurf (by blob grouping), p and s blobs in NewCartoon
#
#
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#	lMin (Integer): An integers greater than 1 and less then the legnth of the sequence that determines the minimum length of hblobs
# 	H (Float): A float that determines the hydropathy threshold, this determines how hydrophobic something needs to be to be counted
#	for an h blob
proc ::blobulator::graphRepUser2 {} {
	
	set range [molinfo $::blobulator::MolID get numreps]
	for {set i 0} {$i < $range} {incr i} {
		mol delrep 0 $::blobulator::MolID
	}   
	set count 0
	set sel [atomselect $::blobulator::MolID protein]
	set user2length [lsort -unique [$sel get user2]]
	$sel delete
	foreach u2 $user2length {

		mol representation QuickSurf 1.21 1 .5 2
		mol material AOChalky
		mol color user2
		
		

		mol addrep $::blobulator::MolID 
		mol modselect $count $::blobulator::MolID "user 1 and user2 $u2"
		
		incr count 
	}
	
	
	
	mol representation NewCartoon .3 20
	mol color ColorID 7
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 2"
	incr count 
	
	mol representation NewCartoon .3 20 
	mol color ColorID 3
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 3"
	incr count 

	mol representation NewCartoon .3 20 
	mol color user2
	mol addrep $::blobulator::MolID 
	mol modselect $count $::blobulator::MolID "user 1"
	incr count
	colorScale
return
}


#
#	Program removes all graphical representations
# 
#	Arguments:
#	MolID (Integer): An integer that assigns what protein the algorithm looks for 
#
#	Global Arguments:
#	isFirst (Integer): A number that swtiches to 1 when the blobulation proc has been called and 0 when blobulation hasnn't been called
proc ::blobulator::blobClear {MolID} {
	global isFirst
	set isFirst 0
	set range [molinfo $::blobulator::MolID get numreps]
		for {set i 0} {$i < $range} {incr i} {
			mol delrep 0 $::blobulator::MolID
		} 
return 
	}
	
#
#	Program the destroys the GUI window
#
proc ::blobulator::blobQuit {} {
	destroy .blob
return
}

#
#	Function that creates a gradient from each point using the slope function
#
#	Arguments:
# 	PointA (Integer): Starting value used to start i at the desired color num
#	PointB (Integer): Ending value used to end the iteration to 
#	ColorA (List): List of color values, start point that increments up to the end point
# 	ColorB (List): List of color values, end point 
proc ::blobulator::tricolor_scale {PointA PointB ColorA ColorB} {
	#replaces the rgb colorscale with a custom one
	#sets the color explicitly at three intermediate color anchors (511, 660, 1000) 
	#adds a linear gradient between the anchors 
	set color_start [colorinfo num]
	display update off

	for {set i $PointA} {$i < $PointB} {incr i} {

		set deltaPoint [expr $PointB - $PointA]
		set colorList {}
		foreach pa $ColorA pb $ColorB {
			set deltaColor [expr $pb - $pa]

			set color [expr [expr $deltaColor / $deltaPoint] * [expr $i - $PointA] + $pa]
			lappend colorList $color
		}

		color change rgb [expr $i + $color_start] [lindex $colorList 0] [lindex $colorList 1] [lindex $colorList 2]
	}
	display update on
return
}

#
#	Program that sets colorscale to be inline with blobulation colorscheme, creates a gradient 
#
#	Arguments:
# 	PointA (Integer): Starting value used to start i at the desired color num
#	PointB (Integer): Ending value used to end the iteration to 
#	ColorA (List): List of color values, start point that increments up to the end point
# 	ColorB (List): List of color values, end point 
proc ::blobulator::colorScale {{pointA 0} {pointB 205} {pointC 410} {pointD 615} {pointE 820} {pointF 1024} {colorA "0.0 0.5 0.5"} {colorB "0.4 1.0 1.0"} {colorC "0.0 0.3 0.6"} {colorD "0.4 0.7 1.0"} {colorE "0.0 0.0 0.6"} {colorF "0.2 0.2 1.0"}} {
	::blobulator::tricolor_scale $pointA $pointB $colorA $colorB
	::blobulator::tricolor_scale $pointB $pointC $colorB $colorC
	::blobulator::tricolor_scale $pointC $pointD $colorC $colorD
	::blobulator::tricolor_scale $pointD $pointE $colorD $colorE
	::blobulator::tricolor_scale $pointE $pointF $colorE $colorF
return
}

#  proc ::blobulator::registerMenu {} {
#  	set already_registered 0
#  	if {$already_registered==0} {
#  		incr already_registered
#  		vmd_install_extension blobulatorVMDGUI ::blobulator::GUI "Visualization/Blobulator"
#  	}
# }
::blobulator::GUI