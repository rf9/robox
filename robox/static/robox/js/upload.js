/**
 * Created by rf9 on 11/09/2015.
 */

$(document).ready(function () {
    $('#id_barcode').focus();

    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});