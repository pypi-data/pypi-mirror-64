// DATA_TEMPLATE: dom_data
oTest.fnStart( "bSortClasses" );

$(document).ready( function () {
	/* Check the default */
	$('#example').dataTable();
	
	oTest.fnTest( 
		"Sorting classes are applied by default",
		null,
		function () { return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1'); }
	);
	
	oTest.fnTest( 
		"Sorting classes are applied to all required cells",
		null,
		function () { return $('#example tbody tr:eq(7) td:eq(0)').hasClass('sorting_1'); }
	);
	
	oTest.fnTest( 
		"Sorting classes are not applied to non-sorting columns",
		null,
		function () { return $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_1') == false; }
	);
	
	oTest.fnTest( 
		"Sorting multi-column - add column 1",
		function () { 
			oDispacher.click( $('#example thead th:eq(1)')[0], { 'shift': true } ); },
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2');
		}
	);
	
	oTest.fnTest( 
		"Sorting multi-column - add column 2",
		function () { 
			oDispacher.click( $('#example thead th:eq(2)')[0], { 'shift': true } ); },
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2') &&
						 $('#example tbody tr:eq(0) td:eq(2)').hasClass('sorting_3');
		}
	);
	
	oTest.fnTest( 
		"Sorting multi-column - add column 3",
		function () { 
			oDispacher.click( $('#example thead th:eq(3)')[0], { 'shift': true } );
		},
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2') &&
						 $('#example tbody tr:eq(0) td:eq(2)').hasClass('sorting_3') &&
						 $('#example tbody tr:eq(0) td:eq(3)').hasClass('sorting_3');
		}
	);
	
	oTest.fnTest( 
		"Remove sorting classes on single column sort",
		function () { 
			$('#example thead th:eq(4)').click();
		},
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') == false &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2') == false &&
						 $('#example tbody tr:eq(0) td:eq(2)').hasClass('sorting_3') == false &&
						 $('#example tbody tr:eq(0) td:eq(3)').hasClass('sorting_3') == false;
		}
	);
	
	oTest.fnTest( 
		"Sorting class 1 was added",
		null,
		function () { return $('#example tbody tr:eq(1) td:eq(4)').hasClass('sorting_1'); }
	);
	
	
	/* Check can disable */
	oTest.fnTest( 
		"Sorting classes can be disabled",
		function () {
			oSession.fnRestore();
			$('#example').dataTable( {
				"bSortClasses": false
			} );
		},
		function () { return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') == false; }
	);
	
	oTest.fnTest( 
		"Sorting classes disabled - add column 1 - no effect",
		function () { 
			oDispacher.click( $('#example thead th:eq(1)')[0], { 'shift': true } ); },
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') == false &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2') == false;
		}
	);
	
	oTest.fnTest( 
		"Sorting classes disabled - add column 2 - no effect",
		function () { 
			oDispacher.click( $('#example thead th:eq(2)')[0], { 'shift': true } ); },
		function () {
			return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1') == false &&
						 $('#example tbody tr:eq(0) td:eq(1)').hasClass('sorting_2') == false &&
						 $('#example tbody tr:eq(0) td:eq(2)').hasClass('sorting_3') == false;
		}
	);
	
	
	/* Enable makes no difference */
	oTest.fnTest( 
		"Sorting classes enabled override",
		function () {
			oSession.fnRestore();
			$('#example').dataTable( {
				"bSortClasses": true
			} );
		},
		function () { return $('#example tbody tr:eq(0) td:eq(0)').hasClass('sorting_1'); }
	);
	
	
	oTest.fnComplete();
} );