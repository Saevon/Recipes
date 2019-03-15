var _ = require('lodash');


var storeItems = [];
var me = {};


let purchased = (_.chain(storeItems)
    // Only Grab favourites
    .filter((item) => item.isFavorite)

    // Also we dont want the tools
    .reject((item) => item.category === 'tool')

    // Grab first item with the best quality of each
    .sortBy('quality')
    .groupBy('color_id')
    .map((group) => group[0])

    // Now purchase them
    .sidechain((items) => (_.chain(items)
        // The ones we can't purchase, put out an order instead
        .filter((item) => ! item.isAvailable)
        .map((item) => item.request())

        // Print the receipt for ones we could request
        .filter((purchase) => ! purchase.has_failed)
        .each((purchase) => me.print_reciept(purchase))
    ))
    .filter((item) => item.isAvailable)
    .map((item) => me.purchase(item))

    // And grab the resulting purchase ID (of ones we could buy)
    .filter((item) => item.purchase_id)
    .map((item) => item.purchase_id)
);


purchased.something();






// --------------------------
// "would be nice" functions
(_.chain(storeItems)
    .sidefilter((item) => item.isAvailable, (items) => _.chain(items)
        // Transforms the original list (pre-filter)
        // Thus changing only the items in that list that were filtered
        .map((item) => item.purchase())

        // Here we still have the filtered list (which continues to)
        // Affect the old list
    )
    // Here we have the original list, but after some items were changed
);







