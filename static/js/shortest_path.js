/*function handleShortestPathSearch(event){
    event.preventDefault();
    let requestData;
    requestData = $("#findShortestPathForm").serializeArray();
    console.log(requestData);
    
}*/

$(document).ready(function () {
    //Load Rack Contents
    $("#sourceRackName").select2();
    $("#destinationRackName").select2();
    $("#mediaType").select2();
    $.ajax({
        method: "GET",
        url: "/rack"
    }).done(function (msg) {
        console.log(msg);
        msg.forEach(element => {
            let optionText = element.site + "/" + element.building + "/" + element.room + "/" + element.name;
            $("#sourceRackName").append("<option value=\"" + element.id +"\">" + optionText +"</option");
            $("#destinationRackName").append("<option value=\"" + element.id +"\">" + optionText +"</option");
        });
    });
    $("#findShortestPathForm").submit(function (event) {
        event.preventDefault();
        let indexedData = {};
        let unindexedData = $(this).serializeArray();
        unindexedData.forEach(element => {
            indexedData[element.name] = element.value;
        });
        let requestData = {};
        requestData["rack1"] = { id: indexedData["sourceRackName"] };
        requestData["rack2"] = { id: indexedData["destinationRackName"] };
        requestData["mediaType"] = indexedData["mediaType"]
        console.log(requestData);
        $.ajax({
            method: "POST",
            url: "/shortest-path",
            data: JSON.stringify(requestData),
            contentType: "application/json"
        })
            .done(function (msg) {
                $("#responseDataUl").empty();
                console.log(msg);
                msg[0].forEach((element, i) => {
                    console.log(typeof(msg));
                    $("#responseDataUl").append("<li class=\"list-group-item\">" + element.name + "</li>");
                });
            })
            .fail(function (msg){
                console.log(msg);
            });
    });
});