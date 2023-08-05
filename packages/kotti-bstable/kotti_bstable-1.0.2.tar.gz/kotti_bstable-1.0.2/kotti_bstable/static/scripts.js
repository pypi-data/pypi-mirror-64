function urlFormatter(value, row, index) {
    return "<a href='"+row.url+"'>"+value+"</a>";
}

function htmlFormatter(value, row, index) {
    return $("<div></div>").append(value).html();
}

function dateSorter(a, b){
    if (a.date < b.date) return -1;
    if (a.date > b.date) return 1;
    return 0;
}