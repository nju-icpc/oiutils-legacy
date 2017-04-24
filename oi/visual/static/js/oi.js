function workout(s) {
    var lines = s.split('\n');
    var content = new Array();
    var prob = new Array();
    var startJudging = false;
    var totalScore = new Array();
    var index = new Array();

    var probNum = parseInt(lines[0]);
    for (var i = 1; i < 1 + probNum; i++) {
        var msg = lines[i].split('-');
        prob[msg[0]] = new Array();
        for (var j = 1; j < msg.length; j++)
            prob[msg[0]].push(parseInt(msg[1]));
    }

    for (var i = 1 + probNum; i < lines.length; i++) {
        var msg = lines[i].split('-');
        if (!msg[2]) continue;
        if (msg[2] == 'compiling') {
            content[msg[0]] = new Array();
            content[msg[0]]['__compiling__'] = true;
            totalScore[msg[0]] = -1;
            index.push(msg[0]);
            continue;
        }
        content[msg[0]]['__compiling__'] = false;
        if (totalScore[msg[0]] == -1) totalScore[msg[0]] = 0;
        startJudging = true;
        if (!content[msg[0]]) content[msg[0]] = new Array();
        if (!content[msg[0]][msg[1]]) content[msg[0]][msg[1]] = 0;
        content[msg[0]][msg[1]] += parseInt(parseFloat(msg[3])) * prob[msg[1]][parseInt(msg[2])];
        totalScore[msg[0]] += parseInt(parseFloat(msg[3])) * prob[msg[1]][parseInt(msg[2])];
    }
    index.sort(function(a, b) {
        return totalScore[b] - totalScore[a]; 
    });

    var $table = $('<table id="hor-minimalist-a"></table>');
    var $tr = $('<tr></tr>');
    $tr.append($('<th>contestant</th>'));
    for (var i in prob) {
        $tr.append($('<th>' + i + '</th>'));
    }
    $tr.append($('<th>total</th>'));
    $table.append($tr);

    for (var i in index) {
        var cst = index[i];
        $tr = $('<tr></tr>');
        $tr.append('<td>' + cst + '</td>');
        if (content[cst]['__compiling__']) {
            if (!startJudging) $tr.append('<td>Compiling</td>');
            else $tr.append('<td>Waiting</td>');
        }
        else {
            for (var i in prob) {
                if (!content[cst][i]) $tr.append($('<td>0</td>'));
                else $tr.append($('<td>' + content[cst][i] + '</td>'));
            }
            $tr.append($('<td>' + totalScore[cst] + '</td>'));
        }
        $table.append($tr);
    }
    $('#ranklist').html($table);
}
function getRanklist() {
    console.log('Getting ranklist....');
    var data = {};
    $.getJSON(
        $SCRIPT_ROOT + '/get_ranklist', 
        {},
        function(data) {
            workout(data.result);
            setTimeout(getRanklist, 2000);
    });
}

$(document).ready(function() {
    setTimeout(getRanklist(), 2000);
});
