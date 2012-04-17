/**
 * Created by PyCharm.
 * User: modland
 * Date: 3/16/12
 * Time: 11:08 AM
 * To change this template use File | Settings | File Templates.
 */

function search_submit(){
    var query = $("#id_query").val();
    $("#search-results").load(
        "/search/?ajax&query=" + encodeURIComponent(query)
    );
    return false;
}

$(document).ready(function () {
    $("#search-form").submit(search_submit);
});