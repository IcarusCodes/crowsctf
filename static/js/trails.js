$(document).ready(function() {
  var $grid = $('.grid')
  var $gridItem = $('.grid__item')

  var gridItemHeight = $gridItem.height()
  var gridItemWidth = $gridItem.width()

  var horzCount = Math.floor($grid.width() / gridItemWidth)
  var vertCount = Math.floor($grid.height() / gridItemHeight)

   console.log("Hor count: " + horzCount);
   console.log("Ver count: " + vertCount);

  var totalGridItems = horzCount * vertCount
  console.log("Total count: " + totalGridItems);

  for (var i = 0; i < totalGridItems; i++) {
    var $gridItemClone = $gridItem.clone()
    $grid.append($gridItemClone)
  }
})
