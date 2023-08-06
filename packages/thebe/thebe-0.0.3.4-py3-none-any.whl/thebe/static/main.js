vm={}
document.addEventListener("DOMContentLoaded", function(){
	cells={}
	vm=new Vue({
		el: '#app',
		data: {
			cells:cells,
			spinnerHtml:'<div class="lds-grid"></div>'

		},
		delimiters: ['[[',']]']
	})
	var socket = io();
	function myCallback() {
//		socket.emit('checkOnUpdate')
	 }
	socket.on('connect', function() {
		console.log('Connected to server');
        });
	socket.on('disconnect', function() {
		console.log('Disconnected to server');
        });
	socket.on('ping client', function() {
		socket.emit('check if saved')
	});
	socket.on('show loading', function(newCells) {
		vm.cells=newCells
	});
	socket.on('show output', function(newOutput) {
		for (var i in vm.cells){
			out=newOutput.shift()
			vm.cells[i].changed=false
			vm.cells[i].stderr=out.stderr
			vm.cells[i].stdout=out.stdout
			vm.cells[i]['image/png']=out['image/png']
		}
	});
	socket.on('show all', function(cellList) {
		vm.cells=cellList
	});
});
