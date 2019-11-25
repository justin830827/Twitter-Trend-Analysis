
function getAndRenderTopK() {
    $('#go-button').hide()
    $('#result-container').hide()
    $('#loading-button').show()

    var request = {
        "endTime": document.getElementById("end-time-input-box").value,
        "place": document.getElementById("place-input-box").value,
        "startTime": document.getElementById("start-time-input-box").value,
        "term": document.getElementById("term-input-box").value,
        "k": parseInt(document.getElementById("k-input-box").value)
    }

    fetch('/api/heavyhitters/search', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request)
    })
    .then(result => result.json())
    .then(items => renderResponse(items));
}

function createRow(wordFrequency, index) {
    return React.createElement('tr', null, [
        React.createElement('th', {'scope': 'row'}, index + 1),
        React.createElement('td', null, wordFrequency['word']),
        React.createElement('td', null, wordFrequency['count'])
    ])
}

function renderResponse(items) {
    items = items.sort(function(a, b) {
        return b['count'] - a['count'];
    });

    var tableContainer = document.getElementById('top-results-table');

    var rows = items.map(createRow);

    var thead = React.createElement('thead', {className: 'thead-dark'},
        [
            React.createElement('tr', null, [
                React.createElement('th', {'scope': 'col'}, '#'),
                React.createElement('th', {'scope': 'col'} , 'Word'),
                React.createElement('th', {'scope': 'col'}, 'Frequency')
            ])
        ]
    );

    var tbody = React.createElement('tbody', null, rows);

    var table = React.createElement('table', {className: 'table table-bordered text-center'}, [thead, tbody]);

    ReactDOM.render(table, tableContainer)

    $('#loading-button').hide()
    $('#go-button').show()
    $('#result-container').show()
}
