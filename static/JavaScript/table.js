// to highlight the current row
function highlight(tableIndex) {
    // Just a simple check. If .highlight has reached the last, start again
    console.log("inside highlight table fun")

    // Element exists?
    if ($('#data tbody tr:eq(' + tableIndex + ')').length > 0) {
        // Remove other highlights
        $('#data tbody tr').removeClass('highlight');

        // Highlight your target
        $('#data tbody tr:eq(' + tableIndex + ')').addClass('highlight');
    }
}