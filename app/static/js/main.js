

$("[data-url]").click(function(){
    window.location.href = $(this).attr("data-url");
});
console.log($(".menu .item"));
$(".menu .item").tab();