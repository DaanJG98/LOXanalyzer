// create an array with nodes
        var lijst = ['Bleeching', 'Lipoxygenase', '13-LOX', 'Cancer stuff', 'improve grain qualities'];
        var nodes = new vis.DataSet([]);

        for (i=0; i<lijst.length; i++){
        nodes.add({id: i, label:lijst[i]});

//        var nodes = new vis.DataSet(
//        [
//            {id: 1, label: 'Bleeching'},
//            {id: 2, label: 'Lipoxygenase'},
//            {id: 3, label: '13-LOX'},
//            {id: 4, label: 'Cancer stuff'},
//            {id: 5, label: 'improve grain qualities'}
//        ]
//        );

        // create an array with edges
        var edges = new vis.DataSet([
            {from: 1, to: 3, label:'500'},
            {from: 1, to: 2, label:'253'},
            {from: 2, to: 4, label:'120'},
            {from: 2, to: 5, label:'53'}
        ]);

        // create a network
        var container = document.getElementById('mynetwork');

        // provide the data in the vis format
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {};

        // initialize your network!
        var network = new vis.Network(container, data, options);