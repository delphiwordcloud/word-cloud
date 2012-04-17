/**
 * Created by PyCharm.
 * User: academy
 * Date: 3/16/12
 * Time: 1:34 PM
 * To change this template use File | Settings | File Templates.
 */
function corpus_edit() {
    var item = $(this).parent();
    var url = item.find(".title").attr("href");
    item.load(
        "/save/?ajax&url=" + encodeURIComponent(url),
        null,
        function () {
            $("#save-form").submit(corpus_save);
        }
    );
    return false
}

$(document).ready(function () {
    $("ul.corpora .edit").click(corpus_edit)
});

function corpus_save() {
    var item = $(this).parent();
    var data = {
        file:  item.find("#id_file").val(),
        title: item.find("#id_title").val(),
        tags:  item.find("#id_tags").val()
    };
    $.post("/save/?ajax", data, function (result) {
        if (result != "failure"){
            item.before($("li", result)).get(0);
            item.remove();
            $("ul.corpora .edit").click(corpus_edit);
        }
        else {
            alert("Failed to validate corpus before saving.");
        }
    });
    return false;
}